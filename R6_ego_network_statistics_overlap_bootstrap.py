#!/usr/bin/env python

"""
Created by Julia Poncela on March 2011

Given a network.gml (with role attributes) it calculates averages and standard deviation of
weight change, BMI change and activity for all N6's neighbors, depending on 
how many R6s you are connected to.

It takes as argument the path/network.gml  and creates a buch of files: ego_R6s_average_weight_change300.txt, 


"""

import sys
import os
import networkx as nx
import math
from pylab import *
import numpy
import random
from  scipy import stats
 
def main(graph_name):
  
    G = nx.read_gml(graph_name)
    G = nx.connected_component_subgraphs(G)[0] # Giant component 
  
   
   


    list_one_friend_percent_weight_change=[]    
    list_all=[]
    for node in G.nodes():
        if G.node[node]['label'] == "40155" :
            special=node           
            for n in G.neighbors(node):                
                if G.node[n]['time_in_system'] >100:
                    list_all.append(float(G.node[n]['percentage_weight_change']))
                    print len(G.neighbors(n))
                    if len(G.neighbors(n))==1:
                        list_one_friend_percent_weight_change.append(float(G.node[n]['percentage_weight_change']))
           
            break

  
    print "final number of friendless nodes:", len(list_one_friend_percent_weight_change), "av_percent_wc:",numpy.mean(list_one_friend_percent_weight_change),numpy.std(list_one_friend_percent_weight_change)
    print "av_%_wc fo all",len(list_all), "neighbors of 40155:", numpy.mean(list_all), numpy.std(list_all) 


  



    #dir=graph_name.split("fr")[0]
    dir=graph_name.split("mas")[0]
   
   
    original_name=graph_name.split("data/")[1]
    original_name=original_name.split(".gml")[0]

    dir=dir+"roles/"+original_name
            
 
    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

    iterations=1000  #for boostrap

   
    name00=dir+"bootstrap_statistics_percent_weight_change_one_hops_R6s"+str(time_in_system)+"days_exclude_R6s.dat"
  

    list_R6s=[]     # collect the R6 of the system   
    list_R6s_labels=[] 
    for node in G.nodes() :    
        if str(G.node[node]['role']) == "R6" :
          list_R6s.append(node)
          list_R6s_labels.append(str(G.node[node]['label']))
    


    list_percentage_wc_one_hop=[]    
    list_one_hoppers=[]    
    for node in G.nodes():       
        if (str(G.node[node]['role']) == "R6" ):
            
            for n in  G.neighbors(node):
                if (str(G.node[n]['role']) != "R6" ):
                    if  int(G.node[n]['time_in_system']) > time_in_system :
                        if n not in list_one_hoppers:
                            list_percentage_wc_one_hop.append(float(G.node[n]['percentage_weight_change']))  

                            list_one_hoppers.append(n)
                        
  


    print "all one-hops:",numpy.mean(list_percentage_wc_one_hop),len(list_percentage_wc_one_hop)
           
   
    file0=open(name00, 'wt')
    print >> file0,"Percentage Weight Change for one-hop-from-R6s\n\n\n","original:",numpy.mean(list_percentage_wc_one_hop),"   set size:",len(list_percentage_wc_one_hop)           
    file0.close()
       

    
# R6s en friend_graph_all.gml: 40155, 28688, 45784, 41794, 43020, 47063, 39625, 31954, 40324,40666


#R6s en master_adherent_homo.gml: 40155, 41794, 39625, 46487, 31954, 40324, 28688, 45784, 40666


    for excluding in list_R6s_labels:


        list_percentage_wc_one_hop_excluding_oneR6=[]    
        list_one_hoppers_excluding_oneR6=[]    
        for node in G.nodes():       
            if (str(G.node[node]['role']) == "R6" ) and (str(G.node[node]['label']) != excluding ): 
                for n in  G.neighbors(node):
                    if (str(G.node[n]['role']) != "R6" ):
                        if  int(G.node[n]['time_in_system']) > time_in_system :
                            if n not in list_one_hoppers_excluding_oneR6:                          
                                list_percentage_wc_one_hop_excluding_oneR6.append(float(G.node[n]['percentage_weight_change']))  
                                
                                list_one_hoppers_excluding_oneR6.append(n)
                                  


        actual_diff=numpy.mean(list_percentage_wc_one_hop)-numpy.mean(list_percentage_wc_one_hop_excluding_oneR6)

        print "\n\ndiff. all one-hops & all but one hub",excluding,":",actual_diff



        file0=open(name00, 'at')
        print >> file0,"    excluding",excluding, ":",numpy.mean(list_percentage_wc_one_hop_excluding_oneR6), " (diff:" , actual_diff,")   set size:",len(list_percentage_wc_one_hop_excluding_oneR6)         
        file0.close()





      ###############################################
      # boostrap routine, sampling with replacement:#
      ###############################################
        list_all=[]
        for i in list_percentage_wc_one_hop:
            list_all.append(i)
        for i in list_percentage_wc_one_hop_excluding_oneR6:
            list_all.append(i)


        list_synth_diff=[]


        for iter in range(iterations):
            list_synth_one_hop=sample_with_replacement(list_all,len(list_percentage_wc_one_hop))
            list_synth_one_hop_excluding_oneR6s=sample_with_replacement(list_all,len(list_percentage_wc_one_hop_excluding_oneR6))
                        

            mean1=numpy.mean(list_synth_one_hop)
            mean2=numpy.mean(list_synth_one_hop_excluding_oneR6s)

            list_synth_diff.append(mean1-mean2)
       

        zscore=(actual_diff-numpy.mean(list_synth_diff))/numpy.std(list_synth_diff)

        print "mean_over_synth_realizations (with repl.):",numpy.mean(list_synth_diff),"zscore:",zscore
        

        file0=open(name00, 'at')
        print >> file0,"       z-score (sampling with replacement)",zscore
        file0.close()
        

      # boostrap routine, sampling without replacement:

        list_synth_diff=[]


        for iter in range(iterations):
            list_synth_one_hop=random.sample(list_all,len(list_percentage_wc_one_hop))

            for i in list_all:
                if i not in list_synth_one_hop:
                    list_synth_one_hop_excluding_oneR6s.append(i)
                                   

            mean1=numpy.mean(list_synth_one_hop)
            mean2=numpy.mean(list_synth_one_hop_excluding_oneR6s)

            list_synth_diff.append(mean1-mean2)
       

        zscore=(actual_diff-numpy.mean(list_synth_diff))/numpy.std(list_synth_diff)

        print "mean_over_synth_realizations (without repl.):",numpy.mean(list_synth_diff),"zscore:",zscore

       

       

        # mood test
        mood=stats.mood(list_percentage_wc_one_hop,list_percentage_wc_one_hop_excluding_oneR6) 
        print "mood test:",mood
        
        #t test:
        ttest=stats.ttest_ind(list_percentage_wc_one_hop,list_percentage_wc_one_hop_excluding_oneR6, axis=0)
        print "t-test:",ttest


       #wilcoxon test  SET SIZES MUST BE THE SAME
       # wilcoxon=stats.wilcoxon(list_percentage_wc_one_hop, list_percentage_wc_one_hop_excluding_oneR6)
        #print "wilcoxon test:",wilcoxon
     


        file0=open(name00, 'at')
        print >> file0,"       z-score (sampling without replacement)",zscore,"\n       mood-test:",mood#,"\n       wilcoxon-test:",wilcoxon,"\n"
        file0.close()



    file0=open(name00, 'at')
    print >> file0,"\n\n(number iterations for the bootstrap:",iterations,")"
    file0.close()
        


        
##########################
def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result



######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics_overlap_bootstrap.py path/network_file.gml"

    
