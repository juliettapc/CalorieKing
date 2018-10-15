#!/usr/bin/env python

"""
Created by Julia Poncela on March 2010

Given a network.gml (with role attributes) it calculates averages and standar deviation of
weight change, BMI change and activity for all N6's egonetworks.

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
  
   


    dir=graph_name.split("fr")[0]
    dir=dir+"roles/"
   

    time_in_system=200  #minimum amount of time in the sytem for a user to be included in the statistics


    cont=1

    list_R6s=[]
    for node in G.nodes() :    
      if str(G.node[node]['role']) == "R6" :
          list_R6s.append(node)



    for node in list_R6s:  
        neighbors=G.neighbors(node)#a list of nodes               
        
        average_BMI_change=0.0               
        list_BMI_changes=[]
        
        average_weight_change=0.0       
        list_weight_changes=[]
          
        average_activity=0.0     # ojo! sera dividida por el numero de dias!!!!!
        list_activities=[]
          
        eff_degree=0
        
       

        for n in G.neighbors(node):
           
            if int(G.node[n]['time_in_system']) > time_in_system:
               
                eff_degree=eff_degree+1.0                
                
                list_BMI_changes.append(float(G.node[n]['final_BMI'])-float(G.node[n]['initial_BMI']))
                               
                list_weight_changes.append(float(G.node[n]['weight_change']))
               
                              
                list_activities.append(float(G.node[n]['activity'])/float(G.node[n]['time_in_system']))               



                #print float(G.node[n]['final_BMI'])-float(G.node[n]['initial_BMI']),float(G.node[n]['weight_change']),float(G.node[n]['activity'])/float(G.node[n]['time_in_system'])
                
                
           

#averages 
        average_weight_change=sum(list_weight_changes)/eff_degree
        average_BMI_change=sum(list_BMI_changes)/eff_degree
        average_activity=sum(list_activities)/eff_degree


        print cont,"R6: ",average_weight_change,average_BMI_change,average_activity

#standard deviation
        deviation_BMI=0.0 
        for i in list_BMI_changes:    
            deviation_BMI=deviation_BMI +(i - average_BMI_change)**2       
                    
        deviation_BMI=deviation_BMI/eff_degree
        deviation_BMI=sqrt(deviation_BMI)
       


        deviation_weight=0.0 
        for i in list_weight_changes:    
            deviation_weight=deviation_weight +(i - average_weight_change)**2       
        
        deviation_weight=deviation_weight/eff_degree
        deviation_weight=sqrt(deviation_weight)
       


        deviation_activity=0.0 
        for i in list_activities:    
            deviation_activity=deviation_activity +(i - average_activity)**2       
        
        deviation_activity=deviation_activity/eff_degree
        deviation_activity=sqrt(deviation_activity)




#print out
        name1=dir+"ego_R6s_average_BMI_change_"+str(time_in_system)+"days.dat"
        file1=open(name1, 'at')
        print >> file1,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_BMI_change,deviation_BMI#,list_BMI_changes
        file1.close()


        name2=dir+"ego_R6s_average_weight_change_"+str(time_in_system)+"days.dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_weight_change,deviation_weight#,list_weight_changes
        file2.close()


        name3=dir+"ego_R6s_average_activity_"+str(time_in_system)+"days.dat"
        file3=open(name3, 'at')
        print >> file3,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_activity,deviation_activity#,list_activities
        file3.close()


        name4=dir+"ego_R6s_dispersions_"+str(time_in_system)+"days.dat"
        file4=open(name4, 'at')
        for i in range(len(list_activities)):
            print >> file4,cont, list_BMI_changes[i],list_weight_changes[i],list_activities[i]
        print >> file4,"\n\n" #to separate roles
        file4.close()




        cont=cont+1




######################################3
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
