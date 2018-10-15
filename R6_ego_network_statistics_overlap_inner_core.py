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

    dir=dir+"roles/"
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

    #name=graph_name.split('data/')[1]
    name=graph_name.split('3method/')[1]


    name=name.split('.gml')[0]

    name0=dir+name+"_overlap_averages_"+str(time_in_system)+"days_exclude_inner_cores.dat"
    file0=open(name0, 'wt')    
    file0.close()
    



    list_R6s=[]     # collect the R6 of the system
    list_R6s_label=[]
    list_R6s_percent_weight_change=[] 
    for node in G.nodes() :    
        if str(G.node[node]['role']) == "inner_core" :
          list_R6s.append(node)
          list_R6s_label.append(G.node[node]['label'])
          list_R6s_percent_weight_change.append(float(G.node[node]['percentage_weight_change'])) 



    name00=dir+name+"_and_top_tens_averages_"+str(time_in_system)+"days_exclude_inner_cores.dat"
           
    file0=open(name00, 'at')
    print >> file0,"inner_cores",numpy.mean(list_R6s_percent_weight_change),numpy.std(list_R6s_percent_weight_change)
    file0.close()
    


   # print "\n\n inner_cores:\n"
    #for i in  list_R6s_label:
     #   print i


    
 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if str(G.node[n]['role']) == "inner_core" :
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)




   #####dose effect of the R6s independently########

    name11=dir+name+"_dose_eff_indepently_only_one_"+str(time_in_system)+"days_exclude_inner_cores.dat" 
    file11=open(name11, 'wt')   
    file11.close()






    list_weight_changes_no_neighbors=[]
    for node in G.nodes():
        resta=set(G.neighbors(node))-set(list_R6s)
        print node, resta
        if len(resta)==0:
            list_weight_changes_no_neighbors.append(G.node[node]['percentage_weight_change'])
       
    file11=open(name11, 'at')  
    print >> file11,0,"average_no_neighbors","average_no_neighbors","average_no_neighbors",len(list_weight_changes_no_neighbors),numpy.mean(list_weight_changes_no_neighbors),numpy.std(list_weight_changes_no_neighbors)
    file11.close()
    




    cont=1
    for R6 in list_R6s:
        list_weight_changes=[]
        for n in G.neighbors(R6):
            if (G.node[n]['role'] != "inner_core")  and ( G.node[n]["R6_overlap"]==1) :
                list_weight_changes.append(float(G.node[n]['percentage_weight_change']))

        if len(list_weight_changes)>0:

            file11=open(name11, 'at')  
            print >> file11,cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes),numpy.mean(list_weight_changes),numpy.std(list_weight_changes)
            file11.close()
            print cont,G.node[R6]['role'],G.node[R6]['label'], len(G.neighbors(R6)),len(list_weight_changes),numpy.mean(list_weight_changes),numpy.std(list_weight_changes)
            cont=cont+1

        else:
            file11=open(name11, 'at')  
            print >> file11,cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes)
            file11.close()
            print cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes)
            cont=cont+1



  ####################################





    for  r in range(len(list_R6s)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["R6_overlap"])==r:

              
                
                if G.node[node]["role"]== "inner_core":  # i exclude the R6s                    
                    
                    pass
                else:
                    
                    if int(G.node[node]['time_in_system']) > time_in_system:                                               
                        
                       
                        #list_BMI_changes.append(float(G.node[node]['final_BMI'])-float(G.node[node]['initial_BMI']))
                        list_weight_changes.append(float(G.node[node]['weight_change']))
                        list_percentage_weight_changes.append(float(G.node[node]['percentage_weight_change']))
                        list_activities.append(float(G.node[node]['activity'])/float(G.node[node]['time_in_system']))
                        

        if len(list_percentage_weight_changes)>0:
           # average_BMI_change=numpy.mean(list_BMI_changes)
            average_weight_change=numpy.mean(list_weight_changes)
            average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)
            average_activity=numpy.mean(list_activities)
            
           # deviation_BMI=numpy.std(list_BMI_changes)       
            deviation_weight=numpy.std(list_weight_changes)
            deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
            deviation_activity=numpy.std(list_activities) 


#print out
           
            file0=open(name0, 'at')
            print >> file0,r,len(list_percentage_weight_changes),average_percentage_weight_change,deviation_percentage_weight,average_weight_change,deviation_weight,average_activity,deviation_activity
            file0.close()
       





            
   #### averages for every R6's egonetwork:#########
    cont=1

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
          
      
        
       

        for n in G.neighbors(node):
           
            if int(G.node[n]['time_in_system']) > time_in_system:
               
                         
                
               # list_BMI_changes.append(float(G.node[n]['final_BMI'])-float(G.node[n]['initial_BMI']))
                               
                list_weight_changes.append(float(G.node[n]['weight_change']))


                list_percentage_weight_changes.append(float(G.node[n]['percentage_weight_change']))

                                             
                list_activities.append(float(G.node[n]['activity'])/float(G.node[n]['time_in_system']))


 
      

#averages 
        average_weight_change=numpy.mean(list_weight_changes)
       # average_BMI_change=numpy.mean(list_BMI_changes)
        average_activity=numpy.mean(list_activities)
        average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)

      
#standard deviation
      #  deviation_BMI=numpy.std(list_BMI_changes)       
        deviation_weight=numpy.std(list_weight_changes)
        deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        




#print out
       # name1=dir+name+"_ego_average_BMI_change_"+str(time_in_system)+"days.dat"
        #file1=open(name1, 'at')
        #print >> file1,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_BMI_change,deviation_BMI
        #file1.close()


        name2=dir+name+"_ego_average_weight_change_"+str(time_in_system)+"days.dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_weight_change,deviation_weight
        file2.close()


        name22=dir+name+"_ego_average_percentage_weight_change_"+str(time_in_system)+"days.dat"
        file22=open(name22, 'at')
        print >> file22,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_percentage_weight_change,deviation_percentage_weight
        file22.close()


        name3=dir+name+"_ego_average_activity_"+str(time_in_system)+"days.dat"
        file3=open(name3, 'at')
        print >> file3,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_activity,deviation_activity
        file3.close()


       # name4=dir+name+"_ego_dispersions_"+str(time_in_system)+"days.dat"
        #file4=open(name4, 'at')
        #for i in range(len(list_activities)):
         #   print >> file4,cont, list_BMI_changes[i],list_weight_changes[i],list_activities[i]
        #print >> file4,"\n\n" #to separate roles
        #file4.close()




        cont=cont+1





       #############just checking what happens if we remove the 40155 guy


    cont=0
    for n in G.nodes():
        if len(G.neighbors(n))==0:
            cont=cont+1            
    #print "# friendless guys before:", cont



    for  n in G.nodes():
        if G.node[n]['label']=="40155": 
            G.remove_node(n)
            break

    cont=0
    for n in G.nodes():
        if len(G.neighbors(n))==0:
            cont=cont+1
    #print "# friendless guys after:", cont



######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
