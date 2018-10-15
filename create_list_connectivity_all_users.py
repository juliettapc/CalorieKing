#! /usr/bin/env python

"""
Created by Julia Poncela, May 2011

Given the  1_points_network_2010/data/friend_graph_all_1_2010.gmla and the CK database, 
it creates a list of user-connectivity for everyone.

"""




import networkx as nx
import sys
import os
from database import *  


def main ():

    name_network='1_points_network_2010/data/friend_graph_all_1_2010.gml'
    dir=name_network.split('friend')[0]   

    G=nx.read_gml(name_network)

   


    database = "calorie_king_social_networking"
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd)
 
    query="""select distinct ck_id, id from users"""
    result = db.query(query) #[{'ck_id': ,'id': },{'ck_id': ,'id': },{... },...]



    dict_gml={}
    dict_database={}

    list_all_network_ids=[]
    list_all_network_labels=[]
    for node in G.nodes():
        list_all_network_ids.append(G.node[node]['id'])  # gml ids!!!!
        list_all_network_labels.append(G.node[node]['label'])  # database ids!!!!

        label=G.node[node]['label']
        dict_gml[label]=G.node[node]['id']  


    #print list_all_network_labels



    list_all_CKids=[]   
    list_all_network_CKids=[]
    list_all_database_ids=[] #== label gml ids!!!

    for r in result:

        ck_id=r['ck_id']
        id=r['id']
        dict_database[id]=ck_id


        list_all_CKids.append(r['ck_id'])
        list_all_database_ids.append(r['id']) # database ids!!!! == label gml ids!!!

        if r['id'] in list_all_network_labels:
            list_all_network_CKids.append(r['ck_id'])





    file = open(dir+'list_CK_users_connectivities','wt')     
    for index in list_all_database_ids: # database ids!!!!  (== label gml ids)
        if index in list_all_network_labels:
            node=dict_gml[index]  # i get the gml id
            print >> file, index, dict_database[id], len(G.neighbors(node))   # id according to the gml file, not the user database!!!
        else:
            print >> file, index, dict_database[id], 0
    file.close()
    


##################################
if __name__== "__main__":
   
    
    main()
