#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-01-10.
Copyright (c) 2011 __Northwestern University__. All rights reserved.
This script performs two functions:
1) When run normally it uses Ziggy to perform bootstrapping-based comparison of weight loss in a network's giant
component with weight loss in all other components
2) When run with the "external" argument, it performs a t-test between mean weight loss of all networked users
and all un-networked users
"""

import sys
import os
import string
import networkx as nx
import scipy.stats
import numpy

ITERATIONS = 1000

def compute_external_weight_loss(G, data):
    components = nx.connected_component_subgraphs(G)
    #remove the giant component
    giant_component = components[0]
    components.remove(giant_component)
    #for all remaining components, compared connected with unconnected
    #as a precaution, remove any self-edges from G
    for e in G.edges():
      if e[0]==e[1]:
        G.remove_edge(e[0],e[1])
    
    #Group nodes into two bins: those with a connection versus those without
    with_connection = giant_component.nodes()
    without_connection = []
    component_edges = map(len, map(dict.values, map(nx.Graph.degree, components)))
    for i in range(len(component_edges)):
      if component_edges[i] == 1:
        without_connection += components[i].nodes()
      else:
        with_connection += components[i].nodes()
    
    connected_weight_loss = []
    disconnected_weight_loss = []
    
    for n in with_connection:
      connected_weight_loss.append(data[n])
    
    for n in without_connection:
      disconnected_weight_loss.append(data[n])
    
    external_count = len(without_connection)
    for n in data:
      #these too are people without a significant connection
      if n not in with_connection and n not in without_connection:
        disconnected_weight_loss.append(data[n])
        external_count += 1
    
    return connected_weight_loss, disconnected_weight_loss
    
    

def compute_mean_weight_loss(G,data):
    components = nx.connected_component_subgraphs(G)
    giant_component = components[0]
    components.remove(giant_component)
    
    giant_component_weight_loss = 0.0
    for n in giant_component.nodes():
        try:
            giant_component_weight_loss += data[n]
        except KeyError:
            pass
    giant_component_weight_loss /= float(len(giant_component))
    
    external_component_weight_loss = 0.0
    for c in components:
        for n in c.nodes():
            try:
                external_component_weight_loss += data[n]
            except KeyError:
                pass
    external_component_weight_loss /= float(sum(map(len,components)))
    
    return giant_component_weight_loss, external_component_weight_loss
    
def main(graph_filename, data_filename,external=False):
    graph_name = data_filename.strip().split(".")[0]
    randomization_mapper = 'make_random_graphs.py'
    if not external:
      mean_collector = "collect_mean_values.py"
      ITERATIONS = 1000
    else:
      mean_collector = None
      ITERATIONS = 1
    #mean_collector=None
    supporting_files = ["ck_mc_graph", "ck_mc_data", "mean_chk", "GraphRandomization.py"]
    G = nx.read_edgelist(graph_filename)
    #data is organized as:
    #"id", "ck_id", "weigh_ins", "weight_change", "days"
    dataset = open(data_filename).readlines()[1:]
    dataset = map(string.strip, dataset)
    data = {}
    for line in range(len(dataset)):
        dataset[line] = dataset[line].split(',')
        data[dataset[line][0]]=float(dataset[line][1])
    
    os.system("cp "+graph_filename + " ck_mc_graph")
    f = open("ck_mc_data", "w")
    for key in data:
        print >> f, str(key) + " " + str(data[key])
    f.close()

    if external:
      giant_mean, external_mean = compute_external_weight_loss(G,data)
      output_filename = graph_name+"_external_mean_z_score"
      output = str(sum(giant_mean)/float(len(giant_mean))) + " " + str( sum(external_mean)/float(len(external_mean)))+"\n"
      output += str(scipy.stats.shapiro(numpy.array(giant_mean)))+"\n"
      output += str(scipy.stats.shapiro(numpy.array(external_mean)))+"\n"
      output += "t.test:"+str(scipy.stats.ttest_ind(numpy.array(giant_mean), numpy.array(external_mean)))+"\n"
      output += "mood.median:"+str(scipy.stats.mood(numpy.array(giant_mean), numpy.array(external_mean)))+"\n"
      print output
      
    else:
      giant_mean, external_mean = compute_mean_weight_loss(G,data)
      args=""
      output_filename = graph_name +"_mean_z_score"
      f = open("mean_chk", "w")
      print >> f, " ".join(map(str, [giant_mean, external_mean]))
      f.close()
    
      hdmc.submit_inline(randomization_mapper, output_filename, ITERATIONS, supporting_files, mean_collector,arguments=args,debug=False, num_mappers = config.num_map_tasks)
      output = hdfs.cat(output_filename+"/part*")["stdout"]

    f = open(output_filename+".dat", "w")
    for line in output.split("\n"):
        print >> f, line.strip()
    f.close()


if __name__ == '__main__':
    try:
        import psyco
        from ziggy import hdmc
        from ziggy.hdmc import hadoop_config as config
        import ziggy.hdmc.hdfs as hdfs
    except ImportError:
        pass
    external = False
    if len(sys.argv) > 2:
        graph_filename = sys.argv[1]
        data_filename = sys.argv[2]
    else:
        print "Usage: compare_weight_loss_mean_to_random graph_filename data_filename"
    if len(sys.argv) > 3:
      if sys.argv[3] == "external":
        external = True
    main(graph_filename, data_filename, external)

