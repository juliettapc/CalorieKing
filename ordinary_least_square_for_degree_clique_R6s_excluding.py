#!/usr/bin/env python


import sys
import os
import networkx as nx
import math
from pylab import *
import numpy
from  scipy import stats

import random


 
def main(graph_name):
  
    H = nx.read_gml(graph_name)

    for node in H.nodes():  # i remove self loops
        if node in H.neighbors(node):          
            if len(H.neighbors(node))>1:
                H.remove_edge(node,node)             
            else:
                H.remove_node(node)              





    for node in H.nodes():        
        if H.node[node]['weigh_ins'] <5: #Adherent filter
            H.remove_node(node)
           # print node, "is going down"


    G= nx.connected_component_subgraphs(H)[0] # Giant component 


    name1=graph_name.split('.gml')[0]
    name1=name1+"_values_weigh_change_users_degree_clique_R6s_excluding.csv"           
    file=open(name1, 'wt')
   
    print >> file,'label','pwc','act','log_act','wi','wi/12','ibmi','sqrt_ibmi','R6','R6_2','k','log_k','cs','cs_2',"t"


    for n in G.nodes():

        if (float(G.node[n]['initial_bmi']) >25.0)  and (G.node[n]['label']!='40155') :  #only consider obese and overweight
            if sqrt(float(G.node[n]['degree']))<=10.0:
                if int(G.node[n]['R6_overlap']) <=6:
                    if int(G.node[n]['max_clique_size']) <=7:

                        list=[]
                        list.append(G.node[n]['label'])
                        list.append(G.node[n]['percentage_weight_change'])           

                        list.append(G.node[n]['activity'])
                        list.append(log(float(G.node[n]['activity'])))
                        
                        list.append(G.node[n]['weigh_ins'])
                        list.append(float(G.node[n]['weigh_ins'])/12.0)                        
                                                
                        list.append(G.node[n]['initial_bmi'])          
                        list.append(sqrt(float(G.node[n]['initial_bmi'])))

                        list.append(G.node[n]['R6_overlap'])
                        list.append((G.node[n]['R6_overlap'])*(G.node[n]['R6_overlap']))
                                
           
                        list.append((G.node[n]['degree']-1))
                        list.append(log(G.node[n]['degree']-1))
                             
           
                        list.append((G.node[n]['max_clique_size']-2))
                        list.append((G.node[n]['max_clique_size']-2)*(G.node[n]['max_clique_size']-2))
                          
                        list.append(G.node[n]['time_in_system'])

                        for element in list:                      
                            print >> file, element,

                        print >> file, " "
 

    file.close()




  





####################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python program.py path/network_file.gml"

    
