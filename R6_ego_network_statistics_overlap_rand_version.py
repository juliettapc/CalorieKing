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
import random



def main(graph_name):
  



    dir=graph_name.split("master")[0]   
    dir=dir+"roles/"
   

    time_in_system=100 #minimum amount of time in the sytem for a user to be included in the statistics

    name=graph_name.split('data/')[1] #for methods 1 and 2   
    name=name.split('.gml')[0]


    name0=dir+name+"_overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s_rand_version.dat"
    file0=open(name0, 'wt')    
    file0.close()







    H = nx.read_gml(graph_name)  
   
    H= nx.connected_component_subgraphs(H)[0] # i take the GC

  
    for node in H.nodes():  # i remove self loops
        if node in H.neighbors(node):          
            if len(H.neighbors(node))>1:
                H.remove_edge(node,node)             
            else:
                H.remove_node(node)              


  

    G= randomize_network(H)  # i randomize the network

    nx.write_gml(G,"5_points_network_2010/data/master_adherent_homo_rand_version.gml")


   
    cont_newR1=0
    for node in G.nodes(): 
          
       
      
        try:
            print node, G.node[node]['role']


           # G.node[node]['role']=str(H.node[node]['role'])
        except KeyError:
            print "node", node, "doesnt have label or role"

            G.node[node]['role']="R1"            
            cont_newR1=cont_newR1+1




  
       # G.node[node]['label']=int(H.node[node]['label'] )
        #G.node[node]['percentage_weight_change']=float(H.node[node]['percentage_weight_change'])
        #G.node[node]['weigh_ins']=int(H.node[node]['weigh_ins'])
        #G.node[node]['final_BMI']=float(H.node[node]['final_BMI'])
        #G.node[node]['initial_BMI']=float(H.node[node]['initial_BMI'])
        #G.node[node]['time_in_system']=int(H.node[node]['time_in_system'])
        #G.node[node]['weight_change']=float(H.node[node]['weight_change'])
        #G.node[node]['activity']=float(H.node[node]['activity'])
        #G.node[node]['degree']=int(len(G.neighbors(node)))

        #print node, G.node[node]['label'],G.node[node]['role']
       
    print "\n# new R1s",cont_newR1,"# users",len(G.nodes())

 
 

    list_R6s=[]     # collect the R6 of the system   
    list_R6s_percent_weight_change=[] 
   

    for node in G.nodes():
        if G.node[node]['role']=="R6":
            list_R6s.append(node)           
            list_R6s_percent_weight_change.append(G.node[node]['percentage_weight_change'])
            print node,G.node[node]['role']

     
    name00=dir+name+"R6s_and_top_tens_averages_"+str(time_in_system)+"days_exclude_R6s_rand_version.dat"           
    file0=open(name00, 'at')
    print >> file0,"R6s",numpy.mean(list_R6s_percent_weight_change),numpy.std(list_R6s_percent_weight_change)
    file0.close()
    



 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if str(G.node[n]['role']) == "R6" :
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)
       



    for  r in range(len(list_R6s)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["R6_overlap"])==r:

              
                
                if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                    
                    pass
                else:
                    
                                           
                        
                       
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






        cont=cont+1




def randomize_network(H):

    num_iter=len(H.edges())*500
    num_nodes=len(H.nodes())
    list_nodes=H.nodes()

    for i in range(num_iter): # number of iterations for the link ramdomization
        x1=int(random.random()*num_nodes)
        node1=list_nodes[x1]
        
        x2=int(random.random()*len(H.neighbors(node1)))
        list_neighbors=H.neighbors(node1)
        node2=list_neighbors[x2]




        x3=int(random.random()*num_nodes)
        node3=list_nodes[x3]
       
        x4=int(random.random()*len(H.neighbors(node3)))
        list_neighbors=H.neighbors(node3)
        node4=list_neighbors[x4]


        #print node1,"-",node2,"   ",node3,"-",node4

        if (node1!=node4) and  (node2!=node3):
            if (node1 not in H.neighbors(node4)) and (node2 not in H.neighbors(node3)):

                H.remove_edge(node1,node2)
                H.remove_edge(node3,node4)

                H.add_edge(node1,node4)
                H.add_edge(node2,node3)

               # print node1,"-",node2,"   ",node3,"-",node4


            

    return H




######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_name = sys.argv[1]
        main(graph_name)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
