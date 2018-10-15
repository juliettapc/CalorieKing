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
import random



def main(graph_name):
  
    H = nx.read_gml(graph_name)
    


    print len(H.nodes())
  #dir=graph_name.split("fr")[0]
   # dir=graph_name.split("mas")[0]
    dir=graph_name.split("full_")[0]
   

    name=graph_name.split('network_no_bias/')[1]   
    name=name.split('.gml')[0]



  
    name00=name+"_average_percent_weight_change_per_kshell.dat"


 
    contador=3
    name12=dir+name+"_slopes_for_the_fits_average_weight_change.dat"           
    file=open(name12, 'at')
    file.close()


   # list_conn=[]
    #for node in H.nodes():  # i remove self loops
     #   if node in H.neighbors(node):          
      #      if len(H.neighbors(node))>1:
       #         H.remove_edge(node,node)             
        #    else:
         #       H.remove_node(node)              
        #try:
         #   list_conn.append(len(H.neighbors(node)))
        #except:
         #   pass 

    list_conn=[]
    for node in H.nodes():
        list_conn.append(len(H.neighbors(node)))
    max_connect=max(list_conn)



  #  for node in H.nodes():        
   #     if H.node[node]['weigh_ins'] <5: #Adherent filter
    #        H.remove_node(node)
           # print node, "is going down"






    G = nx.connected_component_subgraphs(H)[0] # Giant component 

   
    print "final size of the GC:",len(G.nodes())
      
    print "max connectivity:", max_connect

    cum_size_set=float(len(G.nodes()))

    list_of_lists_for_bootstrap=[]
    x_positions_fit=[]
    y_positions_fit=[]
   
    list_percent_weight_change_k_shell=[]
    for index in range (max_connect+1):     
         
        k_core=nx.algorithms.core.k_shell(G,k=index)
        if len (k_core)>0:

            num_users_set=cum_size_set

            #print"k-shell index:",index

            num_loosers=0
            for node in k_core:           
                list_percent_weight_change_k_shell.append(float(G.node[node]['percentage_weight_change']))

              #  if int(index)==12:#inner core
               #     G.node[node]['role']="inner_core"


                G.node[node]['kshell_index']=int(index)
                #print node, G.node[node]['kshell_index']
                if float(G.node[node]['percentage_weight_change'])<0.0:
                    num_loosers=num_loosers+1

                cum_size_set-=1.0


               
            print "\n",index,len(k_core),num_users_set/float(len(G.nodes())),numpy.mean(list_percent_weight_change_k_shell),numpy.std(list_percent_weight_change_k_shell)

            file0=open(name00, 'at')
            print >> file0,index,len(k_core),num_users_set/float(len(G.nodes())),numpy.mean(list_percent_weight_change_k_shell),numpy.std(list_percent_weight_change_k_shell),
                                                                 
            print  >> file0,stats.shapiro(list_percent_weight_change_k_shell)
#w entre 0 y 1 (normal si cerca de 1), p menor que 0.05 para normalidad
            

            file0.close()
           


            if len(x_positions_fit)<=7:
                x_positions_fit.append(index)
                y_positions_fit.append(numpy.mean(list_percent_weight_change_k_shell))

                list_of_lists_for_bootstrap.append(list_percent_weight_change_k_shell)
         


    slope, intercept, Corr_coef, p_value, std_err =stats.linregress(x_positions_fit,y_positions_fit)  # least squeares polinomial fit

    print "result linear. fit for kshell dependency:"
   
    print "slope:",slope, "intercept:", intercept, "Corr_coef:", Corr_coef, "p_value:", p_value, "std_err:", std_err



  
    name11=dir+name+"_fits_kshell.dat"
           
    file11=open(name11, 'wt')
    for i in range(len(x_positions_fit)):
        print >> file11,x_positions_fit[i],intercept+x_positions_fit[i]*slope

   

    print >> file11,"\n\n","y=",intercept,"+",slope,"*x",
    print   "Bootstrap for kshell:\n"
   
    mean_slope, standard_dev = bootstrap(x_positions_fit[0],x_positions_fit[-1],list_of_lists_for_bootstrap)
    zscore=(slope-mean_slope)/standard_dev

    print >> file11, "bootstrap:\n","actual slope:",slope,"mean_slope:",mean_slope,"standard_dev:",standard_dev,"\n zscore:",zscore


    print x_positions_fit[0],x_positions_fit[-1],"actual slope:",slope,"mean_slope:",mean_slope,"standard_dev:",standard_dev,"\n zscore:",zscore 

    file11.close()


   # print "size main k-core:",len(nx.algorithms.core.k_shell(G))




    contador+=1     
    file=open(name12, 'at')
    print >> file,contador,mean_slope,standard_dev, "kshell"
    file.close()








    list_nodes_kindex=[]
    for index in range (max_connect+1):  
        list=[]
        for node in G.nodes():
            if  G.node[node]['kshell_index']==index:
                list.append(node)
        if len(list)>0:
            list_nodes_kindex.append(list)




  
    name1=name+"_list_of_lists_kshells.dat"        
    file=open(name1, 'wt')
    print >> file,list_nodes_kindex   
    file.close()
    #print list_nodes_kindex   
        

    nx.write_gml(G,name1+"_inner_core.gml")
        
##########################
def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result


#############################################
def bootstrap(first_x,last_x,list_of_lists_for_bootstrap):
    
    last_x +=1
    x_positions=[]
    for x in range(first_x,last_x):
        x_positions.append(x)
        print x


    list_slopes=[]
    list_intersections=[]
    for iter in range (100):

        y_positions=[]
        for list in list_of_lists_for_bootstrap:
            if len(list)>1:
                list_synth=sample_with_replacement(list,len(list))
                y_positions.append(numpy.mean(list_synth))
            else:
                y_positions.append(numpy.mean(list_synth))

        
        slope, intercept, Corr_coef, p_value, std_err =stats.linregress(x_positions,y_positions)  # least squeares polinomial fit
        list_slopes.append(slope)
        list_intersections.append(intercept)


  

    return numpy.mean(list_slopes),numpy.std(list_slopes)

######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
