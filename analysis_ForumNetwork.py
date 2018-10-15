#! /usr/bin/env python

"""
Created by Julia Poncela of March 2011

Perform the basic topological analysis of the Forum Network: P(k), 
P(num_posts), P(num_posters), number of connected components,

Community analysis


"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import date
import networkx as nx




def main (file_name):


    G=nx.read_gml(file_name) # create the network from the original input file  


    #G=nx.gnp_random_graph(1000, 0.2)
    Pk=nx.degree_histogram(G)  # create a list with the frequencies of every connectivity 



    print Pk
   

    components=nx.connected_component_subgraphs(G) # create a list of lists

    num_nodes=len(G)

    print len(components), "connected component(s)"
   

    P_members=[0.0]*num_nodes
    P_posts=[0.0]*num_nodes
    
    for nodo in G.nodes():
        size=G.node[nodo]['size']       
        P_members[size]=P_members[size]+1
       

        num_posts=G.node[nodo]['num_posts']        
        P_posts[num_posts]=P_posts[num_posts]+1
       
 




   
    file1 = open("Post-poster_distributions_CK_forums.dat",'wt') # just to check
    for i in range(num_nodes):       
        print >> file1, i, P_members[i]/num_nodes,P_posts[i]/num_nodes 
    file1.close()


    file2 = open("Pk_CK_forums.dat",'wt')
    for i in range(len(Pk)+1):
        print >> file2, i, float(Pk[i])/num_nodes        
    file2.close()



    nx.write_edgelist(G, "Forum_network_edgelist") # for the community analysis


    print "done!"


 #########################


if __name__== "__main__":
    if len(sys.argv)>1:
        file_name=sys.argv[1]   
    
        main(file_name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
        
