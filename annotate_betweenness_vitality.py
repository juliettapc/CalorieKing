#! /usr/bin/env python


"""
Created by Julia Poncela, June 2011

Given a .gml graph, it reads it and annotates it with betweenness and vitality for the nodes.

"""





import networkx as nx
import math
import sys




def main (name):


    dir=name.split('master')[0]


    H=nx.read_gml(name) # create the network from the original input file  

# al leer la red de un .gml, los nodos tiene atributos: label, activity, community,...



    dicc_betweenness=nx.algorithms.centrality.betweenness_centrality(H, normalized=True)
      

    dicc_vitality=nx.algorithms.vitality.closeness_vitality(H)


    for i in range(len(dicc_betweenness)):

        H.node[i]["betweenness"]=float(dicc_betweenness[i])
        H.node[i]["vitality"]=float(dicc_vitality[i])

        print i,dicc_betweenness[i],dicc_vitality[i]


    name=name.split('.')
    name=name[0]   #  remove the extension of the filename

    nx.write_gml(H,name)#+"betw.gml")




############################
if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
