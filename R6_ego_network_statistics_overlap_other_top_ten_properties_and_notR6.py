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

    name0=dir+name+"_overlap_top_ten_"+str(top_ten_feature)+"_averages_"+str(time_in_system)+"days_excluding_themselves_and_notR6s.dat"
    file0=open(name0, 'wt')    
    file0.close()
    


    name220=dir+name+"_overlap_top_ten_"+str(top_ten_feature)+"_averages_"+str(time_in_system)+"days_excluding_themselves_and_andR6s.dat"
    file220=open(name220, 'wt')    
    file220.close()
    


    R6_to_exclude  = '40155'


    list_top_tens=[] 

    list_top_tens_notR6s=[]     # collect the top_tens of the system
    list_top_tens_notR6s_percent_weight_change=[] 
    list_top_tens_andR6s=[]     # collect the top_tens of the system
    list_top_tens_andR6s_percent_weight_change=[] 


    f = lambda x:x[1][top_ten_feature]
    membership = map(f,G.nodes(data=True))
    membership.sort()
    top_ten_values = membership[-10:]  #TOP TEN

   # print top_ten_values # the sorted top-tens: from smallest to largest
    #print membership  #the whole sorted list



    cont=0
    for value in top_ten_values:
        for node in G.nodes():
            if (G.node[node][top_ten_feature]==value) and (node not in list_top_tens):
                list_top_tens.append(node)

                if G.node[node]['role']!="R6":  #top ten, but not R6
                    #print node, G.node[node]['role']
                   
                    list_top_tens_notR6s.append(node)
                    list_top_tens_notR6s_percent_weight_change.append(float(G.node[node]['percentage_weight_change']))              
                 
                elif (G.node[node]['role']=="R6") and (str(G.node[node]['label']) !=  R6_to_exclude  ):  #top ten and R6
                    list_top_tens_andR6s.append(node)

                    list_top_tens_andR6s_percent_weight_change.append(float(G.node[node]['percentage_weight_change']))      
                    break  
# if there are more than 10, it will pick just the first 10 according to their id


   



    for node in list_top_tens_andR6s:
        print G.node[node]['label'],G.node[node][top_ten_feature], len(G.neighbors(node)), G.node[node]['Pi'], G.node[node]['zi']
        
    print "\n"

    for node in list_top_tens_notR6s:
        print G.node[node]['label'],G.node[node][top_ten_feature], len(G.neighbors(node)), G.node[node]['Pi'], G.node[node]['zi']

      
   
 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in G.neighbors(node):
            if (n in list_top_tens_notR6s) :
                cont+=1

        G.node[node]["top_ten_notR6_overlap"]=int(cont)

        cont=0
        for n in G.neighbors(node):
            if (n in list_top_tens_andR6s) :
                cont+=1

        G.node[node]["top_ten_andR6_overlap"]=int(cont)


    for  r in range(len(list_top_tens_notR6s)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["top_ten_notR6_overlap"])==r:
                              
                if node in list_top_tens_notR6s:  # i exclude the top_tens per se
                    
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
            
            





    for  r in range(len(list_top_tens_andR6s)+1):    
       
        list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        

        for node in G.nodes():

            if int(G.node[node]["top_ten_andR6_overlap"])==r:

              
                
                if node in list_top_tens_andR6s:  # i exclude the top_tens per se
                    
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
           
            file220=open(name220, 'at')
            print >> file220,r,len(list_BMI_changes),average_percentage_weight_change,deviation_percentage_weight,average_BMI_change,deviation_BMI,average_weight_change,deviation_weight,average_activity,deviation_activity
            file220.close()
            
            












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


#  averages for the neighbors of a given top-ten ########


    for node in list_top_tens:  
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
        deviation_percentage_weight=numpy.std(list_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        

       # print cont,"R6: ",average_weight_change,deviation_weight,average_BMI_change,deviation_BMI,average_activity,deviation_activity




#print out
        name1=dir+"ego_top_ten_"+str(top_ten_feature)+"_average_BMI_change_"+str(time_in_system)+"days.dat"
        file1=open(name1, 'at')
        print >> file1,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_BMI_change,deviation_BMI#,list_BMI_changes
        file1.close()


        name2=dir+"ego_top_ten_"+str(time_in_system)+"_average_weight_change_"+str(time_in_system)+"days.dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_weight_change,deviation_weight#,list_weight_changes
        file2.close()


        name3=dir+"ego_top_ten_"+str(top_ten_feature)+"_average_activity_"+str(time_in_system)+"days.dat"
        file3=open(name3, 'at')
        print >> file3,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),eff_degree,average_activity,deviation_activity#,list_activities
        file3.close()


        name4=dir+"ego_top_ten_"+str(top_ten_feature)+"_dispersions_"+str(time_in_system)+"days.dat"
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

    
