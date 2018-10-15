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

    ####### input network files to collect the info from
    graph_name="./network_all_users/GC_full_network_all_users_merged_small_comm_roles_diff_layers1_roles_diff_layers1.5.gml"

    ##################
   
 



   ######### i build the networks  (remember label attribute matches id in users table)
    G = nx.read_gml(graph_name)
    G_GC = nx.connected_component_subgraphs(G)[0]


#    print "network size:", len(G.nodes()), "GC size:", len(G_GC.nodes())  # the network IS just the GC     1910

 
   ################
    csv_file="analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_2w_ins.txt"
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
    cont_small_clusters=0
    cont_networked =0
    cont_GC=0
    cont_one_weigh_in=0
    cont_non_networked=0


    list_percent_weight_changes_6months_all_2wins=[]
    list_percent_weight_changes_6months_networked=[]
    list_percent_weight_changes_6months_non_networked=[]
    list_percent_weight_changes_6months_GC=[]
    list_percent_weight_changes_6months_small_clusters=[]
    list_percent_weight_changes_6months_with_R6friends=[]

    list_percent_weight_changes_6months_0R6s=[]
    list_percent_weight_changes_6months_1R6s=[]
    list_percent_weight_changes_6months_2R6s=[]
    list_percent_weight_changes_6months_3R6s=[]
    list_percent_weight_changes_6months_4R6s=[]
    list_percent_weight_changes_6months_5R6s=[]
    list_percent_weight_changes_6months_6R6s=[]


    cont_fat_fingers=0
    list_users=[]
    for line in list_lines_file_csv_info:
        if cont >0: 
            list_elements_line=line.strip("\r\n").split(" ")
          
            ck_id=str(list_elements_line[0])     
            label=str(list_elements_line[1])      

            if ck_id not in list_users:
                list_users.append(ck_id)

          
            dict_label_ck_id[label]=ck_id
            dict_ck_id_label[ck_id]=label

     
            weigh_change_6months=float(list_elements_line[2])
            percent_weight_change_6months= float(list_elements_line[3])

            if percent_weight_change_6months < 100. and percent_weight_change_6months > -100.:

            
              number_weigh_ins_6months=  int(list_elements_line[4] )
              activity_6months=int(list_elements_line[5])
              degree=int(list_elements_line[20])
              p_friends=int(list_elements_line[15])

            

              if number_weigh_ins_6months >=2:
                cont_2wins+=1
                list_percent_weight_changes_6months_all_2wins.append(percent_weight_change_6months)

                if p_friends ==1 :
                    cont_networked +=1
                    list_percent_weight_changes_6months_networked.append(percent_weight_change_6months)
          
                    if label in dict_label_id:  #GC
                        node=dict_label_id[label]                                                      
                        list_percent_weight_changes_6months_GC.append(percent_weight_change_6months)
                        cont_GC+=1

                        if G.node[node]["R6_overlap"]>0:
                            list_percent_weight_changes_6months_with_R6friends.append(percent_weight_change_6months)
                           

                            if G.node[node]["R6_overlap"] == 1:
                                list_percent_weight_changes_6months_1R6s.append(percent_weight_change_6months)
                            elif G.node[node]["R6_overlap"] == 2:
                                list_percent_weight_changes_6months_2R6s.append(percent_weight_change_6months)
                            elif G.node[node]["R6_overlap"] == 3:
                                list_percent_weight_changes_6months_3R6s.append(percent_weight_change_6months)
                            elif G.node[node]["R6_overlap"] == 4:
                                list_percent_weight_changes_6months_4R6s.append(percent_weight_change_6months)
                            elif G.node[node]["R6_overlap"] == 5:
                                list_percent_weight_changes_6months_5R6s.append(percent_weight_change_6months)
                            elif G.node[node]["R6_overlap"] >= 6:
                                list_percent_weight_changes_6months_6R6s.append(percent_weight_change_6months)

                        else:
                            list_percent_weight_changes_6months_0R6s.append(percent_weight_change_6months)

            
                    else:
                        list_percent_weight_changes_6months_small_clusters.append(percent_weight_change_6months)
                        cont_small_clusters+=1

                else:
                    list_percent_weight_changes_6months_non_networked.append(percent_weight_change_6months)
                    cont_non_networked+=1
              else:
                cont_one_weigh_in+=1

            else:
                cont_fat_fingers+=1

        cont+=1

    ##############

    print "number of fat fingers:", cont_fat_fingers, "(excluded)"

    print "total sample size:",len(list_users),"\n with >=2 w-ins:",cont_2wins

    print "networked:",cont_networked,"   non-networked:",cont_non_networked,"\nsize GC from csv:", cont_GC, "\nsmall clusters:",cont_small_clusters
    print "users with just one weigh in:", cont_one_weigh_in

    
    print "\navg. percent weight change:"
    print "  all with two w-ins:", numpy.mean(list_percent_weight_changes_6months_all_2wins),"+/-", numpy.std(list_percent_weight_changes_6months_all_2wins)/numpy.sqrt(float(len(list_percent_weight_changes_6months_all_2wins)-1.)), "set size:",len(list_percent_weight_changes_6months_all_2wins)
    print "  non networked:", numpy.mean(list_percent_weight_changes_6months_non_networked),"+/-", numpy.std(list_percent_weight_changes_6months_non_networked)/numpy.sqrt(float(len(list_percent_weight_changes_6months_non_networked)-1.)), "set size:",len(list_percent_weight_changes_6months_non_networked)
    
    print "  networked:", numpy.mean(list_percent_weight_changes_6months_networked),"+/-", numpy.std(list_percent_weight_changes_6months_networked)/numpy.sqrt(float(len(list_percent_weight_changes_6months_networked)-1.)), "set size:",len(list_percent_weight_changes_6months_networked)
    
    print "  small clusters:", numpy.mean(list_percent_weight_changes_6months_small_clusters),"+/-", numpy.std(list_percent_weight_changes_6months_small_clusters)/numpy.sqrt(float(len(list_percent_weight_changes_6months_small_clusters)-1.)), "set size:",len(list_percent_weight_changes_6months_small_clusters)
    
     
    print "  GC:", numpy.mean(list_percent_weight_changes_6months_GC),"+/-", numpy.std(list_percent_weight_changes_6months_GC)/numpy.sqrt(float(len(list_percent_weight_changes_6months_GC)-1.)), "set size:",len(list_percent_weight_changes_6months_GC)

    print "  without R6s:", numpy.mean(list_percent_weight_changes_6months_0R6s),"+/-", numpy.std(list_percent_weight_changes_6months_0R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_0R6s)-1.)), "set size:",len(list_percent_weight_changes_6months_0R6s)

    print "  with R6s:", numpy.mean(list_percent_weight_changes_6months_with_R6friends),"+/-", numpy.std(list_percent_weight_changes_6months_with_R6friends)/numpy.sqrt(float(len(list_percent_weight_changes_6months_with_R6friends)-1.)), "set size:",len(list_percent_weight_changes_6months_with_R6friends),"\n"

   

   


    ##########################################################
    ############  Bootstrap for comparing the different sets:


    print "\n\nComparing Networked population vs. 2-weigh-in population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_all_2wins, len(list_percent_weight_changes_6months_networked)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic networked population weight change vs. 2weigh-in pop.:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_networked))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_networked_from_2wins_weight_changes.dat")




   #####
    print "\n\nComparing GC population vs. 2-weigh-in population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_all_2wins, len(list_percent_weight_changes_6months_GC)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic GC population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_GC))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_GC_from_2wins_weight_changes.dat")



 #####
    print "\n\nComparing R6s friends population vs. 2-weigh-in population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_all_2wins, len(list_percent_weight_changes_6months_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_R6s_friends_from_2wins_weight_changes.dat")





 #####
    print "\n\nComparing Small clusters population vs. 2-weigh-in population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_all_2wins, len(list_percent_weight_changes_6months_small_clusters)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic small clusters population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_small_clusters))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_small_clusters_from_2wins_weight_changes.dat")




 #####
    print "\n\nComparing Non-networked population vs. 2-weigh-in population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_all_2wins, len(list_percent_weight_changes_6months_non_networked)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic Non networked population weight change vs. 2weigh-in population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_non_networked))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_non_networked_from_2wins_weight_changes.dat")



#######
#########

    print "\n\nComparing GC population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_networked, len(list_percent_weight_changes_6months_GC)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic GC population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_GC))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_GC_from_networked_weight_changes.dat")



   #####



    print "\n\nComparing R6s friends population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_networked, len(list_percent_weight_changes_6months_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_R6friends_from_networked_weight_changes.dat")



   #####




    print "\n\nComparing small clusters population vs Networked population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_networked, len(list_percent_weight_changes_6months_small_clusters)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic small clusters population weight change vs. Networked population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_small_clusters))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_small_clusters_from_networked_weight_changes.dat")



  #####
  #####



    print "\n\nComparing R6s friends population vs GC population"
    list_synthetic_averages_for_distribution=[]   # 2 w-ins vs networked pop.
    for i in range(Niter):
        synthetic_mean=numpy.mean(sample_with_replacement(list_percent_weight_changes_6months_GC, len(list_percent_weight_changes_6months_with_R6friends)) )
        list_synthetic_averages_for_distribution.append(synthetic_mean )
      #  print  synthetic_mean

    print "average all synthetic values:",numpy.mean(list_synthetic_averages_for_distribution), "+/-",numpy.std(list_synthetic_averages_for_distribution)

  
    print "z-score synthetic R6s friends  population weight change vs. GC population:", (numpy.mean(list_synthetic_averages_for_distribution)-numpy.mean(list_percent_weight_changes_6months_with_R6friends))/numpy.std(list_synthetic_averages_for_distribution)

    histograma_bines_gral.histograma_bins(list_synthetic_averages_for_distribution,50,"./analysis_time_bins_bmi_groups/histogram_synthetic_with_R6friends_from_GC_weight_changes.dat")

    print "\n"

####################

    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_all_2wins,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_2weigh_ins.dat")


    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_networked,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_networked.dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_non_networked,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_non_networked.dat")
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_GC,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_GC.dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_small_clusters,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_small_clusters.dat")
    
    
    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_with_R6friends,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_with_R6friends.dat")


    histograma_bines_gral.histograma_bins(list_percent_weight_changes_6months_0R6s,50,"./analysis_time_bins_bmi_groups/histogram_real_weigh_change_distrib_without_0R6s_friends.dat")


 


#################


    print "\nRegarding weight change and having one or more R6s as friends:"
    print "  0 R6s:", numpy.mean(list_percent_weight_changes_6months_0R6s),numpy.std(list_percent_weight_changes_6months_0R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_0R6s)-1.)), " size:",len(list_percent_weight_changes_6months_0R6s)
    print "  1 R6s:", numpy.mean(list_percent_weight_changes_6months_1R6s),numpy.std(list_percent_weight_changes_6months_1R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_1R6s)-1.)), " size:",len(list_percent_weight_changes_6months_1R6s)
    print "  2 R6s:", numpy.mean(list_percent_weight_changes_6months_2R6s),numpy.std(list_percent_weight_changes_6months_2R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_2R6s)-1.)), " size:",len(list_percent_weight_changes_6months_2R6s)
    print "  3 R6s:", numpy.mean(list_percent_weight_changes_6months_3R6s),numpy.std(list_percent_weight_changes_6months_3R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_3R6s)-1.)), " size:",len(list_percent_weight_changes_6months_3R6s)
    print "  4 R6s:", numpy.mean(list_percent_weight_changes_6months_4R6s),numpy.std(list_percent_weight_changes_6months_4R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_4R6s)-1.)), " size:",len(list_percent_weight_changes_6months_4R6s)
    print "  5 R6s:", numpy.mean(list_percent_weight_changes_6months_5R6s),numpy.std(list_percent_weight_changes_6months_5R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_5R6s)-1.)), " size:",len(list_percent_weight_changes_6months_5R6s)
    print "  >= 6 R6s:", numpy.mean(list_percent_weight_changes_6months_6R6s),numpy.std(list_percent_weight_changes_6months_6R6s)/numpy.sqrt(float(len(list_percent_weight_changes_6months_5R6s)-1.)), " size:",len(list_percent_weight_changes_6months_6R6s)




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
