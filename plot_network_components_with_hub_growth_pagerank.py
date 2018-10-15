#!/usr/bin/env python
# encoding: utf-8
"""
plot_network_components_with_hub_growth_pagrank.py

Created by Daniel McClary on 2011-01-11. Modified by Satyam Mukherjee for the pagerank
Copyright (c) 2011 __Northwestern University__. All rights reserved.

"""

import sys
import os
import networkx as nx
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict

def main(graph_name, max_hubs):
    print "generating plots using " + str(max_hubs) + " hubs"
    G = nx.read_edgelist(graph_name)
    #get the giant component
#    G = nx.connected_component_subgraphs(G)[0]

    #compute pagerank for nodes
    pagerank_dictionary = nx.pagerank(G,alpha=0.85)
    
    pagerank_lookup = defaultdict(list)
    ordered_pagerank = []
    for key in pagerank_dictionary:
        ordered_pagerank.append(pagerank_dictionary[key])
        pagerank_lookup[pagerank_dictionary[key]].append(key)
    
    ordered_pagerank.sort()
    if not max_hubs:
        max_hubs = len(set(ordered_pagerank))
    #iterate through the betweenness values plotting the graph at each step
    # H: the initially blank graph we're building up
    H = nx.Graph()
    f = open("component_growth_with_hubs_pagerank.dat", "w")
    print >> f, '"hubs added","minimum hub betweenness","number of components", "percent of giant"'
    hubs_added = 0
    giant_length = len(G)
    layout=nx.spring_layout(G)
    pp = PdfPages('growth_with_hubs_pagerank.pdf')
    for i in range(len(ordered_pagerank)-1,-1,-1):
        if hubs_added > max_hubs:
            pp.close()
            f.close()
            exit()

        for node in pagerank_lookup[ordered_pagerank[i]]:
            #get the bunch of nodes connected to this neighbor
            bunch = [node]+G.neighbors(node)
            Gprime = G.subgraph(bunch)
            H.add_edges_from(Gprime.edges())
            hubs_added +=1
            percent_giant = len(H)/float(len(G))
            num_components = nx.number_connected_components(H)
            print >> f, ",".join(map(str,[hubs_added, ordered_pagerank[i], percent_giant, num_components]))
            fig = pyplot.figure()
            ax = fig.add_subplot(111)
            nx.draw(H,pos=layout,with_labels = False)
            pyplot.draw()
            ax.set_title("Nodes connected with minimum hub pagerank "+str(ordered_pagerank[i]))
            pp.savefig()
            
    f.close()
    pp.close()
    

        
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
    if len(sys.argv) > 2:
        max_hubs = int(sys.argv[2])
    else:
        max_hubs = None
    main(graph_filename, max_hubs)

