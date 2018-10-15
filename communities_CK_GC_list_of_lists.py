#! /usr/bin/env python
"""
Created by Julia Poncela on March 2011.


Given an edgelist, it returns a list of lists, corresponding to Roger's
community analysis. 

"""

import subprocess as sp
import networkx as nx
import sys

def main(input_file_name):

    name=input_file_name                        
    edge_data = open(name).readlines()

    H=nx.read_edgelist(name) # create the network from the original input file  
    components=nx.connected_component_subgraphs(H)     
    G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]

    new_edge_data = [] #this list is what i will pass to Roger's code
    for e in G.edges(): # e is a list of two neighbors: [n1,n2]
                        #i have to convert e to str because it is in some other format and the algorithm may not recognise it
             
        new_edge_data.append(" ".join(map(str,e))) # i join the two neighbors, separating them just by a space, so now they are just one element of the edge_list, which is: [n1 n2, n3 n4, n2 n3,...]   

    p = sp.Popen(["/opt/communityID"], stdin=sp.PIPE, stdout=sp.PIPE)
    output, error = p.communicate("\n".join(new_edge_data))
    community_lines = output.split("part")
    modularity = float(community_lines[0])
    partition_lines = community_lines[1].split("\n")
    modules = []

    for p in partition_lines:
        this_module = p.split("---")         
        if len(this_module) > 1:
            this_module = this_module[1] # 'this_module' is the list of nodes in the current module
            this_module = map(int, this_module.split())
            modules.append(this_module) # list of modules (list of lists)
    
    return modules
               
if __name__== "__main__":pass
    
    
    #if len(sys.argv)>1:
    #    input_file_name=sys.argv[1]   
    
    #    main(input_file_name)

    #else:
    #    print "Usage: python program_name path/edgelist_file_name"
