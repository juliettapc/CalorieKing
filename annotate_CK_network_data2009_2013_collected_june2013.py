#!/usr/bin/env python


'''
Code to build the CK network from the database

Created by Julia Poncela, on June 27th, 2013

'''

import networkx as nx  
import numpy
import random
import csv
import sys
import os
import itertools
import datetime
from database import *   #package to handle databases
from datetime import *

def main():
 

    ########### dB connection
    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 


    ###########  read the network file
    graph_filename="../Results/Networks/Network2009_2012.gml"
    G = nx.read_gml(graph_filename)
  


    first_date_included_analysis="2009-01-01 00:00:00"  # to filter out old records from the dB





    dict_node_ck_id={}
    dict_ck_id_node={}
    list_user_ck_id=[]
    for node in G.nodes():   # nodes are labels
        ck_id=G.node[node]['ck_id']
        list_user_ck_id.append(ck_id)
        dict_ck_id_node[ck_id]=node
        dict_node_ck_id[node]=ck_id




    for node in G.nodes():   
        G.node[node]['max_clique_size']=nx.algorithms.clique.node_clique_number(G, node)        
      
       
      



    ########### getting total time in the system (NOT considering membership periods)
    for ck_id in list_user_ck_id:
    
        query3="""SELECT * FROM activity_combined where ck_id ='"""+ str(ck_id)+ """' and activity_date >= '"""+ str(first_date_included_analysis)+"""' order by activity_date"""    
        result3 = db.query(query3)  # is a list of dict
     
        first_day_user=result3[0]["activity_date"]
        last_day_user=result3[-1]["activity_date"]

        time_in_system=(last_day_user-first_day_user).days +1

        node=dict_ck_id_node[ck_id]

        G.node[node]['tot_time_system']=time_in_system   # AT SOME POINT I WILL ADD AND effective_time_system, CONSIDERING MEMBERSHIP PERIODS


        print ck_id, first_day_user,last_day_user, time_in_system







    ########### getting betweenness
    dict_betweennes=nx.algorithms.centrality.betweenness_centrality(G)   
    for node in dict_betweennes:
        print node, "k:",G.node[node]['degree'],"betw.:",dict_betweennes[node], "max clique:",G.node[node]['max_clique_size']
        G.node[node]['betweenness']=dict_betweennes[node]

 

    ########### getting number of weigh_ins
    cont=0
    for ck_id in list_user_ck_id:

   
        query1="""SELECT * FROM weigh_in_history where ck_id ='"""+ str(ck_id)+ """' and on_day >= '"""+ str(first_date_included_analysis)+"""' order by on_day"""    
        result1 = db.query(query1)  # is a list of dict. 

        node= dict_ck_id_node[ck_id]
        G.node[node]['weigh_ins']=len(result1)
        print cont, ck_id, G.node[node]['weigh_ins']

        cont+=1



    ######### getting number of activity records
    cont=0
    for ck_id in list_user_ck_id:
     # if cont <100:
        query2="""SELECT * FROM activity_combined where ck_id ='"""+ str(ck_id)+ """' and activity_date >= '"""+ str(first_date_included_analysis)+"""' and activity_flag != '""" + str("WI")+"""' order by activity_date"""    
        result2 = db.query(query2)  # is a list of dict. 

        node= dict_ck_id_node[ck_id]
        G.node[node]['activity']=len(result2)
        print cont,ck_id, G.node[node]['activity']
      
        cont +=1




    #############  print out the network file
    new_graph_filename=graph_filename.split(".gml")[0]+"_annotated.gml"
    nx.write_gml(G,new_graph_filename)
    
    print "\nwritten network file:" , new_graph_filename






##################################################
######################################
if __name__ == '__main__':
 #   if len(sys.argv) > 1:
  #      filename = sys.argv[1]
   
        main()
   # else:
    #    print "Usage: python script.py path/filename"

    
