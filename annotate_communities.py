import networkx as nx
from transform_labels_to_nx import transform_labels_to_nx
import sys, os
from numpy import *
import itertools 

def annotate_communities(G, num_points, filename, communitylist, dbdate = '2010'):
    
    '''
    Created by Rufaro Mukogo on 2011-03-31.
    Copyright (c) 2010 __Northwestern University__. All rights reserved.

    This script takes a GML file and the number of points and reads the a dat file that contains the 
    list of lists for the communties and then annotates the GML file with a community attribute for 
    each node that belongs to a community, the communities are odered from the largest to the smallest
    the identifies is "n_s" where n is the number of the communitiy (zero is the largest) and s is the size of the community
    '''



    for n in G.nodes():  # because the type of the labels or ids in some gml files is diff, and otherwise it gives me an error
       
        G.node[n]['label']=str(G.node[n]['label'])
        G.node[n]['id']=str(G.node[n]['id'])

       

    if dbdate =="2010":
        G = transform_labels_to_nx(G)          
        #open file with the list of communities 
        f = open(str(communitylist)).readlines()       
    else:
        print "You need to generate a gml file that has only 2009 data"
        sys.exit()


  
   
   
    #extract list of communities should return a list of list
    communities = [x.strip().split(";") for x in f]  
   # print communities,"\n"  
    communities  = [x.strip().split(",") for x in communities[0]]
    #print communities,"\n"  
    
    #sort communities
    communities = sorted(communities, key=len, reverse=True) 

    #lisf of all the nodes that are in a community
    com_nodes= itertools.chain(*communities) 

    #convert to integers to avoid key errors
    com_nodes =map(int, list(com_nodes))
    



    for n in G.nodes():
        if n not in com_nodes:
            G.node[n]["community"] = ""  
            #print n
      
    ii = 0
    for co in communities:
        s = str(ii)+"_"+str(len(co))
        #print "community_size", len(co), "s:",s
        for n in co:    
           
              #add attribute to the main GML file     
            n=str(n)        
            G.node[n]["community"] = s
        ii+=1
    nx.write_gml(G,str(filename)+".gml")  
    
    return G
    
if __name__ =="__main__":
    
    if len(sys.argv)>1:
        communitylist = sys.argv[1]
    else:
        print "Enter the name of the list of communities"
    
    if len(sys.argv)>2:
        filename = sys.argv[2]
    else:
        print "Enter the name of the name of the .gml file"
    
    num_points = 5
    M = nx.read_gml(str(filename)+".gml")
    for n in M.nodes():
        M.node[n]["community"] = ""
    
    H = annotate_communities(M,num_points, filename, communitylist)
