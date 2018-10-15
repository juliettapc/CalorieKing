#!/usr/bin/env python

"""
Created by Julia Poncela on May 2011

Given a network.gml (with attributes) it calculates averages and standard 
deviation of percentage weight change as a function of the k-shell index of the set.

It takes as argument the path/network.gml  


"""

import sys
import networkx as nx
from  scipy import stats
import numpy

def main(graph_name):
  
    H = nx.read_gml(graph_name)
    

  #dir=graph_name.split("fr")[0]
   # dir=graph_name.split("mas")[0]

    name00=graph_name.split(".gml")[0]
    print type(name00)
    name00=name00+"_average_percent_weight_change_per_kshell_clinically_signif.dat"

 



    list_conn=[]
    for node in H.nodes():  # i remove self loops
        if node in H.neighbors(node):          
            if len(H.neighbors(node))>1:
                H.remove_edge(node,node)             
            else:
                H.remove_node(node)              
        try:
            list_conn.append(len(H.neighbors(node)))
        except:
            pass 


    max_connect=max(list_conn)



    for node in H.nodes():        
        if H.node[node]['weigh_ins'] <5: #Adherent filter
            H.remove_node(node)
           # print node, "is going down"





    G = nx.connected_component_subgraphs(H)[0] # Giant component 

   
    print "final size of the GC:",len(G.nodes())
    
  



    cum_size_set=float(len(G.nodes()))
    
   
    list_percent_weight_change_k_shell=[]
    for index in range (max_connect+1):     
         
        k_core=nx.algorithms.core.k_shell(G,k=index)
        if len (k_core)>0:

            num_users_set=cum_size_set


            num_users_clinically_signif=0.0     

           
           
            for node in k_core:           
                list_percent_weight_change_k_shell.append(float(G.node[node]['percentage_weight_change']))

                if int(index)==12:#inner core
                    G.node[node]['role']="inner_core"


                G.node[node]['kshell_index']=int(index)
                #print node, G.node[node]['kshell_index']
               

                cum_size_set-=1.0


                if G.node [node]['percentage_weight_change']<=-5.0:
                    num_users_clinically_signif+=1.0

               
            print "\n",index,len(k_core),num_users_set/float(len(G.nodes())),num_users_clinically_signif/len(list_percent_weight_change_k_shell),numpy.mean(list_percent_weight_change_k_shell),numpy.std(list_percent_weight_change_k_shell)

            file0=open(name00, 'at')
            print >> file0,index,len(k_core),num_users_set/float(len(G.nodes())),num_users_clinically_signif/len(list_percent_weight_change_k_shell),numpy.mean(list_percent_weight_change_k_shell),numpy.std(list_percent_weight_change_k_shell),
                                                                 
            print  >> file0,stats.shapiro(list_percent_weight_change_k_shell)
#w entre 0 y 1 (normal si cerca de 1), p menor que 0.05 para normalidad
            

            file0.close()
           

           

   # print "size main k-core:",len(nx.algorithms.core.k_shell(G))


    list_nodes_kindex=[]
    for index in range (max_connect+1):  
        list=[]
        for node in G.nodes():
            if  G.node[node]['kshell_index']==index:
                list.append(node)
        if len(list)>0:
            list_nodes_kindex.append(list)




    name1=graph_name.split(".gml")[0]
    name=name1+"_list_of_lists_kshells.dat"        
    file=open(name, 'wt')
    print >> file,list_nodes_kindex   
    file.close()
    #print list_nodes_kindex   
        

    nx.write_gml(G,name1+"_inner_core.gml")


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
