#!/usr/bin/env python

import networkx as nx
import numpy
import sys
import networkx as nx
from matplotlib import pyplot as plt
from pylab import *
import matplotlib

def compute_degree(G):
    
    degree = G.degree()    
    
    return degree

def compute_closeness(G):
    
    closeness = nx.closeness_centrality(G) 
        
    return closeness

def compute_betweenness(G):
    
    betweenness = nx.betweenness_centrality(G)  
     
    return betweenness
     
def strip_file_name(graph_filename):
    
    header_name = graph_filename.split('_')[-1] 
    header_name = 'undiredcted_giant_'+str(header_name.split('.')[0])
    
    return header_name
    
def main(graph_filename, cut_off):
    
    try:
        G = nx.read_gml(graph_filename)
    except IOError:
        pass
    #G = nx.connected_component_subgraphs(G)

    #G = G[0]

    # compute network metrics
    degree = compute_degree(G)
    closeness = compute_closeness(G)
    betweenness = compute_betweenness(G)

    #extract values from dictionaries
    degree_values = map(float,list(degree.values()))
    closeness_values = map(float, closeness.values())
    betweenness_values = map(float, betweenness.values())
    
    n_bins = max(degree_values)
    header_name = strip_file_name(graph_filename)
    
    try:
        f = open(str(path)+'degree_for_'+str(cut_off)+'_'+str(header_name)+'.dat', 'w') 
        g = open(str(path)+'betweenness_for_'+str(cut_off)+'_'+str(header_name)+'.dat', 'w')
        h = open(str(path)+'closeness_for_'+str(cut_off)+'_'+str(header_name)+'.dat', 'w')
    except IOError:
        pass
    

    keys = degree.keys()

    for d in keys:
        print >> f,"%s,%s" %(d,degree[d])
   
    for b in betweenness:
         print >> g,"%s,%s" %(b,betweenness[b])

    for c in closeness:
        print >> h,"%s,%s" %(c,closeness[c])

    f.close()
    g.close()
    h.close()

    #plot histograms
    figure(1) 
    plt.hist(degree_values, n_bins,normed = 0, facecolor='blue')
    plt.xlabel('degree (k)')
    plt.ylabel('N(k)')
    plt.title('degree distribution for'+' '+str(header_name)+'_'+str(cut_off)+'_points')
    ax=gca()
    ax.autoscale_view()
    #plt.axis([0, 200, 0, 500])
    plt.grid(True)   
    plt.savefig(str(path)+'degree_distribution_'+str(cut_off)+'_points_'+str(header_name)+'.eps', dpi=100)
    
    figure(2)
    plt.hist(betweenness_values, bins=50,normed = 0, facecolor='blue') 
    plt.xlabel('betweenness (b)')
    plt.ylabel('N(b)')
    plt.title('betweenness distribution for'+' '+str(header_name)+'_'+str(cut_off)+'_points')
    ax = gca()    
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(path)+'betweenness_distribution_'+str(cut_off)+'_points_'+str(header_name)+'.eps', dpi=100)
    
    figure(3)    
    plt.hist(closeness_values, bins = 50,normed = 0, facecolor='blue')
    plt.xlabel('closeness (c)')
    plt.ylabel('N(c)')
    plt.title('closeness distribution for'+' '+str(header_name)+'_'+str(cut_off)+'_points') 
    ax = gca()    
    ax.autoscale_view()
    #plt.axis([0,.25,0,1])
    plt.grid(True)
    plt.savefig(str(path)+'closeness_distribution_'+str(cut_off)+'_points_'+str(header_name)+'.eps', dpi=100)
        
    plt.show()

if __name__ == '__main__':
    try:
        import psyco
    except ImportError:
        pass
        
    if len(sys.argv) >= 2:
        cut_off = sys.argv[1]
    else:
        print "Usage: generate_plot_of_degree_distribution"
        
    path = '/home/staff/rmukogo/calorie_king_hg/'+str(cut_off)+'_points_network/'
    graph_filename = 'calorie_king_friends_undirected_giant_all0.gml'


    main(path+graph_filename,cut_off) 
    

     
