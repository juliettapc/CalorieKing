#!/usr/bin/env python
# encoding: utf-8
"""
network-structure-color.py

Created by Satyam Mukherjee on 2011-01-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.

Plot the network with nodes colored according to the total activity of users. One can color them based on weightloss/vitality...etc!
"""

import sys
import os
import networkx as nx
from matplotlib import pyplot
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict
import matplotlib.cm as cm
import numpy as np
import pylab
from copy import copy
from matplotlib.colors import LogNorm
import glob
from matplotlib.numerix import asarray
import networkx_pylab_new as nx1  #### Draw arrows using matplotlib fancyarrow !!!!


def main(graph_name):
#    print "generating plots using " + str(max_hubs) + " hubs"
    G = nx.read_gml(graph_name)
    print len(G.nodes())
#    G = nx.connected_component_subgraphs(G)[0] ### For plotting Giant component ###
#    G = nx.connected_component_subgraphs(G)[0]
    top_nodes = []
    top_nodes.append(G.nodes())
    topn = map(int, G.nodes())
    string_mapping = dict(zip(G.nodes(), map(int, G.nodes())))

    G = nx.relabel_nodes(G, string_mapping)

    H = nx.Graph() #### For undirected graph use H = nx.Graph() and for directed use nx.DiGraph()
    H.add_edges_from(G.edges())
#    print G.edges()
    activity = []
#    nodepos = []
    pos=nx.graphviz_layout(H,prog='neato',args='')
#    pos = nx.spring_layout(H,iterations=100)
    for n in topn:
        nodelabel = G.node[n]['label']
        activity.append(G.node[n]['activity'])
#        nodepos.append(int(nodelabel))
    max_activity = max(activity)

    pop_plus = []
    pop_minus = []
    pop_zero=[]
    pop = []
    size_plus = []
    size_minus = []
    size_zero = []
    nodepos_plus = []
    nodepos_minus = []
    nodepos_zero = []

    for n in topn:
       pop.append((np.log(float(G.node[n]['activity']))/np.log(float(max_activity)))) ### One can change it to log scale too !!!
       size_node = G.node[n]['percentage_weight_change']
       if size_node > 0 :
          size_plus.append(size_node)
          nodepos_plus.append(G.node[n]['id'])
	  pop_plus.append((np.log(float(G.node[n]['activity']))/np.log(float(max_activity))))

       if size_node < 0 :
          size_minus.append(abs(size_node))
          nodepos_minus.append(G.node[n]['id'])
	  pop_minus.append((np.log(float(G.node[n]['activity']))/np.log(float(max_activity))))

       if size_node == 0 :
          size_zero.append(abs(size_node))
          nodepos_zero.append(G.node[n]['id'])
	  pop_zero.append((np.log(float(G.node[n]['activity']))/np.log(float(max_activity))))

#    print size_minus, size_plus

    colors_plus = []
    for rank_plus in pop_plus:
       colors_plus.append(plot.cm.jet(float(rank_plus)))

    colors_minus = []
    for rank_minus in pop_minus:
       colors_minus.append(plot.cm.jet(float(rank_minus)))

    colors_zero = []
    for rank_zero in pop_zero:
       colors_zero.append(plot.cm.jet(float(rank_zero)))


   
   
    fig = plot.figure(figsize=(11,11))
    ax = fig.add_axes((0.0,0.0,1.0,1.0))

    cax = ax.imshow([activity],cmap=cm.jet,norm=LogNorm(vmin=1, vmax=max_activity))

#    cax = ax.imshow([activity],cmap=cm.jet)
#    nx.draw(H,pos,node_color=colors,node_shape='o',node_size = size_minus, with_labels=False)


#    nx1.draw_networkx_nodes(H,pos,nodelist=None,node_size = 300, node_shape = 'o', node_color=colors, cmap=plot.cm.jet)
                      
    nx1.draw_networkx_nodes(H,pos,nodelist=None,node_size = size_plus, node_shape = 's', node_color=colors_plus, cmap=plot.cm.jet)

    nx1.draw_networkx_nodes(H,pos,nodelist=None,node_size = size_minus, node_shape = 'o', node_color=colors_minus, cmap=plot.cm.jet)

    nx1.draw_networkx_nodes(H,pos,nodelist=None,node_size = size_minus, node_shape = 'o', node_color=colors_zero, cmap=plot.cm.jet)

    nx1.draw_networkx_edges(H,pos,edgelist=None,edge_color='k',style='solid',alpha=0.4)

#    nx1.draw_networkx_labels(H,pos,labels=None,font_size=10) ### For labeling the nodes with uid


#    formatter=ticker.LogFormatterMathtext()
    #colorbar(format=formatter)

    plot.rcParams["font.size"] = 12
    c=plot.colorbar(cax,orientation='vertical',shrink = 0.75)
    
    c.set_label("Total Activity of Users")
    pyplot.title('Percentage weight-loss (circle) and Normalized weight-gain (square)')
    pyplot.axis('off')
    pyplot.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
    if len(sys.argv) > 2:
        max_hubs = int(sys.argv[2])
    else:
        max_hubs = None

    main(graph_filename)

    
