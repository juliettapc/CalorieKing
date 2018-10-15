#! /usr/bin/env python

"""
Created by Julia Poncela of June 2012

Analyze the strength of the links with R6s, defined as #_messages_to_R6s/tot.

"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import networkx as nx
import random
import histograma_gral
import histograma_bines_gral
import csv

def main ():


   
     
    result_master= csv.reader(open("/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_all_users/new_master_csv_jan_20_after_filter_for_2_weighins_withSM_info.csv", 'r'), delimiter=',')   

    result_sc_adh= csv.reader(open("/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_all_users/adherent_sc.csv", 'r'), delimiter=',')   

    result_sc_Nonadh= csv.reader(open("/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_all_users/nonadherent_sc.csv", 'r'), delimiter=',') 

    list_sc=[]
    for row in result_sc_adh:
         if row[0] != 'id':  # i exclude the first line 
             sc_ck_id=row[1]
             print sc_ck_id
             if sc_ck_id not in list_sc:
                 list_sc.append(sc_ck_id)

    print len(list_sc)
    raw_input()


    for row in result_sc_Nonadh:
         if row[0] != 'id':  # i exclude the first line 
             sc_ck_id=row[1]
             print sc_ck_id
             if sc_ck_id not in list_sc:
                 list_sc.append(sc_ck_id)

    print len(list_sc)


    raw_input()


    outputfile = open("new_master_csv_jan_20_after_filter_for_2_weighins_withSM_info_modified.csv",'wt')

    print >> outputfile, "activity","id","ck_id","join_date","initial_weight","most_recent_weight","height","age","weighins","initial_bmi","final_bmi","percentage_weight_change","weight_change","time_in_system","outcome20","outcome50","p_50","act_20","wi_20","p_friend","R6_overlap","degree","friend_avg","C0","C1","C2","C3","C4","C5","C6","C7","max_clique","k.shell","p50andfriend","p50pfriend","SC"

    for row in result_master:        
        if row[0] != 'id':  # i exclude the first line 

            ck_id=row[1]
            if ck_id in list_sc:
                for element in row:

                    print >> outputfile,element
                print >> outputfile,1

            else:
                for element in row:

                    print >> outputfile,element
            print >> outputfile,0
   

        #  print >> file,label,ck_id,Gini_friends,Gini_to_friends,Gini_from_friends,sum(list_weighted_tot_messg_friends_R6s_norm),sum(list_weighted_to_friends_R6s_norm),sum(list_weighted_from_friends_R6s_norm),num_tot_messg,tot_sent,tot_received, tot_public_mess,blog_posts,home_page,forum_posts,lesson_com,tot_activity


    outputfile.close()
     




################################################

          
if __name__ == '__main__':
  

    main()
   
     

##############################################
