#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-02-11.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import networkx as nx
from itertools import combinations
from copy import copy
import numpy
import string
from collections import defaultdict

DESIRED_COLUMNS = ["degree_nodes", "degree_metrics", "degree_neighbors", "activity_nodes", "activity_metrics",\
 "activity_neighbors", "weightloss_nodes", "weightloss_metrics", "weightloss_neighbors"]

def transform_labels_to_nx(G):
	H = nx.Graph()
	label_mapping = {}
	#add the nodes by label from G to H
	for node in G.nodes(data=True):
		H.add_node(node[1]['label'])
		label_mapping[node[0]] = node[1]['label']
		if len(node[1]) > 2:
			for key in node[1]:
				H.node[node[1]['label']][key] = node[1][key]
	#add the appropriate edges
	for edge in G.edges(data=True):
		H.add_edge(label_mapping[edge[0]], label_mapping[edge[1]])
		if len(edge[2]) > 0:
			for key in edge[2]:
				H[label_mapping[edge[0]]][label_mapping[edge[1]]][key] = edge[2][key]			
	return H
 
def prep_csv(summary):
    csv_file = open(summary).readlines()
    #separate the header from the data
    header = csv_file[0].split(",")
    data = csv_file[1:]
    #sanitize the data
    f = lambda x:x.strip().split(",")
    data=map(f, data)
    find_columns = lambda x:header.index(x)
    columns = map(find_columns, DESIRED_COLUMNS)
    #split the neighbors into lists
    g = lambda x: ":" in x and x.split(":") or x
    for i in range(len(data)):
        data[i] = map(g, data[i])
    
    selected_header = DESIRED_COLUMNS
    selected_data = []
    for d in data:
        entry = []
        for c in columns:
            entry.append(d[c])
        selected_data.append(entry)
        
    return selected_header, selected_data

def get_high_nodes(header, data):
    node_columns = filter(lambda x:"nodes" in x and x,header)
    data_columns = filter(lambda x:"metrics" in x and x, header)
    node_indeces = map(lambda x:header.index(x), node_columns)
    data_indeces = map(lambda x:header.index(x), data_columns)
    metric_names = map(lambda x:x.split("_")[0], node_columns)
    #for each metric, put together a list of node-metric pairs
    highs = {}

    for m in metric_names:
        highs[m] = {"node":[], "value":[]}
    for d in data:
        for m,n,v in zip(metric_names,node_indeces, data_indeces):
            highs[m]["node"].append(d[n])
            highs[m]["value"].append(d[v])

    return highs

def get_high_neighbors(header, data):
    node_columns = filter(lambda x:"nodes" in x and x,header)
    data_columns = filter(lambda x:"neighbors" in x and x, header)
    node_indeces = map(lambda x:header.index(x), node_columns)
    data_indeces = map(lambda x:header.index(x), data_columns)
    metric_names = map(lambda x:x.split("_")[0], node_columns)
    #for each metric, put together a list of node-metric pairs
    highs = {}

    for m in metric_names:
        highs[m] = {"node":[], "value":[]}
    for d in data:
        for m,n,v in zip(metric_names,node_indeces, data_indeces):
            highs[m]["node"].append(d[n])
            highs[m]["value"].append(d[v])

    return highs
    
def compute_intersections(node_sets):
    for c in combinations(node_sets,len(node_sets)):
        intersect = c[0].intersection(c[1])
        for i in range(2,len(node_sets)):
            intersect = intersect.intersection(c[i])
    return intersect
    
def compute_unions(node_sets):
    for c in combinations(node_sets,len(node_sets)):
        u = c[0].union(c[1])
        for i in range(2,len(node_sets)):
            u = u.union(c[i])
    return u

def compute_combination_percentage(high_nodes):
	#compute overall node intersections
	intersection_sizes = range(2,len(high_nodes.keys())+1)
	intersect_dictionary = {}
	for i in intersection_sizes:
		#print str(i) + "-way intersections"
		#print "size, percentage"
		for c in combinations(high_nodes.keys(),i):
			#print "-".join(c) + " intersection:"
			f = lambda x:high_nodes[x]["node"]
			set_combinations = map(set, map(f,c))
			intersect = compute_intersections(set_combinations)
			u = compute_unions(set_combinations)
			key = ".".join(c)
			intersect_dictionary[key] = {"intersect":intersect, "total":u}

	return intersect_dictionary

def read_communities(com_file):
	lines = open(com_file).readlines()
	communities = []
	for line in lines:
		communities += line.strip().split(";")
	f = lambda x:x.strip().split(",")
	communities = map(f, communities)
	for i in range(len(communities)):
		communities[i] = map(string.strip, communities[i])
	com_dict = {}
	for i in range(len(communities)):
		for n in communities[i]:
			com_dict[n] = i+1
	return communities, com_dict

def get_set_weightloss(s, G):
	w_loss = []
	for n in s:
		w_loss.append(float(G.node[n]['weightloss']))
	return w_loss

def build_csv(data_hash):
	header = ",".join(map(str,data_hash.keys()))
	lines = [header]
	#we need to pad all entries with the difference between them and the maximum length column
	longest = max(map(len, data_hash.values()))
	for col in data_hash:
		if len(data_hash[col]) < longest:
			data_hash[col] += [" " for pad in range(longest-len(data_hash[col]))]
	#sanity check
	f = lambda x: len(x)==longest
	if sum(map(f, data_hash.values())) == len(data_hash):
		#assemble csv
		#make interleaved rows
		rows = zip(*data_hash.values())
		f = lambda x: ",".join(map(str, x))
		lines += map(f, rows)

	return lines

def print_csv(rows, filename):
	f = open(filename, "w")
	for r in rows:
		print >> f, r
	f.close()
	
def make_blockmodel(G, communities):
	B = nx.DiGraph()
	#add the nodes
	for c in range(len(communities)):
		B.add_node(c)
	
	#add the node sizes and edges
	
	for c in range(len(communities)):
		B.node[c]['size'] = len(communities[c])
		weight_loss = 0.0
		for n in communities[c]:
			weight_loss += float(G.node[n]['weightloss'])
			for m in range(len(communities)):
				if communities[m] != communities[c]:
					if len(set(G.neighbors(n)).intersection(communities[m])) > 0:
						B.add_edge(c, m,weight=float(len(set(G.neighbors(n)).intersection(communities[m]))))
			B.node[c]['weightloss'] = weight_loss/ len(communities[c])						
	return B
			
		
	
def main(summary, graph=None, communities=None):

	#I need to annotate the graph to include community roles
	header, data = prep_csv(summary)
	output_file_prefix = "/".join(summary.split("/")[:-1])
	csv_file_prefix = "/"+str(len(data))+"point_intersections"
	block_model_suffix = "/block_model.gml"

	high_nodes = get_high_nodes(header,data)
	overall_metric_intersections = compute_combination_percentage(high_nodes)
	
	if graph:
		G = nx.read_gml(graph)
		G = transform_labels_to_nx(G)
		
		giant = nx.connected_component_subgraphs(G)[0]
		# if we have a community index, annotate the giant component with it
		if communities:
			communities, community_dictionary = read_communities(communities)
			for n in giant.nodes(data=True):
				n[1]['community'] = community_dictionary[n[0]]
			B = make_blockmodel(G, communities)
			nx.write_gml(B, output_file_prefix+block_model_suffix)
			nx.write_gml(G, graph)
		#make the over all summaries
		overall_summary = {}
		for key in overall_metric_intersections:
			#if this is a weight-loss intersection
			if 'weightloss' in key:
				#get the set of weighlosses for these nodes
				w_loss = get_set_weightloss(overall_metric_intersections[key]['intersect'],G)
				overall_summary[key] = w_loss
				
		high_nodes_in_giant_component = {}
		high_nodes_outside_giant_component = {}
		for metric in high_nodes:
			# print "examining "+metric+" in and out of the giant component"
			high_nodes_in_giant_component[metric]={"node":[], "value":[]}
			high_nodes_outside_giant_component[metric]={"node":[], "value":[]}
			nodes = high_nodes[metric]["node"]
			high_metric_inside = [h in giant.nodes() and h for h in nodes]
			for i in range(len(nodes)):
				if high_metric_inside[i]:
					high_nodes_in_giant_component[metric]["node"].append(high_nodes[metric]["node"][i])
					high_nodes_in_giant_component[metric]["value"].append(high_nodes[metric]["value"][i])
				else:
					high_nodes_outside_giant_component[metric]["node"].append(high_nodes[metric]["node"][i])
					high_nodes_outside_giant_component[metric]["value"].append(high_nodes[metric]["value"][i])
			if "weightloss" in metric:
				overall_summary[metric+".inside.giant"] = get_set_weightloss(high_nodes_in_giant_component[metric]["node"],G)
				overall_summary[metric+".outside.giant"] = get_set_weightloss(high_nodes_outside_giant_component[metric]["node"],G)
				
		overall_summary["whole.network"] = get_set_weightloss(G.nodes(), G)
		
		#build the csv of the overall summary and write to file
		csv_rows = build_csv(overall_summary)
		print_csv(csv_rows, output_file_prefix+csv_file_prefix+"_overall_summary.csv")
		
		
		#end of overall summaries
		#begin scoping down of the giant component
		giant_component_scope_summary = {}
		node_wise_summary = {}
		
		giant_component_intersections = compute_combination_percentage(high_nodes_in_giant_component)
		disconnected_component_intersections = compute_combination_percentage(high_nodes_outside_giant_component)
		#since we have the graph, let's do neighbor analysis as well
		
		
		#let's start with the mean weight-loss of all neighbors for each of the intersections
		giant_component_scope_summary["giant.component"] = get_set_weightloss(giant.nodes(), G)
		
		
		for key in giant_component_intersections:
			#for each key, get all the neighbors of each node
			intersection_neighbors = set()
			difference_neighbors = {}
			for node in giant_component_intersections[key]["intersect"]:
				intersection_neighbors = intersection_neighbors.union(G.neighbors(node))
				difference_neighbors[node] = set(G.neighbors(node))
			unique_neighbors = intersection_neighbors.difference(giant_component_intersections[key]["intersect"])
			# use difference neighbors to measure the influence of each of the top 100 in this intersection
			difference_neighbor_metrics = {}
			difference_neighbor_metrics["node"] = []
			difference_neighbor_metrics["size"] = []
			difference_neighbor_metrics["mean"] = []
			difference_neighbor_metrics["sd"] = []
			for node in giant_component_intersections[key]["intersect"]:
				for other_node in giant_component_intersections[key]["intersect"]:
					if node != other_node:
						difference_neighbors[node] = difference_neighbors[node].difference(G.neighbors(other_node))
				if len(difference_neighbors[node]) > 0:
					node_wise_summary[key+".node."+node]=get_set_weightloss(difference_neighbors[node],G)
					
			#get the mean weight loss
			giant_component_scope_summary['one.hop.neighborhood'] = get_set_weightloss(unique_neighbors, G)
			
			
			
			outside_influence = set(giant.nodes()).difference(unique_neighbors.union(giant_component_intersections.keys()))
			giant_component_scope_summary[key+'.outside.one.hop'] = get_set_weightloss(outside_influence, G)
			
			#build the csv of the giant component summary and write to file
			csv_rows = build_csv(giant_component_scope_summary)
			print_csv(csv_rows, output_file_prefix+csv_file_prefix+"_giant_component_summary.csv")
			if len(node_wise_summary) > 0:
				csv_rows = build_csv(node_wise_summary)
				print_csv(csv_rows, output_file_prefix+csv_file_prefix+"_node_wise_summary.csv")
		
			
		#now let's do communities
		if communities:
			#collect all the weigh losses for each community
			community_w_loss = defaultdict(list)
			for key in community_dictionary:
				community_w_loss["community."+str(giant.node[key]['community'])].append(giant.node[key]['weightloss'])
			
			#build the csv of the community summary and write to file
			csv_rows = build_csv(community_w_loss)
			print_csv(csv_rows, output_file_prefix+csv_file_prefix+"_community_summary.csv")

		# DMC: This is preserved in case someone wanted to check the disconnected component (which is not significant for CK)
		# print "disconnected component non-community summary"
		# for key in disconnected_component_intersections:
		# 	#for each key, get all the neighbors of each node
		# 	intersection_neighbors = set()
		# 	for node in disconnected_component_intersections[key]["intersect"]:
		# 		intersection_neighbors = intersection_neighbors.union(G.neighbors(node))
		# 	unique_neighbors = intersection_neighbors.difference(disconnected_component_intersections[key]["intersect"])
		# 	#get the mean weight loss
		# 	if "weightloss" in key:
		# 		print unique_neighbors
		# 		if len(unique_neighbors) > 0:
		# 			giant_component_scope_summary[key+'.disconnected.component.one.hop'] = get_set_weightloss(unique_neighbors, G)




if __name__ == '__main__':
	cam_summary = sys.argv[1]
	communities = None
	graph = None
	if len(sys.argv) > 2:
		graph = sys.argv[2]
	if len(sys.argv) > 3:
		communities = sys.argv[3]
		
	main(cam_summary, graph, communities)

