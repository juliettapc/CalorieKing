#!/usr/bin/env python
"""
Given a gml file, it calculates the P(k) and writes it into a text file
Created by Julia Poncela, February 2012
"""

import networkx as nx
import math
import sys

def main(name):


    G=nx.read_gml(name) # create the network from the original input file  

    Pk=10000*[0]  # i create a list full of ceros (to keep the degree distribution) 
    Pk_cum=10000*[0]  # i create a list full of ceros (to keep the degree distribution)   
    norma_Pk=0.



    for node in G.nodes():        
        k=len(G.neighbors(node))

        if k==0:
            print node, "k=0"
        Pk[k]+=1 
        norma_Pk +=1.
       

        for i in range(len(Pk)):
            if i <= k:
                Pk_cum[i]+=1.0
        
        


    file1 = open(name.split(".gml")[0]+"_PK.dat",'wt')
    for i in range(len(Pk)):
        if Pk[i] !=0:
            print >> file1, i, Pk[i]/norma_Pk, Pk_cum[i]/norma_Pk
            
    file1.close()




if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
