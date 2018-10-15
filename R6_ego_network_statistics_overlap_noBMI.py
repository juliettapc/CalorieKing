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
    #dir=graph_name.split("master")[0]
    dir=graph_name.split("method_3")[0]

   # dir=dir+"roles/"
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

    #name=graph_name.split('data/')[1]
    name=graph_name.split('3method/')[1]


    name=name.split('.gml')[0]

    name0=dir+name+"_overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s.dat"
    file0=open(name0, 'wt')    
    file0.close()
    



    list_R6s=[]     # collect the R6 of the system
    list_R6s_label=[]
    list_R6s_percent_weight_change=[] 
    for node in G.nodes() :    
        if str(G.node[node]['role']) == "R6" :
          list_R6s.append(node)
          list_R6s_label.append(G.node[node]['label'])
          list_R6s_percent_weight_change.append(float(G.node[node]['percentage_weight_change'])) 



     
    name00=dir+name+"R6s_and_top_tens_averages_"+str(time_in_system)+"days_exclude_R6s.dat"
           
    file0=open(name00, 'at')
    print >> file0,"R6s",numpy.mean(list_R6s_percent_weight_change),numpy.std(list_R6s_percent_weight_change)
    file0.close()
    


    print "\n\n R6s:\n"
    for i in  list_R6s_label:
        print i

 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if str(G.node[n]['role']) == "R6" :
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)



    for  r in range(len(list_R6s)+1):    
       
               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["R6_overlap"])==r:

              
                
                if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                    
                    pass
                else:
                    
                    if int(G.node[node]['time_in_system']) > time_in_system:                                               
                        
                       
                       
                        list_weight_changes.append(float(G.node[node]['weight_change']))
                        list_percentage_weight_changes.append(float(G.node[node]['percentage_weight_change']))
                        list_activities.append(float(G.node[node]['activity'])/float(G.node[node]['time_in_system']))
                        

        if len(list_weight_changes)>0:           
            average_weight_change=numpy.mean(list_weight_changes)
            average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)
            average_activity=numpy.mean(list_activities)
            
           
            deviation_weight=numpy.std(list_weight_changes)
            deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
            deviation_activity=numpy.std(list_activities) 


#print out
           
            file0=open(name0, 'at')
            print >> file0,r,len(list_weight_changes),average_percentage_weight_change,deviation_percentage_weight,average_weight_change,deviation_weight,average_activity,deviation_activity
            file0.close()
       





            


           # print "\n",r,max(list_weight_changes),min(list_weight_changes)
            #raw_input()


            #Num_bins=int(max(list_weight_changes)-min(list_weight_changes)/10.0)
            #hist= numpy.histogram(list_weight_changes, bins=Num_bins)
           

            #name0=dir+"histograms_weight_"+str(time_in_system)+"days_exclude_R6s.dat"
            #file0=open(name0, 'at')
           
            #for elem in range(len(hist[0])):
                                
             #    print  hist[1][elem+1],hist[0][elem]
              #   print  (hist[1][elem]+hist[1][elem+1])/2.0,hist[0][elem]

            #print >> file0, "\n" # to separate sets
            #file0.close()


#  averages for the neighbors of a given R6 ########


    for node in list_R6s:  
        neighbors=G.neighbors(node)#a list of nodes               
        
       
        
        average_weight_change=0.0       
        list_weight_changes=[]
          
        average_activity=0.0     # ojo! sera dividida por el numero de dias!!!!!
        list_activities=[]
          
        eff_degree=0
        
       

        for n in G.neighbors(node):
           
            if int(G.node[n]['time_in_system']) > time_in_system:
               
                eff_degree=eff_degree+1.0                
                
               
                               
                list_weight_changes.append(float(G.node[n]['weight_change']))
               
                              
                list_activities.append(float(G.node[n]['activity'])/float(G.node[n]['time_in_system']))               


 
      

#averages 
        average_weight_change=numpy.mean(list_weight_changes)       
        average_activity=numpy.mean(list_activities)


      
#standard deviation       
        deviation_weight=numpy.std(list_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        

      

#print out
      
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
            print >> file4,cont,list_weight_changes[i],list_activities[i]
        print >> file4,"\n\n" #to separate roles
        file4.close()




        cont=cont+1




######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
