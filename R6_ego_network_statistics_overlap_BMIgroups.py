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
  


    H = nx.read_gml(graph_name)   
    G = nx.connected_component_subgraphs(H)[0] # Giant component 
  
   #clasify the users  that belong to the network into BMI categories:

    for node in G.nodes():
        if (float(G.node[node]['initial_BMI']) >30): #obese
            G.node[node]['BMI_group']='obese'

        elif (float(G.node[node]['initial_BMI'])>25) and(float(G.node[node]['initial_BMI']) <30): #overweighted
            G.node[node]['BMI_group']='overweighted'
                                                            
        elif (float(G.node[node]['initial_BMI']) < 25) and (float(G.node[node]['initial_BMI'])> 18.5): #normal   
            G.node[node]['BMI_group']='normal'
            
        elif (float(G.node[node]['initial_BMI'])< 18.5): #underweighted group   
            G.node[node]['BMI_group']='underweighted'


         
        #print node, H.node[node]['initial_BMI'],H.node[node]['BMI_group']
   
    list_BMIgroups=['obese','overweighted','normal','underweighted']




    dir=graph_name.split("fr")[0]
    dir=dir+"roles/"
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics



    list_R6s=[]     # collect the R6 of the system
    for node in G.nodes() :    
      if str(G.node[node]['role']) == "R6" :
          list_R6s.append(node)





 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if str(G.node[n]['role']) == "R6" :
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)



    for  BMIgroup in list_BMIgroups:


        for  r in range(len(list_R6s)+1):    
       
            list_BMI_changes=[]               
            list_weight_changes=[]                
            list_activities=[]


            for node in G.nodes():

                if (int(G.node[node]["R6_overlap"])==r) and (G.node[node]["BMI_group"]==BMIgroup):

              
                
                    if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                    
                        pass
                    else:
                    
                        if int(G.node[node]['time_in_system']) > time_in_system:                                               
                        
                       
                            list_BMI_changes.append(float(G.node[node]['final_BMI'])-float(G.node[node]['initial_BMI']))
                            list_weight_changes.append(float(G.node[node]['weight_change']))
                            list_activities.append(float(G.node[node]['activity'])/float(G.node[node]['time_in_system']))
               

            if len(list_BMI_changes)>0:
                average_BMI_change=numpy.mean(list_BMI_changes)
                average_weight_change=numpy.mean(list_weight_changes)
                average_activity=numpy.mean(list_activities)
                           
                deviation_BMI=numpy.std(list_BMI_changes)       
                deviation_weight=numpy.std(list_weight_changes)
                deviation_activity=numpy.std(list_activities) 


#print out
                name0=dir+"overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s_"+str(BMIgroup)+".dat"
                file0=open(name0, 'at')
                print >> file0,r,len(list_BMI_changes),average_BMI_change,deviation_BMI,average_weight_change,deviation_weight,average_activity,deviation_activity
                file0.close()












#  averages for the neighbors of a given R6 ########


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


 
      

#averages 
        average_weight_change=numpy.mean(list_weight_changes)
        average_BMI_change=numpy.mean(list_BMI_changes)
        average_activity=numpy.mean(list_activities)


      
#standard deviation
        deviation_BMI=numpy.std(list_BMI_changes)       
        deviation_weight=numpy.std(list_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        

       # print cont,"R6: ",average_weight_change,deviation_weight,average_BMI_change,deviation_BMI,average_activity,deviation_activity




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

    
