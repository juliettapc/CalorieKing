import networkx as nx
from transform_labels_to_nx import transform_labels_to_nx
import sys, os
from numpy import *
import itertools 

def annotate_communities(G, num_points,q, period, dbdate = '2010'):
    
    '''
    Created by Rufaro Mukogo on 2011-03-31.
    Copyright (c) 2010 __Northwestern University__. All rights reserved.

    This script takes a GML file and the number of points and reads the a dat file that contains the 
    list of lists for the communties and then annotates the GML file with a community attribute for 
    each node that belongs to a community, the communities are odered from the largest to the smallest
    the identifies is "n_s" where n is the number of the communitiy (zero is the largest) and s is the size of the community
    '''

    if dbdate =="2010":
        G = nx.read_gml("./"+str(num_points)+"_points_network_2010/data/new_networks/friends_undirected_all_"+str(period)+str(q)+".gml")  
        G = transform_labels_to_nx(G)
        #open file with the list of communities
        f = open("./"+str(num_points)+"_points_network_2010/data/new_networks/friends_undirected_all_"+str(period)+str(q)+"_list_of_communities_csv").readlines()
  
    else:
        print "you are not including 2010 data: use another script"
        sys.exit()

    #extra list of communities should return a list of list
    communities = [x.strip().split(";") for x in f]    
    communities  = [x.strip().split(",") for x in communities[0]]
    
    #sort communities from largest to smallest
    communities = sorted(communities, key=len, reverse=True) 

    #lisf of all the nodes that are in a community
    com_nodes= itertools.chain(*communities)

    #convert keys to ints, the int/string convention somtimes causes KeyErrors
    com_nodes =map(int, list(com_nodes))
    
    for n in G.nodes():
        print n
        if n not in com_nodes:
            G.node[n]["community"] = ""

    ii = 0
    for co in communities:
        s = str(ii)+"_"+str(len(co))
        for n in co:    
              #add attribute to the main GML file  
            G.node[int(n)]["community"] = s
        ii+=1
    nx.write_gml(G,"./"+str(num_points)+"_points_network_2010/data/new_networks/6months/friends_graph_"+str(period)+str(q)+"_comm.gml")  
    
    return G
    
if __name__ =="__main__":
    
    try:
        import pyscho
        psycho.ful()
    except ImportError:
        pass

    if len(sys.argv) >1:
        num_points = sys.argv[1]
    else:
        num_points = 5

    if len(sys.argv) >2:
        period = sys.argv[2]
    else:
        period = "sixmonths"
    
    if period =="sixmonths":
        r = 4
    elif period =="quarters":
        r = 8
    else:
        print "invalid period"
        sys.exit()

    for q in range(4):
        M = nx.read_gml("./"+str(num_points)+"_points_network_2010/data/new_networks/friends_undirected_all_"+str(period)+str(q)+".gml")
        H = annotate_communities(G=M,q=q,num_points=num_points, period=period)
  
