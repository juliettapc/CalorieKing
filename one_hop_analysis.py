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
    	f = open(str(full_path)+str(input_file),"r")
    except IOError:
	pass
    #print "full_path", full_path 
   
    top_nodes = map(string.strip,f.readlines()[1:])

    string_mapping = dict(zip(G.nodes(), map(str, G.nodes())))
    G = nx.relabel_nodes(G, string_mapping)
    
    neighbor_tuples = []
    
    for n in top_nodes:
        print "nodes---",n
                
        neighbor_tuples.append((n,G.neighbors(n)))
        print neighbor_tuples
    
    neighbors = dict(neighbor_tuples)
    
    weight_changes = []
    weight_change_means = []
    weight_change_std_devs = []
    
    for n in top_nodes:
        data = neighbors[n]
        
        weight_changes.append((n,[G.node[k]['weightloss'] for k in data]))
        weight_change_means.append((n,mean([G.node[k]['weightloss'] for k in data])))
        weight_change_std_devs.append((n,stddev([G.node[k]['weightloss'] for k in data])))
    
    pprint.pprint (dict(weight_changes))
    pprint.pprint (dict(weight_change_means))
    pprint.pprint (dict(weight_change_std_devs))
    
    return dict(weight_changes),dict(weight_change_means),dict(weight_change_std_devs)
    
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        num_points = int(sys.argv[1])
    else:
          num_points = 2
    
    if len(sys.argv) >2:
        
        input_file = str(sys.argv[2])
    else:
        input_file= "top_10_highest_degree_and_activity_nodes.txt"
    
    if len(sys.argv) >3:
        path = str(sys.argv[3])  
    else:
        path ="./"
        
    if len(sys.argv) > 4:
        graph_file  = str(sys.argv[4])
    else:
        graph_file = "friend_graph_all0.gml"
        
    changes, means, standard_deviations=one_hop_analysis(num_points,input_file,graph_file,path)



