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
    dir=graph_name.split("master")[0]
    dir=dir+"roles/"
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

    name=graph_name.split('data/')[1]
    name=name.split('.gml')[0]

    name0=dir+name+"_overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s_union_sets_larger5.dat"
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



    name=dir+name+"_ID_percentWC_number_R6s.dat"           
    file=open(name, 'wt')
    for n in G.nodes():
        if str(G.node[n]['role']) == "R6" :
            pass
        else:
            list=[]
            list.append(str(G.node[n]['label']))
            list.append(str(float(G.node[n]['final_BMI'])-float(G.node[n]['initial_BMI'])))
            list.append(str(G.node[n]['percentage_weight_change']))           
            list.append(str(G.node[n]['R6_overlap']))
       
            print >> file,",".join(list)
       

    file.close()




    for  r in range(len(list_R6s)+1):    
       
        if r <=5:

            list_BMI_changes=[]               
            list_weight_changes=[]                
            list_percentage_weight_changes=[]    
            list_activities=[]
            
            
            for node in G.nodes():
                
                if int(G.node[node]["R6_overlap"])==r:
                    
                    
                    
                    if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                        
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
            


   #overlap larger or equal to 6:

    list_BMI_changes=[]               
    list_weight_changes=[]                
    list_percentage_weight_changes=[]    
    list_activities=[]
            
            
    for node in G.nodes():   
        
        if int(G.node[node]["R6_overlap"])>=6:                                                  
            
            if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                
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
    print >> file0,6,len(list_BMI_changes),average_percentage_weight_change,deviation_percentage_weight,average_BMI_change,deviation_BMI,average_weight_change,deviation_weight,average_activity,deviation_activity
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




######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
