#! /usr/bin/env python

import numpy
import sys
import networkx as nx
import string
import pprint
from standard_deviation_class import mean, stddev

"""
one_hop_analysis.py

Created by Rufaro Mukogo on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script computes the average and standard deviation of the weight_loss of the nearest
neighbors of a list of nodes. The input is a list of nodes read from a file, the output is a dictionary with the mean
weight loss for the one-hoop neighbors and the standard deviations for those losses for the one hop neighbors.
"""
    
def one_hop_analysis(num_points,input_file,graph_file,path): 
        
    full_path = str(path)+str(num_points)+"_points_network/data/"
    
    G = nx.read_gml(full_path+graph_file) 
    
    try:
        f = open(str(full_path)+str(input_file),"r" )

    except IOError:
        pass
   
    top_nodes_list = [x.split()[0] for x in f.readlines()[2:]]

    #print "top_nodes_list", len(top_nodes_list)

    out_put = input_file.strip().split(".")[0]

    print out_put

    h = open(str(full_path)+str(out_put)+"_means_stds.dat","w")

    top_nodes = map(string.strip,top_nodes_list)
    print "top_nodes", top_nodes
    string_mapping = dict(zip(G.nodes(), map(str, G.nodes())))
    #print string_mapping
    
    G = nx.relabel_nodes(G, string_mapping)
    
    neighbor_tuples = []
    
    for n in top_nodes:
        #print "nodes---",n
        neighbor_tuples.append((n,G.neighbors(n)))
        #print neighbor_tuples
    
    neighbors = dict(neighbor_tuples)
    
    print "neigbours", neighbors

    weight_changes = []
    weight_change_means = []
    weight_change_std_devs = []
    
    for n in top_nodes:
        data = neighbors[n]
        
        weight_changes.append((n,[G.node[k]['weightloss'] for k in data]))
        weight_change_means.append((n,mean([G.node[k]['weightloss'] for k in data])))
        weight_change_std_devs.append((n,stddev([G.node[k]['weightloss'] for k in data])))
          
    print>>h, "node","weight change averages","weight_change_std_dev"
    

    weight_changes.append((n,[G.node[k]['weightloss'] for k in data]))

    weight_changes = dict(weight_changes)
    weight_change_means = dict(weight_change_means)
    weight_change_std_devs = dict(weight_change_std_devs)
       
    print "weight changes"
    pprint.pprint (dict(weight_changes))
    print "weight change averages"
    pprint.pprint (dict(weight_change_means))
    print "weight change standard deviations"
    pprint.pprint (dict(weight_change_std_devs))
    
    for n in top_nodes:
        print>>h, n, weight_change_means[n], weight_change_std_devs[n]
    
    return dict(weight_changes),dict(weight_change_means),dict(weight_change_std_devs)
    
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        num_points = int(sys.argv[1])
    else:
        num_points = 5

    if len(sys.argv) >2:
        input_file = str(sys.argv[2])
    else:
        input_file= "top_100_highest_weight_loss_but_not_degree_and_activity_nodes.txt"
    
    if len(sys.argv) >3:
        path = float(sys.argv[3])  
    else:
        path ="/home/staff/rmukogo/calorie_king_hg/"
        
    if len(sys.argv) > 4:
        graph_file  = str(sys.argv[4])
    else:
        graph_file = "friend_graph_all0.gml"
        
    changes, means, standard_deviations=one_hop_analysis(num_points,input_file,graph_file,path)


