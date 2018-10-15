#!/usr/bin/env python

"""
Created by Julia Poncela on May  2010

Given a network.gml it adds new attributes corresponding to the rank on some otrhe attributes.

It takes as argument the path/network.gml  


"""

import sys
import os
import networkx as nx
import math
from pylab import *
import numpy
 
def main(graph_name):
  
    G = nx.read_gml(graph_name)
    G = nx.connected_component_subgraphs(G)[0] # Giant component 
  
   

    dir=graph_name.split("fr")[0]



    
    name00=dir+"scatter_plot_overlap_rank_top_tens.dat"
    file0=open(name00, 'wt')
    file0.close()

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics


# clustering, vitality, activity, betweenness,weigh_ins,degree,time_in_system

    list_top_ten_feature=['time_in_system','activity','betweenness','weigh_ins','degree','vitality']



    list_new_labels=[]
    list_top_tens_total=[] 
    for feature in list_top_ten_feature:

        f = lambda x:x[1][feature]
        membership = map(f,G.nodes(data=True))
        membership.sort()
        top_ten_values = membership[-20:]  #TOP TWENTY



      
      
        list_top_tens=[]     # collect the top_tens of the system
        cont=1
        for value in top_ten_values:
            for node in G.nodes():
                if (G.node[node][feature]==value) and (node not in list_top_tens) :
                   
                    if node not in  list_top_tens_total:
                        list_top_tens_total.append(node)

                    list_top_tens.append(node)
                    new_label=str(feature)+"_index"
                    G.node[node][new_label]=cont

                    cont=cont+1

                    print G.node[node][feature],G.node[node][new_label]


                    if new_label not in list_new_labels:               
                        list_new_labels.append(new_label)

    print "tot_number_top_tens",len(list_top_tens_total)
    print list_new_labels

    file0=open(name00, 'at')
    for node in G.nodes():
        if node in  list_top_tens_total:
            print >> file0,G.node[node]['label'],
            
            for l in list_new_labels:
                try:
                    print >> file0,l,G.node[node][l],
                except KeyError:
                    print >> file0,0,
                    
            print >> file0,'\n'        
    file0.close()
                

    cont=1
    file0=open(name00+'_R6s', 'wt')
    for node in G.nodes():
         if node in  list_top_tens_total:
             if G.node[node]['role']=="R6":
                 print >> file0,G.node[node]['label'],
                 cont=cont+1
                 for l in list_new_labels:
                     try:
                         print >> file0,l,G.node[node][l],
                     except KeyError:
                         print >> file0,0,
                    
                 print >> file0,'\n'        
    file0.close()
                
      

######################################3
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
