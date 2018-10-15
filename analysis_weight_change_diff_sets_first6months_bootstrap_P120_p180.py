#!/usr/bin/env python


'''
Code to read the CK database and the .gml file(s) to collect all info
on all users and create a csv master file for weight change and activity until 6months

Created by Julia Poncela, on September, 2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from database import *   
from datetime import *
import histograma_bines_gral

def main():
 

    Niter=10000     #  for bootstrapping 

    period="6m"  # "4m"or "6m"   # for the weight change over a period around a 4 or 6 months mark


    ####### input network files to collect the info from
    graph_name="./network_all_users/GC_full_network_all_users_merged_small_comm_roles_diff_layers1_roles_diff_layers1.5.gml"

    ##################
   


   ######### i build the networks  (remember label attribute matches id in users table)
    G = nx.read_gml(graph_name)
    G_GC = nx.connected_component_subgraphs(G)[0]


#    print "network size:", len(G.nodes()), "GC size:", len(G_GC.nodes())  # the network IS just the GC     1910

 
   ################
    csv_file="./analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_p180_p120_within.txt"
   #############




    dict_label_ck_id={}
    dict_ck_id_label={}

    dict_id_label={}
    dict_label_id={}

    for node in G.nodes():
        label=G.node[node]["label"]
        dict_id_label[node]=label
        dict_label_id[label]=node

    print "getting user's info from csv....."
    ################# getting info from csv
    
    file_csv_info=open(csv_file,'r')
    list_lines_file_csv_info=file_csv_info.readlines()  

    cont=0           
    cont_2wins=0
    cont_2wins_within_period =0


    cont_small_clusters=0
    cont_networked =0
    cont_GC=0
    cont_one_weigh_in=0
    cont_non_networked=0



   
    list_paying_period_all_2wins_p_period=[]
    list_paying_period_networked=[]
    list_paying_period_non_networked=[]
    list_paying_period_GC=[]
    list_paying_period_small_clusters=[]
    list_paying_period_with_R6friends=[]
    list_paying_period_0R6s=[]
    list_paying_period_kshell2_or_more=[]
    list_paying_period_kshell3_or_more=[]
    list_paying_period_kshell4_or_more=[]
    list_paying_period_kshell5_or_more=[]
    list_paying_period_kshell6_or_more=[]



    list_activity_period_all_2wins=[]
    list_activity_period_all_2wins_p_period=[]
    list_activity_period_networked=[]
    list_activity_period_non_networked=[]
    list_activity_period_GC=[]
    list_activity_period_small_clusters=[]
    list_activity_period_with_R6friends=[]
    list_activity_period_0R6s=[]

    list_activity_period_kshell2_or_more=[]
    list_activity_period_kshell3_or_more=[]
    list_activity_period_kshell4_or_more=[]
    list_activity_period_kshell5_or_more=[]
    list_activity_period_kshell6_or_more=[]







    list_percent_weight_changes_period_all_2wins=[]
    list_percent_weight_changes_period_all_2wins_p_period=[]
    list_percent_weight_changes_period_networked=[]
    list_percent_weight_changes_period_non_networked=[]
    list_percent_weight_changes_period_GC=[]
    list_percent_weight_changes_period_small_clusters=[]
    list_percent_weight_changes_period_with_R6friends=[]



    list_percent_weight_changes_period_0R6s=[]
    list_percent_weight_changes_period_1R6s=[]
    list_percent_weight_changes_period_2R6s=[]
    list_percent_weight_changes_period_3R6s=[]
    list_percent_weight_changes_period_4R6s=[]
    list_percent_weight_changes_period_5R6s=[]
    list_percent_weight_changes_period_6R6s=[]




    list_percent_weight_changes_period_0kshell=[]
    list_percent_weight_changes_period_1kshell=[]
    list_percent_weight_changes_period_2kshell=[]
    list_percent_weight_changes_period_3kshell=[]
    list_percent_weight_changes_period_4kshell=[]
    list_percent_weight_changes_period_5kshell=[]
    list_percent_weight_changes_period_6kshell=[]
    list_percent_weight_changes_period_7kshell=[]
    list_percent_weight_changes_period_8kshell=[]
    list_percent_weight_changes_period_9kshell=[]
    list_percent_weight_changes_period_10kshell=[]
    list_percent_weight_changes_period_11kshell=[]
    list_percent_weight_changes_period_12kshell=[]    # there is no kshell 13

    list_percent_weight_changes_period_9_or_more_kshell=[]    
   

    list_percent_weight_changes_period_with_kshell2or_more=[]
    list_percent_weight_changes_period_with_kshell3or_more=[]
    list_percent_weight_changes_period_with_kshell4or_more=[]
    list_percent_weight_changes_period_with_kshell5or_more=[]
    list_percent_weight_changes_period_with_kshell6or_more=[]
    list_percent_weight_changes_period_with_kshell7or_more=[]
  


    list_NA_kshell=[]


   
    dict_ck_id_p120={}
    dict_ck_id_p180={}
  



    cont_fat_fingers=0
    list_users=[]
    for line in list_lines_file_csv_info:
        if cont >0: 
            list_elements_line=line.strip("\r\n").split(" ")
          
            ck_id=str(list_elements_line[0])     
            label=str(list_elements_line[1])      

            kshell=int(list_elements_line[30])

            paying= list_elements_line[14]  # paid or free
           
        
            if ck_id not in list_users:
                list_users.append(ck_id)

          
            dict_label_ck_id[label]=ck_id
            dict_ck_id_label[ck_id]=label                       
           
            flag_skip=0
            if period == "4m":
                try:
                    pwc=float(list_elements_line[4])      
                    number_weigh_ins=  int(list_elements_line[6] )
                    activity=int(list_elements_line[8])
                    p=int(list_elements_line[18])     
                except ValueError:   # if pwc=NA
                    flag_skip=1
            elif period == "6m":
                try:
                    pwc=float(list_elements_line[5])
                    number_weigh_ins=  int(list_elements_line[7] )
                    activity=int(list_elements_line[9])
                    p=int(list_elements_line[19])    
                except ValueError:   # if pwc=NA
                    flag_skip=1
                

            if pwc < 100. and pwc > -100. and flag_skip==0:      # if pwc !=NA                    

              degree=int(list_elements_line[26])
              p_friends=int(list_elements_line[20])
                         
          
              if  p ==1 and number_weigh_ins >=2:  # users included in either by p_120 or p_180
                  cont_2wins_within_period +=1

                  list_percent_weight_changes_period_all_2wins_p_period.append(pwc)
                  list_activity_period_all_2wins_p_period.append(activity)
             
                  list_paying_period_all_2wins_p_period.append(paying)


                  if p_friends ==1 :
                    cont_networked +=1
                    list_percent_weight_changes_period_networked.append(pwc)
                    list_activity_period_networked.append(activity)

                    list_paying_period_networked.append(paying)

                   
                   # ojo!!!! people in the network but in SC are coded as kshell0 >>> coorected manually to kshell 1 in SC conditional!!
                    #if  kshell == 0:
                     #   list_percent_weight_changes_period_1kshell.append(pwc)

                    if  kshell == 1:
                        list_percent_weight_changes_period_1kshell.append(pwc)
                    elif  kshell == 2:
                        list_percent_weight_changes_period_2kshell.append(pwc)
                    elif  kshell == 3:
                        list_percent_weight_changes_period_3kshell.append(pwc)
                    elif  kshell == 4:
                        list_percent_weight_changes_period_4kshell.append(pwc)
                    elif  kshell == 5:
                        list_percent_weight_changes_period_5kshell.append(pwc)
                    elif  kshell == 6:
                        list_percent_weight_changes_period_6kshell.append(pwc)
                    elif  kshell == 7:
                        list_percent_weight_changes_period_7kshell.append(pwc)
                    elif  kshell == 8:
                        list_percent_weight_changes_period_8kshell.append(pwc)

 
                    elif  kshell == 9:   # from here on, i will group all users (too small sets otherwise)
                        list_percent_weight_changes_period_9kshell.append(pwc)
                        list_percent_weight_changes_period_9_or_more_kshell.append(pwc)
                    elif  kshell == 10:
                        list_percent_weight_changes_period_10kshell.append(pwc)
                        list_percent_weight_changes_period_9_or_more_kshell.append(pwc)
                    elif  kshell == 11:
                        list_percent_weight_changes_period_11kshell.append(pwc)
                        list_percent_weight_changes_period_9_or_more_kshell.append(pwc)
                    elif  kshell == 12:
                        list_percent_weight_changes_period_12kshell.append(pwc)
                        list_percent_weight_changes_period_9_or_more_kshell.append(pwc)
                 
                    else:
                        list_NA_kshell.append("Buh")
             



                    if  kshell >= 2:
                        list_percent_weight_changes_period_with_kshell2or_more.append(pwc)   # to get the equivalent of having a CH...
                        list_activity_period_kshell2_or_more.append(activity)
                        list_paying_period_kshell2_or_more.append(paying)
                    if  kshell >= 3:
                        list_percent_weight_changes_period_with_kshell3or_more.append(pwc)  
                        list_activity_period_kshell3_or_more.append(activity)
                        list_paying_period_kshell3_or_more.append(paying)
                    if  kshell >= 4:
                        list_percent_weight_changes_period_with_kshell4or_more.append(pwc)
                        list_activity_period_kshell4_or_more.append(activity)
                        list_paying_period_kshell4_or_more.append(paying)
                    if  kshell >= 5:
                        list_percent_weight_changes_period_with_kshell5or_more.append(pwc)
                        list_activity_period_kshell5_or_more.append(activity)
                        list_paying_period_kshell5_or_more.append(paying)
                    if  kshell >= 6:
                        list_percent_weight_changes_period_with_kshell6or_more.append(pwc)
                        list_activity_period_kshell6_or_more.append(activity)
                        list_paying_period_kshell6_or_more.append(paying)

          
                    if label in dict_label_id:  #GC
                        node=dict_label_id[label]                                                      
                        list_percent_weight_changes_period_GC.append(pwc)
                        list_activity_period_GC.append(activity)
                        list_paying_period_GC.append(paying)
                        cont_GC+=1

                        if G.node[node]["R6_overlap"]>0:
                            list_percent_weight_changes_period_with_R6friends.append(pwc)
                            list_activity_period_with_R6friends.append(activity)
                            list_paying_period_with_R6friends.append(paying)



                            if G.node[node]["R6_overlap"] == 1:
                                list_percent_weight_changes_period_1R6s.append(pwc)
                            elif G.node[node]["R6_overlap"] == 2:
                                list_percent_weight_changes_period_2R6s.append(pwc)
                            elif G.node[node]["R6_overlap"] == 3:
                                list_percent_weight_changes_period_3R6s.append(pwc)
                            elif G.node[node]["R6_overlap"] == 4:
                                list_percent_weight_changes_period_4R6s.append(pwc)
                            elif G.node[node]["R6_overlap"] == 5:
                                list_percent_weight_changes_period_5R6s.append(pwc)
                            elif G.node[node]["R6_overlap"] >= 6:
                                list_percent_weight_changes_period_6R6s.append(pwc)

                        else:
                            list_percent_weight_changes_period_0R6s.append(pwc)
                            list_activity_period_0R6s.append(activity)
                            list_paying_period_0R6s.append(paying)

            
                    else:
                        list_percent_weight_changes_period_small_clusters.append(pwc)
                        list_activity_period_small_clusters.append(activity)
                        list_paying_period_small_clusters.append(paying)                    
                        list_percent_weight_changes_period_1kshell.append(pwc)                     
                        cont_small_clusters+=1                        
                        
                       

                  else:
                    list_percent_weight_changes_period_non_networked.append(pwc)
                    list_activity_period_non_networked.append(activity)
                    list_paying_period_non_networked.append(paying)                 
                    list_percent_weight_changes_period_0kshell.append(pwc)
                    cont_non_networked+=1

              
              

            else:
                cont_fat_fingers+=1

        cont+=1

    ##############

    print "number of fat fingers:", cont_fat_fingers, "(excluded)"

    print "total sample size:",len(list_users),"\n with >=2 w-ins and weigh-ins around",period," mark:", cont_2wins_within_period

    print "networked:",cont_networked,"   non-networked:",cont_non_networked,"\nsize GC from csv:", cont_GC, "\nsmall clusters:",cont_small_clusters

  

    
    print "\navg. percent weight change:"

  #  print "  all with two w-ins ", numpy.mean(list_percent_weight_changes_period_all_2wins),"+/-", numpy.std(list_percent_weight_changes_period_all_2wins)/numpy.sqrt(float(len(list_percent_weight_changes_period_all_2wins)-1.)), "set size:",len(list_percent_weight_changes_period_all_2wins)

    print "  all with two w-ins and ",period,"_p=1:", numpy.mean(list_percent_weight_changes_period_all_2wins_p_period),"+/-", numpy.std(list_percent_weight_changes_period_all_2wins_p_period)/numpy.sqrt(float(len(list_percent_weight_changes_period_all_2wins_p_period)-1.)), "set size:",len(list_percent_weight_changes_period_all_2wins_p_period)

    print "  non networked:", numpy.mean(list_percent_weight_changes_period_non_networked),"+/-", numpy.std(list_percent_weight_changes_period_non_networked)/numpy.sqrt(float(len(list_percent_weight_changes_period_non_networked)-1.)), "set size:",len(list_percent_weight_changes_period_non_networked)
    
    print "  networked:", numpy.mean(list_percent_weight_changes_period_networked),"+/-", numpy.std(list_percent_weight_changes_period_networked)/numpy.sqrt(float(len(list_percent_weight_changes_period_networked)-1.)), "set size:",len(list_percent_weight_changes_period_networked)
    
    print "  small clusters:", numpy.mean(list_percent_weight_changes_period_small_clusters),"+/-", numpy.std(list_percent_weight_changes_period_small_clusters)/numpy.sqrt(float(len(list_percent_weight_changes_period_small_clusters)-1.)), "set size:",len(list_percent_weight_changes_period_small_clusters)
    
     
    print "  GC:", numpy.mean(list_percent_weight_changes_period_GC),"+/-", numpy.std(list_percent_weight_changes_period_GC)/numpy.sqrt(float(len(list_percent_weight_changes_period_GC)-1.)), "set size:",len(list_percent_weight_changes_period_GC)

    print "  without R6s:", numpy.mean(list_percent_weight_changes_period_0R6s),"+/-", numpy.std(list_percent_weight_changes_period_0R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_0R6s)-1.)), "set size:",len(list_percent_weight_changes_period_0R6s)

    print "  with R6s:", numpy.mean(list_percent_weight_changes_period_with_R6friends),"+/-", numpy.std(list_percent_weight_changes_period_with_R6friends)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_R6friends)-1.)), "set size:",len(list_percent_weight_changes_period_with_R6friends),"\n"


    print "  with kshell>= 2:", numpy.mean(list_percent_weight_changes_period_with_kshell2or_more),"+/-", numpy.std(list_percent_weight_changes_period_with_kshell2or_more)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_kshell2or_more)-1.)), "set size:",len(list_percent_weight_changes_period_with_kshell2or_more)

    print "  with kshell>= 3:", numpy.mean(list_percent_weight_changes_period_with_kshell3or_more),"+/-", numpy.std(list_percent_weight_changes_period_with_kshell3or_more)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_kshell3or_more)-1.)), "set size:",len(list_percent_weight_changes_period_with_kshell3or_more)

    print "  with kshell>= 4:", numpy.mean(list_percent_weight_changes_period_with_kshell4or_more),"+/-", numpy.std(list_percent_weight_changes_period_with_kshell4or_more)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_kshell4or_more)-1.)), "set size:",len(list_percent_weight_changes_period_with_kshell4or_more)

    print "  with kshell>= 5:", numpy.mean(list_percent_weight_changes_period_with_kshell5or_more),"+/-", numpy.std(list_percent_weight_changes_period_with_kshell5or_more)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_kshell5or_more)-1.)), "set size:",len(list_percent_weight_changes_period_with_kshell5or_more)
    
    print "  with kshell>= 6:", numpy.mean(list_percent_weight_changes_period_with_kshell6or_more),"+/-", numpy.std(list_percent_weight_changes_period_with_kshell6or_more)/numpy.sqrt(float(len(list_percent_weight_changes_period_with_kshell6or_more)-1.)), "set size:",len(list_percent_weight_changes_period_with_kshell6or_more)








   #####################


    print "\navg. activity over",period,":"

  
    print "  all with two w-ins and ",period,"_p=1:", numpy.mean(list_activity_period_all_2wins_p_period),"+/-", numpy.std(list_activity_period_all_2wins_p_period)/numpy.sqrt(float(len(list_activity_period_all_2wins_p_period)-1.)), "set size:",len(list_activity_period_all_2wins_p_period)

    print "  non networked:", numpy.mean(list_activity_period_non_networked),"+/-", numpy.std(list_activity_period_non_networked)/numpy.sqrt(float(len(list_activity_period_non_networked)-1.)), "set size:",len(list_activity_period_non_networked)
    
    print "  networked:", numpy.mean(list_activity_period_networked),"+/-", numpy.std(list_activity_period_networked)/numpy.sqrt(float(len(list_activity_period_networked)-1.)), "set size:",len(list_activity_period_networked)
    
    print "  small clusters:", numpy.mean(list_activity_period_small_clusters),"+/-", numpy.std(list_activity_period_small_clusters)/numpy.sqrt(float(len(list_activity_period_small_clusters)-1.)), "set size:",len(list_activity_period_small_clusters)
    
     
    print "  GC:", numpy.mean(list_activity_period_GC),"+/-", numpy.std(list_activity_period_GC)/numpy.sqrt(float(len(list_activity_period_GC)-1.)), "set size:",len(list_activity_period_GC)

    print "  without R6s:", numpy.mean(list_activity_period_0R6s),"+/-", numpy.std(list_activity_period_0R6s)/numpy.sqrt(float(len(list_activity_period_0R6s)-1.)), "set size:",len(list_activity_period_0R6s)

    print "  with R6s:", numpy.mean(list_activity_period_with_R6friends),"+/-", numpy.std(list_activity_period_with_R6friends)/numpy.sqrt(float(len(list_activity_period_with_R6friends)-1.)), "set size:",len(list_activity_period_with_R6friends),"\n"



    print "  with kshell>=2:", numpy.mean(list_activity_period_kshell2_or_more),"+/-", numpy.std(list_activity_period_kshell2_or_more)/numpy.sqrt(float(len(list_activity_period_kshell2_or_more)-1.)), "set size:",len(list_activity_period_kshell2_or_more)

    print "  with kshell>=3:", numpy.mean(list_activity_period_kshell3_or_more),"+/-", numpy.std(list_activity_period_kshell3_or_more)/numpy.sqrt(float(len(list_activity_period_kshell3_or_more)-1.)), "set size:",len(list_activity_period_kshell3_or_more)

    print "  with kshell>=4:", numpy.mean(list_activity_period_kshell4_or_more),"+/-", numpy.std(list_activity_period_kshell4_or_more)/numpy.sqrt(float(len(list_activity_period_kshell4_or_more)-1.)), "set size:",len(list_activity_period_kshell4_or_more)
    
    print "  with kshell>=5:", numpy.mean(list_activity_period_kshell5_or_more),"+/-", numpy.std(list_activity_period_kshell5_or_more)/numpy.sqrt(float(len(list_activity_period_kshell5_or_more)-1.)), "set size:",len(list_activity_period_kshell5_or_more)
    
    print "  with kshell>=6:", numpy.mean(list_activity_period_kshell6_or_more),"+/-", numpy.std(list_activity_period_kshell6_or_more)/numpy.sqrt(float(len(list_activity_period_kshell6_or_more)-1.)), "set size:",len(list_activity_period_kshell6_or_more)


   
   


 #####################
   

    print "\npercent of users in each group that lose at least 5%:"
    cont_2wins_p_period=0.
    for item in list_percent_weight_changes_period_all_2wins_p_period:        
        if item <= -5.0:
            cont_2wins_p_period+=1.

    print "  2wins and p",period,"=1:   ", cont_2wins_p_period/len(list_percent_weight_changes_period_all_2wins_p_period)*100.


    cont_non_networked=0.
    for item in list_percent_weight_changes_period_non_networked:
        if item <= -5.0:
            cont_non_networked+=1.

    print "    non-networked:   ", cont_non_networked/len(list_percent_weight_changes_period_non_networked)*100.


    cont_networked=0.
    for item in list_percent_weight_changes_period_networked:
        if item <= -5.0:
            cont_networked+=1.

    print "    networked:   ", cont_networked/len(list_percent_weight_changes_period_networked)*100.


    cont_sc=0.
    for item in list_percent_weight_changes_period_small_clusters:
        if item <= -5.0:
            cont_sc+=1.

    print "    SC:   ", cont_sc/len(list_percent_weight_changes_period_small_clusters)*100.




    cont_GC=0.
    for item in list_percent_weight_changes_period_GC:
        if item <= -5.0:
            cont_GC+=1.

    print "    GC:   ", cont_GC/len(list_percent_weight_changes_period_GC)*100.




    cont_withoutR6s=0.
    for item in list_percent_weight_changes_period_0R6s:
        if item <= -5.0:
            cont_withoutR6s+=1.

    print "    without R6s:   ", cont_withoutR6s/len(list_percent_weight_changes_period_0R6s)*100.




    cont_withR6s=0.
    for item in list_percent_weight_changes_period_with_R6friends:
        if item <= -5.0:
            cont_withR6s+=1.

    print "    with R6s:   ", cont_withR6s/len(list_percent_weight_changes_period_with_R6friends)*100.



    cont_kshell2or_more=0.
    for item in list_percent_weight_changes_period_with_kshell2or_more:
        if item <= -5.0:
            cont_kshell2or_more+=1
    print "    with kshell>=2:   ",cont_kshell2or_more/len(list_percent_weight_changes_period_with_kshell2or_more)*100.



    cont_kshell3or_more=0.
    for item in list_percent_weight_changes_period_with_kshell3or_more:
        if item <= -5.0:
            cont_kshell3or_more+=1
    print "    with kshell>=3:   ",cont_kshell3or_more/len(list_percent_weight_changes_period_with_kshell3or_more)*100.


    cont_kshell4or_more=0.
    for item in list_percent_weight_changes_period_with_kshell4or_more:
        if item <= -5.0:
            cont_kshell4or_more+=1
    print "    with kshell>=4:   ",cont_kshell4or_more/len(list_percent_weight_changes_period_with_kshell4or_more)*100.


    cont_kshell5or_more=0.
    for item in list_percent_weight_changes_period_with_kshell5or_more:
        if item <= -5.0:
            cont_kshell5or_more+=1
    print "    with kshell>=5:   ",cont_kshell5or_more/len(list_percent_weight_changes_period_with_kshell5or_more)*100.



    cont_kshell6or_more=0.
    for item in list_percent_weight_changes_period_with_kshell6or_more:
        if item <= -5.0:
            cont_kshell6or_more+=1
    print "    with kshell>=6:   ",cont_kshell6or_more/len(list_percent_weight_changes_period_with_kshell6or_more)*100.







    ##########################################################
    ############  Bootstrap for comparing the different sets:


    print "\n\nComparing Networked population vs. 2-weigh-in and P",period,"population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_networked)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic networked population weight change vs. 2weigh-in pop.:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_networked))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_networked_from_2wins_weight_changes_p"+str(period)+".dat")




   #####
    print "\n\nComparing GC population vs. 2-weigh-in and P",period," population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_GC)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic GC population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_GC))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_GC_from_2wins_weight_changes_p"+str(period)+".dat")



 #####
    print "\n\nComparing R6s friends population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_R6s_friends_from_2wins_weight_changes_p"+str(period)+".dat")





#####
    print "\n\nComparing kshell>=2 population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_kshell2or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
     

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=2 population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell2or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_kshell2_or_more_from_2wins_weight_changes_p"+str(period)+".dat")




#####
    print "\n\nComparing kshell>=3 population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_kshell3or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
     

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=3 population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell3or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_kshell3_or_more_from_2wins_weight_changes_p"+str(period)+".dat")




#####
    print "\n\nComparing kshell>=4 population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_kshell4or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
     

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=4 population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell4or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_kshell4_or_more_from_2wins_weight_changes_p"+str(period)+".dat")








#####
    print "\n\nComparing kshell>=5 population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_kshell5or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
     

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=5 population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell5or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_kshell5_or_more_from_2wins_weight_changes_p"+str(period)+".dat")








#####
    print "\n\nComparing kshell>=6 population vs. 2-weigh-in and P",period," population population"
    list_synthetic_averages_for_distribution=[]   
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_with_kshell6or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
     

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=6 population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell6or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_kshell6_or_more_from_2wins_weight_changes_p"+str(period)+".dat")












 #####
    print "\n\nComparing Small clusters population vs. 2-weigh-in and P",period,"population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_small_clusters)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic small clusters population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_small_clusters))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_small_clusters_from_2wins_weight_changes_p"+str(period)+".dat")




 #####
    print "\n\nComparing Non-networked population vs. 2-weigh-in and P",period," population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_all_2wins_p_period, len(list_percent_weight_changes_period_non_networked)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic Non networked population weight change vs. 2weigh-in and P",period," population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_non_networked))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_non_networked_from_2wins_weight_changes_p"+str(period)+".dat")



#######
#########

    print "\n\nComparing GC population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_GC)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic GC population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_GC))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_GC_from_networked_weight_changes_p"+str(period)+".dat")



   #####



    print "\n\nComparing R6s friends population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_R6friends_from_networked_weight_changes_p"+str(period)+".dat")






   #####



    print "\n\nComparing kshell >=2 population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_kshell2or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=2 population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell2or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell2_or_more_from_networked_weight_changes_p"+str(period)+".dat")




 #####



    print "\n\nComparing kshell >=3 population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_kshell3or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=3 population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell3or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell3_or_more_from_networked_weight_changes_p"+str(period)+".dat")






   #####



    print "\n\nComparing kshell >=4 population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_kshell4or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=4 population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell4or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell4_or_more_from_networked_weight_changes_p"+str(period)+".dat")










   #####



    print "\n\nComparing kshell >=5 population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_kshell5or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=5 population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell5or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell5_or_more_from_networked_weight_changes_p"+str(period)+".dat")










   #####



    print "\n\nComparing kshell >=6 population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_with_kshell6or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=6 population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell6or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell6_or_more_from_networked_weight_changes_p"+str(period)+".dat")









   #####




    print "\n\nComparing small clusters population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_networked, len(list_percent_weight_changes_period_small_clusters)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic small clusters population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_small_clusters))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_small_clusters_from_networked_weight_changes_p"+str(period)+".dat")


  #####
  #####



    print "\n\nComparing R6s friends population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_R6friends_from_GC_weight_changes_p"+str(period)+".dat")









    print "\n\nComparing kshell>=2 population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_kshell2or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=2  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell2or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell2_or_more_from_GC_weight_changes_p"+str(period)+".dat")








    print "\n\nComparing kshell>=3 population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_kshell3or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=3  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell3or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell3_or_more_from_GC_weight_changes_p"+str(period)+".dat")








    print "\n\nComparing kshell>=4 population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_kshell4or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=4  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell4or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell4_or_more_from_GC_weight_changes_p"+str(period)+".dat")









    print "\n\nComparing kshell>=5 population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_kshell5or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=5  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell5or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell5_or_more_from_GC_weight_changes_p"+str(period)+".dat")









    print "\n\nComparing kshell>=6 population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_period_GC, len(list_percent_weight_changes_period_with_kshell6or_more)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic kshell>=6  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_period_with_kshell6or_more))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_kshell6_or_more_from_GC_weight_changes_p"+str(period)+".dat")










    print "\n"

####################

    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_all_2wins_p_period,50,"./analysis_time_bins_bmi_groups/histogram_real_weight_change_distrib_2weigh_ins_p"+str(period)+".dat")

    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_networked,50,"./analysis_time_bins_bmi_groups/histogram_real_weight_change_distrib_networked_p"+str(period)+".dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_non_networked,50,"./analysis_time_bins_bmi_groups/histogram_real_weight_change_distrib_non_networked_p"+str(period)+".dat")
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_GC,50,"./analysis_time_bins_bmi_groups/histogram_real_weight_change_distrib_GC_p"+str(period)+".dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_small_clusters,50,"./analysis_time_bins_bmi_groups/histogram_real_weight_change_distrib_small_clusters_p"+str(period)+".dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_with_R6friends,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_with_R6friends_p"+str(period)+".dat")

    histograma_bines_gral.histograma_bins(list_percent_weight_changes_period_0R6s,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_changet_distrib_without_0R6s_friends_p"+str(period)+".dat")


 


#################


    print "\nRegarding weight change and having one or more R6s as friends:"
    print "  0 R6s:", numpy.mean(list_percent_weight_changes_period_0R6s),numpy.std(list_percent_weight_changes_period_0R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_0R6s)-1.)), " size:",len(list_percent_weight_changes_period_0R6s)
    print "  1 R6s:", numpy.mean(list_percent_weight_changes_period_1R6s),numpy.std(list_percent_weight_changes_period_1R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_1R6s)-1.)), " size:",len(list_percent_weight_changes_period_1R6s)
    print "  2 R6s:", numpy.mean(list_percent_weight_changes_period_2R6s),numpy.std(list_percent_weight_changes_period_2R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_2R6s)-1.)), " size:",len(list_percent_weight_changes_period_2R6s)
    print "  3 R6s:", numpy.mean(list_percent_weight_changes_period_3R6s),numpy.std(list_percent_weight_changes_period_3R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_3R6s)-1.)), " size:",len(list_percent_weight_changes_period_3R6s)
    print "  4 R6s:", numpy.mean(list_percent_weight_changes_period_4R6s),numpy.std(list_percent_weight_changes_period_4R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_4R6s)-1.)), " size:",len(list_percent_weight_changes_period_4R6s)
    print "  5 R6s:", numpy.mean(list_percent_weight_changes_period_5R6s),numpy.std(list_percent_weight_changes_period_5R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_5R6s)-1.)), " size:",len(list_percent_weight_changes_period_5R6s)
    print "  >= 6 R6s:", numpy.mean(list_percent_weight_changes_period_6R6s),numpy.std(list_percent_weight_changes_period_6R6s)/numpy.sqrt(float(len(list_percent_weight_changes_period_5R6s)-1.)), " size:",len(list_percent_weight_changes_period_6R6s),"\n"


#######################33


    print "\nRegarding weight change by kshell:"
    print "  k=0:", numpy.mean(list_percent_weight_changes_period_0kshell),numpy.std(list_percent_weight_changes_period_0kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_0kshell)-1.0)), " size:", len(list_percent_weight_changes_period_0kshell)

    print "  k=1:", numpy.mean(list_percent_weight_changes_period_1kshell),numpy.std(list_percent_weight_changes_period_1kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_1kshell)-1.0)), " size:", len(list_percent_weight_changes_period_1kshell)

    print "  k=2:", numpy.mean(list_percent_weight_changes_period_2kshell),numpy.std(list_percent_weight_changes_period_2kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_2kshell)-1.0)), " size:", len(list_percent_weight_changes_period_2kshell)

    print "  k=3:", numpy.mean(list_percent_weight_changes_period_3kshell),numpy.std(list_percent_weight_changes_period_3kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_3kshell)-1.0)), " size:", len(list_percent_weight_changes_period_3kshell)

    print "  k=4:", numpy.mean(list_percent_weight_changes_period_4kshell),numpy.std(list_percent_weight_changes_period_4kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_4kshell)-1.0)), " size:", len(list_percent_weight_changes_period_4kshell)

    print "  k=5:", numpy.mean(list_percent_weight_changes_period_5kshell),numpy.std(list_percent_weight_changes_period_5kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_5kshell)-1.0)), " size:", len(list_percent_weight_changes_period_5kshell)

    print "  k=6:", numpy.mean(list_percent_weight_changes_period_6kshell),numpy.std(list_percent_weight_changes_period_6kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_6kshell)-1.0)), " size:", len(list_percent_weight_changes_period_6kshell)

    print "  k=7:", numpy.mean(list_percent_weight_changes_period_7kshell),numpy.std(list_percent_weight_changes_period_7kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_7kshell)-1.0)), " size:", len(list_percent_weight_changes_period_7kshell)

    print "  k=8:", numpy.mean(list_percent_weight_changes_period_8kshell),numpy.std(list_percent_weight_changes_period_8kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_8kshell)-1.0)), " size:", len(list_percent_weight_changes_period_8kshell)

    print "  k=9:", numpy.mean(list_percent_weight_changes_period_9kshell),numpy.std(list_percent_weight_changes_period_9kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_9kshell)-1.0)), " size:", len(list_percent_weight_changes_period_9kshell)

    print "  k=10:", numpy.mean(list_percent_weight_changes_period_10kshell),numpy.std(list_percent_weight_changes_period_10kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_10kshell)-1.0)), " size:", len(list_percent_weight_changes_period_10kshell)

    print "  k=11:", numpy.mean(list_percent_weight_changes_period_11kshell),numpy.std(list_percent_weight_changes_period_11kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_11kshell)-1.0)), " size:", len(list_percent_weight_changes_period_11kshell)

    print "  k=12:", numpy.mean(list_percent_weight_changes_period_12kshell),numpy.std(list_percent_weight_changes_period_12kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_12kshell)-1.0)), " size:", len(list_percent_weight_changes_period_12kshell),"\n"

  
    print "  k >=9:", numpy.mean(list_percent_weight_changes_period_9_or_more_kshell),numpy.std(list_percent_weight_changes_period_9_or_more_kshell)/numpy.sqrt(float(len(list_percent_weight_changes_period_9_or_more_kshell)-1.0)), " size:", len(list_percent_weight_changes_period_9_or_more_kshell)


    print "num people with k>0 but no kshell:",len(list_NA_kshell),"\n\n"




    print "Regarding paying users:"
  
    print "   all with 2-wins in period:", list_paying_period_all_2wins_p_period.count("paid"), "  out of ", len(list_paying_period_all_2wins_p_period), "total", list_paying_period_all_2wins_p_period.count("paid")/float( len(list_paying_period_all_2wins_p_period))
    print "   networked:", list_paying_period_networked.count("paid"), "  out of ", len(list_paying_period_networked), "total", list_paying_period_networked.count("paid")/float(len(list_paying_period_networked))
    print "   non networked:", list_paying_period_non_networked.count("paid"), "  out of ", len(list_paying_period_non_networked), "total", list_paying_period_non_networked.count("paid")/float( len(list_paying_period_non_networked))
    print "   GC:", list_paying_period_GC.count("paid"), "  out of ", len(list_paying_period_GC), "total", list_paying_period_GC.count("paid")/float( len(list_paying_period_GC))
    print "   small clusters", list_paying_period_small_clusters.count("paid"), "  out of ", len(list_paying_period_small_clusters), "total", list_paying_period_small_clusters.count("paid")/float( len(list_paying_period_small_clusters))
    print "   without R6 friends:", list_paying_period_0R6s.count("paid"), "  out of ", len(list_paying_period_0R6s), "total", list_paying_period_0R6s.count("paid")/float(len(list_paying_period_0R6s))
    
    print "   with R6 friends:", list_paying_period_with_R6friends.count("paid"), "  out of ", len(list_paying_period_with_R6friends), "total", list_paying_period_with_R6friends.count("paid")/float( len(list_paying_period_with_R6friends))
   

    print "   with kshel>=2:", list_paying_period_kshell2_or_more.count("paid"), "  out of ", len(list_paying_period_kshell2_or_more), "total", list_paying_period_kshell2_or_more.count("paid")/float( len(list_paying_period_kshell2_or_more))
   
    print "   with kshel>=3:", list_paying_period_kshell3_or_more.count("paid"), "  out of ", len(list_paying_period_kshell3_or_more), "total", list_paying_period_kshell3_or_more.count("paid")/float( len(list_paying_period_kshell3_or_more))
   
    print "   with kshel>=4:", list_paying_period_kshell4_or_more.count("paid"), "  out of ", len(list_paying_period_kshell4_or_more), "total", list_paying_period_kshell4_or_more.count("paid")/float( len(list_paying_period_kshell4_or_more))
   
    print "   with kshel>=5:", list_paying_period_kshell5_or_more.count("paid"), "  out of ", len(list_paying_period_kshell5_or_more), "total", list_paying_period_kshell5_or_more.count("paid")/float( len(list_paying_period_kshell5_or_more))
   
    print "   with kshel>=6:", list_paying_period_kshell6_or_more.count("paid"), "  out of ", len(list_paying_period_kshell6_or_more), "total", list_paying_period_kshell6_or_more.count("paid")/float( len(list_paying_period_kshell6_or_more))
   
  





 #################################       
#################################
def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result






##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename_network1 = sys.argv[1]
    #    filename_network_for_kshell = sys.argv[2]
   
     #   main(filename_network1,filename_network_for_kshell)
    #else:
     #   print "Usage: python script.py path/filename.gml  path/filename_for_kshell.gml"

    
    main()
