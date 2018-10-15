#!/usr/bin/env python
# encoding: utf-8
"""
plot_network_components_with_hub_growth.py

Created by Daniel McClary on 2011-01-11.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

A quick script to plot the growth of a network as it the nodes with greatest betweenness (and their one-hop neighbors) are added one-by-one.
A CSV file tracking the growth of the network and its components is also generated.
"""

import sys
import os
import networkx as nx
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict
import matplotlib.pyplot as plot

def main(graph_name, max_hubs):
    print "generating plots using " + str(max_hubs) + " hubs"
    G = nx.read_edgelist(graph_name)
    #get the giant component
    G = nx.connected_component_subgraphs(G)[0]

    #compute betweenness centrality for nodes
    betweenness_dictionary = nx.betweenness_centrality(G)
    #we can't guarantee unique betweenness, so use a hash which allows collisions
    betweenness_lookup = defaultdict(list)
    ordered_betweenness = []
    for key in betweenness_dictionary:
        ordered_betweenness.append(betweenness_dictionary[key])
        betweenness_lookup[betweenness_dictionary[key]].append(key)
    
    ordered_betweenness.sort()
    if not max_hubs:
        max_hubs = len(set(ordered_betweenness))
    #iterate through the betweenness values plotting the graph at each step
    # H: the initially blank graph we're building up
    H = nx.Graph()
    f = open("component_growth_with_hubs_betweenness.dat", "w")
    print >> f, '"hubs added","minimum hub betweenness","number of components", "percent of giant"'
    hubs_added = 0
    giant_length = len(G)
    layout=nx.graphviz_layout(G,prog='neato',args='')
#    pp = PdfPages('growth_with_hubs_betweenness.pdf')
    for i in range(len(ordered_betweenness)-1,-1,-1):
        if hubs_added > max_hubs:
#            pp.close()
            f.close()
            exit()

        for node in betweenness_lookup[ordered_betweenness[i]]:
            #get the bunch of nodes connected to this neighbor
            bunch = [node]+G.neighbors(node)
            Gprime = G.subgraph(bunch)
            H.add_edges_from(Gprime.edges())
            hubs_added +=1
            percent_giant = len(H)/float(len(G))
            num_components = nx.number_connected_components(H)
            print >> f, ",".join(map(str,[hubs_added, ordered_betweenness[i], percent_giant, num_components]))
#            fig = pyplot.figure()
#            ax = fig.add_subplot(111)
            plot.axis('off')
            nx.draw(H,pos=layout,with_labels=False)
            pyplot.draw()
            plot.title("Nodes connected with minimum hub betweenness "+str(ordered_betweenness[i]))
#            pp.savefig()
            pyplot.savefig(str(int(1.0*1./ordered_betweenness[i]))+'-bc.png')
            pyplot.close()
        os.system('./genmovie')
            
    f.close()
#    pp.close()
    

        
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
    if len(sys.argv) > 2:
        max_hubs = int(sys.argv[2])
    else:
        max_hubs = None
    main(graph_filename, max_hubs)

