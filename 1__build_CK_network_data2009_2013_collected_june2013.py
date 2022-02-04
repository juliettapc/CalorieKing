#!/usr/bin/env python


'''
Code to build the CK network from the database

Created by Julia Poncela, on April 8th, 2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
import datetime
from database import *   #package to handle databases


def main():
 


    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 

## G = nx.read_gml(graph_name)
   
    G=nx.Graph()
 
    graph_filename="../Results/Networks/Network2009_2012.gml"

    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict. 

    dict_ck_id_label={}
    dict_label_ck_id={}
    dict_master_user_info={}
    list_users=[]  
    for r1 in result1:
        ck_id=str(r1['ck_id'])       # i dont need to do this for everyone, i should first get only the networked people!!
        prior2009= r1['act_prior2009']

        if prior2009 =="NO":
            dict_master_user_info[ck_id]={}
            
            dict_master_user_info[ck_id]['ck_id'] =str(r1['ck_id'])
            dict_master_user_info[ck_id]['label']=r1['id']
            dict_master_user_info[ck_id]['prior2009']=r1['act_prior2009']
            dict_master_user_info[ck_id]['initial_weight']=r1['initial_weight']
            dict_master_user_info[ck_id]['final_weight']=r1['most_recent_weight']
            dict_master_user_info[ck_id]['weight_change']=r1['most_recent_weight']-r1['initial_weight']
            dict_master_user_info[ck_id]['percentage_weight_change']=(r1['most_recent_weight']-r1['initial_weight'])*100./r1['initial_weight']



            dict_master_user_info[ck_id]['height']=r1['height']
            dict_master_user_info[ck_id]['age']=r1['age']            
            dict_master_user_info[ck_id]['gender']=r1['gender']
            
       
            list_users.append(ck_id)
            dict_ck_id_label[ck_id]=r1['id']
            dict_label_ck_id[r1['id']]=ck_id


    print "tot # users:",len(list_users)
   
    list_networked_labels=[]
    cont=0
    for ck_id in list_users:       
        cont +=1
        print cont

        query2=" select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"') "    # because there are friends that are not in the users table
        result2 = db.query(query2)  # is a list of dicts.   
  
           # there are DUPLICATE friendships  but networkx ignores duplicate links and duplicate nodes

        for r2 in result2:
            src=str(r2['src'])
            dest=str(r2['dest'])          

            if src != dest:   # ignore self-loops
                if (src in list_users) and (dest in list_users):  # friendships only between members who join after 2009, not with older ones                  

                    src_label=dict_ck_id_label[src]
                    dest_label=dict_ck_id_label[dest]
                    
                  #  if src_label not in list_networked_labels:   # just doublechecking
                   #     list_networked_labels.append(src_label)
                    #if  dest_label not in list_networked_labels:
                     #   list_networked_labels.append(dest_label)

                    G.add_node(src_label)  #if the node or link already exists in the network, nothing happens
                    G.add_node(dest_label)

                    G.add_edge(src_label,dest_label)



    print "tot num. friendships",len(G.edges()), " among:",len(G.nodes()),"users."#,len(list_networked_labels)

    G_GC = nx.connected_component_subgraphs(G)[0]

    print "   GC size:", len(G_GC.nodes())

    for node in G.nodes():   # nodes are labels
        ck_id=dict_label_ck_id[node]

        G.node[node]['ck_id']=ck_id
        G.node[node]['initial_weight']= dict_master_user_info[ck_id]['initial_weight']
        G.node[node]['final_weight']= dict_master_user_info[ck_id]['final_weight']

        G.node[node]['height']= dict_master_user_info[ck_id]['height']
        G.node[node]['initial_bmi']= float(G.node[node]['initial_weight'])/( float(dict_master_user_info[ck_id]['height'])*float(dict_master_user_info[ck_id]['height']) ) *703.
        G.node[node]['final_bmi']= float(G.node[node]['final_weight'])/( float(dict_master_user_info[ck_id]['height'])*float(dict_master_user_info[ck_id]['height']) ) *703.

       
        
        G.node[node]['weight_change']= dict_master_user_info[ck_id]['weight_change']
        G.node[node]['percentage_weight_change']=dict_master_user_info[ck_id]['percentage_weight_change']
       
        G.node[node]['age']= dict_master_user_info[ck_id]['age']
        G.node[node]['gender']=dict_master_user_info[ck_id]['gender']

        G.node[node]['degree']=len(G.neighbors(node))




    nx.write_gml(G,graph_filename)

    print "\nwritten network file:" , graph_filename


##################################################
######################################
if __name__ == '__main__':
 #   if len(sys.argv) > 1:
  #      filename = sys.argv[1]
   
        main()
   # else:
    #    print "Usage: python script.py path/filename"

    
