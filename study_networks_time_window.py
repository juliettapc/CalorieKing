#! /usr/bin/env python

"""
Created by Julia Poncela of June 2012

Analyze the strength of the links with R6s, defined as #_messages/tot.

"""


import sys
import os
import networkx as nx
from transform_labels_to_nx import *
import histograma_gral
import numpy


def main ():


    network_all="./semester_quarter_window_networks/network_all_window_roles_diff_layers1.5.gml"   
    H = nx.read_gml(network_all)   # all network (not only GC) with Role info
    
    H = transform_labels_to_nx(H) 
    H_GC = nx.connected_component_subgraphs(H)[0] 



    list_all_R6=[]
    list_old_R6=[]
    list_list_R6s=[]

    for  i in range(8):

        i=str(i)

        name_graph="./semester_quarter_window_networks/network_Q"+i+"_window_roles_diff_layers1.5.gml"
      


        G = nx.read_gml(name_graph)   #  with Role info
        G = transform_labels_to_nx(G)  # i transform labels into id so i can match nodes from diff. networks using their Users label.

        G_GC = nx.connected_component_subgraphs(G)[0] 
        
       
               


        count_nodes_edges(G,G_GC,"Q"+i)  # graph all info,  GC, name to print out


        list_k=[]
        for n in G.nodes():
            list_k.append(len(G.neighbors(n)))
     #   print list_k
        histograma_gral.histograma(list_k,"network_Q"+i)


        list_new_R6= count_R6(G,"Q"+i)
        print "# common R6s from the previous period:",len(list(set(list_new_R6) & set(list_old_R6)))#,"namely:",list(set(list_new_R6) & set(list_old_R6))
       
        list_list_R6s.append(list_new_R6)


        list_old_R6=[]
        for item in list_new_R6:
            list_old_R6.append(item)

            if item not in list_all_R6:
                list_all_R6.append(item)

        print "# common R6s with the total accumulated so far:",len(list(set(list_new_R6) & set(list_all_R6))),"out of",len(list_all_R6)#,"namely:",list(set(list_new_R6) & set(list_all_R6))


        listCC=[]       
        for item in nx.clustering(G_GC):
            listCC.append(nx.clustering(G_GC)[item])

        print "Av. path length:", nx.average_shortest_path_length(G_GC)
        print "Clustering coeff.:", numpy.mean(listCC)



       

    min_index_for_to_intersecton=2

    for i in range(len(list_list_R6s)):  # i calculate the total intersection of R6s
        if i >= min_index_for_to_intersecton :          
            if i<min_index_for_to_intersecton+1:
                intersection= list(set(list_list_R6s[i-1]) & set(list_list_R6s[i]))
                print "total intersection at quarter",i,":",len(intersection), "with min index:",min_index_for_to_intersecton
            else:
               # print intersection
                intersection= list(set(intersection) & set(list_list_R6s[i]))
                print "total intersection at quarter",i,":",len(intersection), "with min index:",min_index_for_to_intersecton
                #print intersection
                


    
   


    list_list_R6s=[]
    list_old_R6=[]
    list_all_R6=[]

    for i in range(4):
        i=str(i)

        name_graph="./semester_quarter_window_networks/network_S"+i+"_window_roles_diff_layers1.5.gml"
      


        G = nx.read_gml(name_graph)   #  with Role info
        G = transform_labels_to_nx(G) 

        G_GC = nx.connected_component_subgraphs(G)[0] 
        
                       

        count_nodes_edges(G,G_GC,"SM"+i)  # graph all info,  GC, name to print out


        list_k=[]
        for n in G.nodes():
            list_k.append(len(G.neighbors(n)))
        #print list_k
        histograma_gral.histograma(list_k,"network_SM"+i)



        list_new_R6= count_R6(G,"SM"+i)
        print "# common R6s from the previous period:",len(list(set(list_new_R6) & set(list_old_R6)))#,"namely:",list(set(list_new_R6) & set(list_old_R6))
       
        list_list_R6s.append(list_new_R6)


        list_old_R6=[]
        for item in list_new_R6:
            list_old_R6.append(item)

            if item not in list_all_R6:
                list_all_R6.append(item)

        print "# common R6s with the total accumulated so far:",len(list(set(list_new_R6) & set(list_all_R6))),"out of",len(list_all_R6)#,"namely:",list(set(list_new_R6) & set(list_all_R6))



        listCC=[]       
        for item in nx.clustering(G_GC):
            listCC.append(nx.clustering(G_GC)[item])

        print "Av. path length:", nx.average_shortest_path_length(G_GC)
        print "Clustering coeff.:", numpy.mean(listCC)



    min_index_for_to_intersecton=1
    for i in range(len(list_list_R6s)):  # i calculate the total intersection of R6s
        if i >= min_index_for_to_intersecton :          
            if i<min_index_for_to_intersecton+1:
                intersection= list(set(list_list_R6s[i-1]) & set(list_list_R6s[i]))
                print "total intersection at quarter",i,":",len(intersection), "with min index:",min_index_for_to_intersecton
            else:
              #  print intersection
                intersection= list(set(intersection) & set(list_list_R6s[i]))
                print "total intersection at quarter",i,":",len(intersection), "with min index:",min_index_for_to_intersecton
               # print intersection
     


##############################################

def count_nodes_edges(G, G_GC, name):


       
   # print QN0.nodes(data=True)
  
    print "\n NODES in ", name, ":",len(G.nodes()),"(GC):",len(G_GC.nodes()),
    print " EDGES in ", name, ":",len(G.edges()),"(GC):",len(G_GC.edges())



##########################################################

def count_R6(G,name):
   

    list_R6=[]
    cont_R6=0
    for n in G.nodes():
        try:
            if G.node[n]['role']=="R6" or G.node[n]['role']=="special_R6":
                cont_R6+=1
                list_R6.append(n)
               
        except : pass   # for the nodes with no role (no GC)


    print "tot # R6s in",name,":", cont_R6,"namely:",list_R6


    return list_R6



 
###############################################

          
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename1 = sys.argv[1]
       

    main()
    #else:
     #   print "usage: python  whatever.py   path/network_file2_R6s_info.gml  "
 
 






###################################################
