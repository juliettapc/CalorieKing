#!/usr/bin/env python

"""
Created by Julia Poncela on March 2010

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
 
def main(graph_name):
  
    G = nx.read_gml(graph_name)
    G = nx.connected_component_subgraphs(G)[0] # Giant component 
  
   
    #dir=graph_name.split("fr")[0]
    dir=graph_name.split("mast")[0]  
    dir=dir+"roles/"

    name=graph_name.split(".gml")[0]  
    name=name.split("data/")[1]  


    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics



# clustering, vitality, activity, betweenness, weigh_ins, degree, time_in_system

    top_ten_feature='time_in_system'





    print "\n\n",top_ten_feature

    name0=dir+name+"_overlap_top_ten_"+str(top_ten_feature)+"_averages_"+str(time_in_system)+"days_excluding_themselves_and_noneR6s.dat"
    file0=open(name0, 'wt')    
    file0.close()
    



    f = lambda x:x[1][top_ten_feature]
    membership = map(f,G.nodes(data=True))
    membership.sort()
    top_ten_values = membership[-10:]  #TOP TEN

  


    list_top_tens=[] 
    for value in top_ten_values:
        for node in G.nodes():
            if (G.node[node][top_ten_feature]==value) and (node not in list_top_tens):
                list_top_tens.append(node)  
                G.node[node]["role"]="R6_aceptable"
                break
# if there are more than 10, it will pick just the first 10 according to their id


   



    for node in list_top_tens:
        print G.node[node]['label'],G.node[node]['role'],G.node[node][top_ten_feature], len(G.neighbors(node)), G.node[node]['Pi'], G.node[node]['zi']
        
   




    for node in G.nodes():
        cont=0
        for n in G.neighbors(node):
            if str(G.node[n]["role"])== "R6" :
                cont+=1
                
        G.node[node]["R6s_overlap"]=int(cont)


   
 # studying the possible cumulative effect of more than one top ten in your neighborhood:
    for node in G.nodes():
        cont=0
        if int(G.node[node]["R6s_overlap"])==0:
            for n in G.neighbors(node):
                if (n in list_top_tens) :
                    cont+=1

        G.node[node]["overlap_top_ten_and_noneR6s"]=int(cont)

       

    for  r in range(len(list_top_tens)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["overlap_top_ten_and_noneR6s"])==r:
                              
                if node in list_top_tens:  # i exclude the top_tens per se
                    
                    pass
                else:
                    
                    if int(G.node[node]['time_in_system']) > time_in_system:                  
                        
                       
                        list_BMI_changes.append(float(G.node[node]['final_BMI'])-float(G.node[node]['initial_BMI']))
                        list_weight_changes.append(float(G.node[node]['weight_change']))
                        list_percentage_weight_changes.append(float(G.node[node]['percentage_weight_change']))
                        list_activities.append(float(G.node[node]['activity'])/float(G.node[node]['time_in_system']))
                        

        if len(list_BMI_changes)>0:
            average_BMI_change=numpy.mean(list_BMI_changes)
            average_weight_change=numpy.mean(list_weight_changes)
            average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)
            average_activity=numpy.mean(list_activities)
            
            deviation_BMI=numpy.std(list_BMI_changes)       
            deviation_weight=numpy.std(list_weight_changes)
            deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
            deviation_activity=numpy.std(list_activities) 


#print out
           
            file0=open(name0, 'at')
            print >> file0,r,len(list_BMI_changes),average_percentage_weight_change,deviation_percentage_weight,average_BMI_change,deviation_BMI,average_weight_change,deviation_weight,average_activity,deviation_activity
            file0.close()
            
            








######################################3
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
