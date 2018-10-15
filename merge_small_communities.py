#! /usr/bin/env python

"""
Created by Julia Poncela, April 2011.

Given a .gml file with a node attribute communitylabel_size 
(obtain with some community analysis algorithm), merge the too small 
communities into the larger ones, so the final structure will be easier to plot.

"""

import networkx as nx
import math
import sys
import math
from pylab import *
import numpy
from transform_labels_to_nx import *



#Modularity=0.391  # value for the actual network, to be compare with the merging versions


def main (graph_name):


    H=nx.read_gml(graph_name) # i create the network from the original input file  

    H = transform_labels_to_nx(H)  #transform, so G.nodes() is a list of label, not ids!
    components=nx.connected_component_subgraphs(H)     
    G=components[0] #  i take just the GC as a subgraph to perform the community ID algorithm


#5_points_network_2010/data/friend_graph_all.gml
   
    num_moved_nodes=0
    list_nodes_to_merge=[]
    list_small_comm_index=[]

    #dir=graph_name.split('friends')[0]
    #dir=graph_name.split('master')[0]
    #dir=graph_name.split('method3_')[0]
    dir=graph_name.split('network_')[0]





    file = open(dir+"original_comm_idexes",'wt')
    for node in G.nodes():   #G is GC    
              
        community_index=int(G.node[node]['community'].split('_')[0])
        community_size=int(G.node[node]['community'].split('_')[1])


        G.node[node]['community_index']=community_index
        G.node[node]['aux_comm_index']=G.node[node]['community_index']  #to be modified when trying to merge


        print >> file, node, community_index

        
        if community_size < 10:  # i set this threshold
            list_nodes_to_merge.append(node)

            if community_index not in  list_small_comm_index:
                list_small_comm_index.append(community_index)
          

    file.close()



    print "initial_mod:",Modularity(G)

    #actual_mod=Modularity(G)
    #print "actual modularity:",actual_mod
   




    list_of_list_small_comm=[]
    for index in list_small_comm_index:
        list=[]
        for node in  list_nodes_to_merge:
            if G.node[node]['community_index']==index:
                list.append(node)
        list_of_list_small_comm.append(list)


    print "list of lists of small communities",list_of_list_small_comm





    num_loner_comm=0
    list_nodes_to_deal_at_the_end=[]
   
    for small_comm in list_of_list_small_comm:  # i go over every small community
       
       
        posible_target_comm=[]  #list of all communities the nodes 
                               #  in that small comm are conected to
        loner_nodes=[]
        for node in small_comm:
            for neighbor in G.neighbors(node):

                if (G.node[neighbor]['community_index'] not in posible_target_comm) and (G.node[neighbor]['community_index'] not in list_small_comm_index):

                    posible_target_comm.append(G.node[neighbor]['community_index'])
                 
                


              # LA EXCEPCION DE QUE UNA COMM. PEQ SOLO ESTE UNIDA A OTRA TB PEQ!!!
        if len(posible_target_comm) == 0:
            print "communidad de loners!:", small_comm
            for node in small_comm:
                list_nodes_to_deal_at_the_end.append(node)
            num_loner_comm=num_loner_comm+1
          



     # i reasign nodes of the current small comm. to different one:      
        if len(posible_target_comm)>1:         
            for node in small_comm:               
                dict_mod={}
                list_mod=[]
                for comm_index in posible_target_comm:
                    G.node[node]['aux_comm_index']=comm_index
                    mod=Modularity(G) #i calculate M with the 'aux_comm_index' of the nodes
                   
                    list_mod.append(mod)
                    dict_mod[mod]=comm_index
                  
                
                max_mod=max(list_mod)                
                index=dict_mod[max_mod]

                G.node[node]['community_index']=dict_mod[mod] #move the node!
                G.node[node]['aux_comm_index']=dict_mod[mod] #move the node!
              
                num_moved_nodes=num_moved_nodes+1
                list_nodes_to_merge.remove(node)

              
                #print "max:",actual_mod,"so node",node, "goes to", G.node[node]['community_index']
               

        elif  len(posible_target_comm)==1:  # if there is only one option for the nodes to merge 
            for node in small_comm:
                G.node[node]['community_index']=posible_target_comm[0]
                G.node[node]['aux_comm_index']=posible_target_comm[0]
                num_moved_nodes=num_moved_nodes+1
                list_nodes_to_merge.remove(node)

             #print "no choice, so node",node, "goes to", posible_target_comm[0]

            
                
       




    posible_target_comm=[]
    for node in list_nodes_to_deal_at_the_end:
        for neighbor in G.neighbors(node):
            if (G.node[node]['community_index'] != G.node[neighbor]['community_index']):
                posible_target_comm.append(G.node[neighbor]['community_index'])  # if there are several options, it will overwrite!!!

           

  

    for node in list_nodes_to_deal_at_the_end:
        G.node[node]['community_index']=posible_target_comm[0]
        G.node[node]['aux_comm_index']=posible_target_comm[0]
        num_moved_nodes=num_moved_nodes+1
        list_nodes_to_merge.remove(node)
  




    file = open(dir+"final_comm_idexes",'wt')
    current_list_comm=[]
    for node in G.nodes():        
        print >> file, node, G.node[node]['community_index'] 
        if G.node[node]['community_index'] not in current_list_comm:
            current_list_comm.append(G.node[node]['community_index'])
    file.close()



    list_of_lists=[]
    for s in current_list_comm:
        list=[]
        for node in G.nodes():
            if G.node[node]['community_index']==s:
                list.append(G.node[node]['label']) #node)  ##list of list with labels, not ids!!
            
        list_of_lists.append(list)

    name=graph_name.split('.gml')[0]
    #name=name.split('data/')[1]
    #file = open(dir+name+"list_of_lists_merged_communities",'wt')
    file = open(name+"_list_of_lists_merged_communities",'wt')
    print >> file, list_of_lists
    file.close()
    



    element=[]
    for list in list_of_lists:
        element.append(",".join(map(str,list)))

        #print element
    string=";".join(map(str,element))
    #print string
    
    file = open(name+"_list_of_lists_merged_communities_csv",'wt') 
    print >> file, string 
    file.close()




    for n in G.nodes():
        G.node[n]['community']=G.node[node]['community_index'] 
    

    nx.write_gml(G,name+"_merged_small_comm.gml")

  
    print  list_nodes_to_merge
    print "\n\n final comm count:\n",len(list_of_lists)

    print "final_mod:",Modularity(G)






#################################
########################################
def Modularity(G):


    current_list_comm=[]
    for node in G.nodes():
        if G.node[node]['aux_comm_index'] not in current_list_comm:
            current_list_comm.append(G.node[node]['aux_comm_index'])


    number_comm=len (current_list_comm)
    L=float(len(G.edges()))

    list_of_lists=[]
    for s in current_list_comm:
        list=[]
        for node in G.nodes():
            if G.node[node]['aux_comm_index']==s:
                list.append(node)
            
        list_of_lists.append(list)



    mod=0.0
            
    for comm in list_of_lists:
        
        Subg=G.subgraph(comm)

        l_s=float(len(Subg.edges())) #number of links among the community

        d_s=0.0
        for node in comm:
            d_s=d_s+float(len(G.neighbors(node)))


        mod=mod+ l_s/L - (d_s/(2.0*L))*(d_s/(2.0*L))





    return mod  #0.391  # this will be the actual value that i obtain



############################################3
if __name__== "__main__":
    if len(sys.argv)>1:
        graph_name=sys.argv[1]   
    
        main(graph_name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
