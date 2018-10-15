from operator import itemgetter
import sys
from CKActivityMetrics import *

"""
identification_of_most_central_active_nodes.py

Created by Rufaro Mukogo on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script returns a list of user IDs for users who are simultaneously in the top nth bracket for both activity and degree.
The results are printed to txt files that can be processed accordingly
"""

def main(num_points,cut_off,path,cf,gf):
    """
    this function compares the set of the top n most active and central actors (defined by degree) and returns a list of their uids
    to a text file
    """
    
    graph_file = "friend_graph_all0.gml"


    full_path = str(path)+str(num_points)+"_points_network/data/"
     
    G = nx.read_gml(full_path+graph_file)

    string_mapping = dict(zip(G.nodes(), map(str, G.nodes())))
    G = nx.relabel_nodes(G, string_mapping)
    
    all_nodes_set = set(G.nodes())

    f = open(str(path)+str(num_points)+'_points_network/data/'+str(num_points)+'_points_top'+str(cut_off)+'_cam_summary.csv','r').readlines()[1:]
	
    h = open(str(path)+str(num_points)+'_points_network/data/top_'+str(cut_off)+'_highest_degree_and_activity_nodes.txt','w')
	
    top_degree_nodes_set = set([x.split(',')[3] for x in f])
    top_activity_nodes_set = set([x.split(',')[18] for x in f])
    top_weight_loss_nodes_set = set([x.split(',')[9] for x in f])

    print "top weight nodes", top_weight_loss_nodes_set
    	
    print>>h, "nodes belonging to both most connected (highest degree) and activity ( activity excluding weigh_ins) but not  in the set of top%d for weight loss for %d cut_off" %(cut_off, cut_off)
	
    for item in list(top_weight_loss_nodes_set&(all_nodes_set-(top_degree_nodes_set&top_activity_nodes_set))):
        print>>h,item
  
    h.close()
    

if __name__ == '__main__':
	
    if len(sys.argv) > 1:
        num_points = int(sys.argv[1])
    else:
        num_points = 5
    
    if len(sys.argv) > 2:
        cut_off = int(sys.argv[2])
    else:
    	cut_off = 100
    	
    if len(sys.argv) >3:
    	path = sys.argv[3]
    else:
		path = os.getcwd()+"/"

    gf = str(path)+str(num_points)+'_points_network/data/friend_graph_all0.gml'
      
    cf = str(path)+str(num_points)+'_points_network/data/'+str(num_points)+'_points_since_2009_all_weigh_ins.dat'
   
    for cut_off in [10,25,50]:
        main(num_points=num_points, cut_off=cut_off, path=path,cf=cf,gf=gf)
