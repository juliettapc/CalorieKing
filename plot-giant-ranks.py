#!/usr/bin/env python
# encoding: utf-8
"""
plot-giant-ranks.py

Created by Satyam Mukherjee on 2011-01-18. Animation for growth of giant component.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
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
import CKActivityMetrics as ck

def main(graph_name, max_hubs):
    print "generating plots using " + str(max_hubs) + " hubs"
    G = nx.read_gml(graph_name)
 
    top_nodes = []
    top_nodes.append(G.nodes())
    topn = map(int, G.nodes())
    string_mapping = dict(zip(G.nodes(), map(int, G.nodes())))

    G = nx.relabel_nodes(G, string_mapping)
#    nodepos = []
    activity = []
    for n in topn:
 
#        print "Activity", G.node[n]['activity'],G.node[n]['label']      
        nodelabel = G.node[n]['label']
        activity.append(int(G.node[n]['activity']))
#        nodepos.append(int(nodelabel))
    max_activity = max(activity)
    print activity
    print "Maximum Activity", max_activity


    #get the giant component
    G2 = nx.connected_component_subgraphs(G)[0]
    #compute betweenness centrality for nodes
    betweenness_dictionary = nx.betweenness_centrality(G2)

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

    hubs_added = 0
    giant_length = len(G2)
#    pp = PdfPages('growth_with_hubs.pdf')


#    layout=nx.pygraphviz_layout(G2,prog='twopi',args='')
    layout = nx.spring_layout(G,iterations=50)
    pop_act = []
    
    pop = []
    for i in range(len(ordered_betweenness)-1,-1,-1):
        if hubs_added > max_hubs:
#            pp.close()
            exit()
       
        nodepos = []
         
        
        for node in betweenness_lookup[ordered_betweenness[i]]:
            #get the bunch of nodes connected to this neighbor
            bunch = [node]+G.neighbors(node)
#            print bunch, layout.keys()
            Gprime = G.subgraph(bunch)
            H.add_edges_from(Gprime.edges())
            hubs_added +=1
            percent_giant = len(H)/float(len(G))
            num_components = nx.number_connected_components(H)
            outfilename = hubs_added
#            print "hubs added", outfilename
#            layout=nx.pygraphviz_layout(H,prog='neato',args='')
            
            for n in bunch :
#                print G.node[n]['label'], G.node[n]['activity']
                nodelabel = G.node[n]['id']
#                nodepos.append(int(nodelabel))
                pop.append((nodelabel,(np.log(float(G.node[n]['activity']))/np.log(float(max_activity)))))
                pop_act.append(float(G.node[n]['activity']))
             #   pop.sort()
            no_dups = list(set(pop))
            no_dups.sort()
            edgelist = []

         #   edgelist.append(G.edges())

            colors = [] 

            for uid, rank in no_dups:
#                print rank
                colors.append(plot.cm.jet(float(rank)))
                nodepos.append(uid)
         
#            nx.draw(G,pos=layout,nodelist=nodepos,edgelist=edgelist,node_color=colors,with_labels=True)


  	    nx.draw_networkx_edges(H,layout,edge_color='k',alpha=0.65)
                     
	    nx.draw_networkx_nodes(H,layout,nodelist=nodepos,node_size=100,node_color=colors,cmap=plot.cm.jet)

#	    nx.draw_networkx_labels(H,layout,labels=None)
	    plot.axis('off')
#	    pyplot.draw()
            print str(int(1.0*1./ordered_betweenness[i]))+'-bc.png'
            pyplot.savefig(str(int(1.0*1./ordered_betweenness[i]))+'-bc.png')
            pyplot.close()
        os.system('./genmovie')
#        for label, act in no_dups :
#           print label, act

#        print colors
 

#            cax = pylab.imshow([maxval],cmap=cm.jet)

#  	    nx.draw_networkx_edges(H,layout,edge_color='k',alpha=0.65)
                     
#	    nx.draw_networkx_nodes(H,layout,node_color=colors,cmap=cm.YlOrRd)

#	    nx.draw_networkx_labels(H,layout,labels=None)

#            formatter=ticker.LogFormatterMathtext()
#            plot.colorbar(format=formatter)

#            plot.rcParams["font.size"] = 12
#            cb=plot.colorbar(cax,orientation='horizontal')
           
#            cb.set_label("Total Activity of Users")


#            plot.axis('off')
#            pyplot.draw()
#            plot.title("Nodes connected with minimum hub betweenness "+str(ordered_betweenness[i]))
#            pyplot.savefig(str(int(1.0*1./ordered_betweenness[i]))+'-bc-color_act.png')
#            pyplot.close()
#        os.system('./genmovie')
        

   
 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
    if len(sys.argv) > 2:
        max_hubs = int(sys.argv[2])
    else:
        max_hubs = None

    main(graph_filename, max_hubs)

    
