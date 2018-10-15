#!/usr/bin/env python

"""
Created by Julia Poncela on March 2010

Given a network.gml (with role attributes) it calculates averages and standard deviation of
weight change, BMI change and activity for all N6's neighbors, depending on 
how many R6s you are connected to.

It takes as argument the path/network.gml  and creates a buch of files: ptha/roles/ego_R6s_average_weight_change300.txt,  and overlap_R6s_averages...dat


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
  
   
    dir=graph_name.split("mas")[0]
    #dir=graph_name.split("fr")[0]

    original_name=graph_name.split("data/")[1]
    original_name=original_name.split(".gml")[0]

    dir=dir+"roles/"+original_name

   
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

##OJO!!! THE .GML FILE DOESNT HAVE A NUMBER-OF-DAYS-IN-THE-SYSTEM THRESHOLD PER SE!!!


    
# R6s en friend_graph_all.gml: 40155, 28688, 45784, 41794, 43020, 47063, 39625, 31954, 40324,40666 
    


#R6s en master_adherent_homo.gml: 40155, 41794, 39625, 46487, 31954, 40324, 28688, 45784, 40666


    R6_to_exclude  = '28688'


    name_aux=graph_name.split("/data")[1]
    name_aux=graph_name.split(".gml")[0]
 
    name0=dir+"_overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s_not_considering_"+str(R6_to_exclude)+".dat"
    file0=open(name0, 'wt')    
    file0.close()
    



    list_R6s=[]     # collect the R6 of the system
#BUT EXCLUDING ONE R6 EVERYTIME (TO CHECK WHAT GOING ON WITH THE 900-FRIEND GUY)
    for node in G.nodes() :    
      if (str(G.node[node]['role']) == "R6" ) and (str(G.node[node]['label']) !=  R6_to_exclude  ) :
          list_R6s.append(node)






 # studying the possible cumulative effect of more than one R6 on the population:
#BUT EXCLUDING ONE R6 EVERYTIME (TO CHECK WHAT GOING ON WITH THE 900-FRIEND GUY)
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if (str(G.node[n]['role']) == "R6") and (str(G.node[n]['label']) !=  R6_to_exclude  ):
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)




    for  r in range(len(list_R6s)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]


        for node in G.nodes():

            if int(G.node[node]["R6_overlap"])==r:

              
                
                if G.node[node]["role"]== "R6":  # i exclude the R6s per se                   
                    
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
        
        average_BMI_change=0.0               
        list_BMI_changes=[]
        
        average_weight_change=0.0       
        list_weight_changes=[]

        average_percentage_weight_change=0.0       
        list_percentage_weight_changes=[]
          
          
        average_activity=0.0     # ojo! sera dividida por el numero de dias!!!!!
        list_activities=[]
          
        eff_degree=0
        
       

        for n in G.neighbors(node):
           
            if int(G.node[n]['time_in_system']) > time_in_system:
               
                eff_degree=eff_degree+1.0                
                
                list_BMI_changes.append(float(G.node[n]['final_BMI'])-float(G.node[n]['initial_BMI']))
                               
                list_weight_changes.append(float(G.node[n]['weight_change']))

                list_percentage_weight_changes.append(float(G.node[n]['percentage_weight_change']))
               
                              
                list_activities.append(float(G.node[n]['activity'])/float(G.node[n]['time_in_system']))               


 
      

#averages 
        average_weight_change=numpy.mean(list_weight_changes)
        average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)
        average_BMI_change=numpy.mean(list_BMI_changes)
        average_activity=numpy.mean(list_activities)


      
#standard deviation
        deviation_BMI=numpy.std(list_BMI_changes)       
        deviation_weight=numpy.std(list_weight_changes)
        deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        

       # print cont,"R6: ",average_weight_change,deviation_weight,average_BMI_change,deviation_BMI,average_activity,deviation_activity




#print out
        name1=dir+"_ego_R6s_average_BMI_change_"+str(time_in_system)+"days_not_considering_"+str(R6_to_exclude)+".dat"
        file1=open(name1, 'at')
        print >> file1,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_BMI_change,deviation_BMI#,list_BMI_changes
        file1.close()


        name2=dir+"_ego_R6s_average_weight_change_"+str(time_in_system)+"days_not_considering_"+str(R6_to_exclude)+".dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_weight_change,deviation_weight#,list_weight_changes
        file2.close()


        name2=dir+"_ego_R6s_average_percentage_weight_change_"+str(time_in_system)+"days_not_considering_"+str(R6_to_exclude)+".dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_percentage_weight_change,deviation_percentage_weight#,list_weight_changes
        file2.close()
        

        name3=dir+"_ego_R6s_average_activity_"+str(time_in_system)+"days_not_considering_"+str(R6_to_exclude)+".dat"
        file3=open(name3, 'at')
        print >> file3,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_activity,deviation_activity#,list_activities
        file3.close()


        name4=dir+"_ego_R6s_dispersions_"+str(time_in_system)+"days_not_considering_"+str(R6_to_exclude)+".dat"
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

    
