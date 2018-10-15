#!/usr/bin/env python


'''
Given a .gml network, 

Created by Julia Poncela, on April 2013.

'''


import sys
import os
import networkx as nx
import numpy
import itertools
import random
import csv
from database import *   #package to handle databases
import histograma_bines_gral
from scipy import stats



def main():

    #full_network_filename="./network_all_users/full_network_all_users.gml"  # i CANT use this network, because the labels dont match the users id from the dB
   # G_full = nx.read_gml(full_network_filename)



  #  list_A=[]   #Testign out how KS works on a random sample
   # list_B=[]
    #for i in range (10000):
     #   list_A.append(random.random())
      #  list_B.append(random.random())

    #print "KS test listA against normal distrib:", stats.kstest(list_A, "norm" )
   # print "KS test listB against normal distrib:", stats.kstest(list_B, "norm" )
    #print "two-sided KS test listA vs listB:", stats.ks_2samp(list_A, list_B)

   

    unrealistic_weight_change=70.

    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 



    GC_network_filename="./network_all_users/GC_full_network_all_users_merged_small_comm_roles_diff_layers1_roles_diff_layers1.5.gml"
    G = nx.read_gml(GC_network_filename)


    output_filename="./network_all_users/Results_comparison_histograms_percent_weight_change.txt"
    file_output = open(output_filename,'wt')



  #  print "num. nodes:",len(G.nodes())

    list_of_lists=nx.connected_components(G)

    print "num. of components:",len(list_of_lists), "size GC:",len(list_of_lists[0])
   
    list_weight_changes_GC=[]
    list_weight_changes_R6friends=[]
    for node in G.nodes():
        label=G.node[node]["label"]
        percent_weight_change=G.node[node]["percentage_weight_change"]
        R6_overlap=G.node[node]["R6_overlap"]
        #print node, label, weight_change, R6_overlap
        if percent_weight_change > -unrealistic_weight_change and  percent_weight_change < unrealistic_weight_change :   # filter out unrealistic values


            list_weight_changes_GC.append(percent_weight_change)
            
            if R6_overlap >0:            
                list_weight_changes_R6friends.append(percent_weight_change)
          

    print >> file_output,"num GC users:", len(list_weight_changes_GC), "num users with R6 friends:", len(list_weight_changes_R6friends)




    histograma_bines_gral.histograma_bins(list_weight_changes_GC, 20, "./network_all_users/histogram_weight_change_GC_users.dat")
    histograma_bines_gral.histograma_bins(list_weight_changes_R6friends, 20, "./network_all_users/histogram_weight_change_users_with_R6friends.dat")


    print >> file_output,"KS test GC against normal distrib:", stats.kstest(list_weight_changes_GC, "norm" )
    print >> file_output,"KS test users with R6 friends against normal distrib:", stats.kstest(list_weight_changes_R6friends, "norm")

    print >> file_output,"two-sided KS test GC vs users with R6 friends:", stats.ks_2samp(list_weight_changes_GC,list_weight_changes_R6friends)



   
    list_weight_changes_all=[]
    query1="""SELECT * FROM users"""    
    result1 = db.query(query1)  # is a list of dicts.
    for r1 in result1:   
        percent_weight_change=(float(r1['most_recent_weight'])-float(r1['initial_weight']) ) /float(r1['initial_weight'])

    #    if percent_weight_change > -unrealistic_weight_change and  percent_weight_change < unrealistic_weight_change :   # filter out unrealistic values
        list_weight_changes_all.append(percent_weight_change)



    histograma_bines_gral.histograma_bins(list_weight_changes_all, 200, "./network_all_users/histogram_weight_change_users_all_200bins.dat")

    print >> file_output,"tot. number users",len(list_weight_changes_all)
    print >> file_output,"KS test all against normal distrib:", stats.kstest(list_weight_changes_all, "norm" )
    print >> file_output,"two-sided KS test all vs GC:", stats.ks_2samp(list_weight_changes_all,list_weight_changes_GC)
    print >> file_output,"two-sided KS test all vs users with R6 friends:", stats.ks_2samp(list_weight_changes_GC,list_weight_changes_R6friends)


    file_output.close()
    print "written file:",output_filename



    exit()

    query1="""SELECT * FROM friends order by src asc"""    
    result1 = db.query(query1)  # is a list of dict.       
    
    print "number links:",len(result1)
    list_friends=[]
    
    for r1 in result1:   
       
        label_src=r1['src']

        label_dest=r1['dest']

        if label_src not in list_friends:
            list_friends.append(label_src)
        if label_dest not in list_friends:
            list_friends.append(label_dest)


    print "num networked users:",len(list_friends)


##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py path/network.gml"

    
