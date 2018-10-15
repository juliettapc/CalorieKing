#!/usr/bin/env python

"""
Created by Julia Poncela on March 2011

Given a network.gml (with role attributes) it calculates averages and standard deviation of
weight change, BMI change and activity for all R6's neighbors, as a function of 
how many R6s you are connected to.

It takes as argument the path/network.gml  and creates a buch of files: ego_R6s_average_weight_change300.txt, 


"""

import sys
import os
import networkx as nx
import math
from pylab import *
import numpy
from  scipy import stats
import random
from transform_labels_to_nx import transform_labels_to_nx

 
def main(graph_name):
  
    H = nx.read_gml(graph_name)

    H = transform_labels_to_nx(H)      

    Graph_full_info = nx.read_gml("./5_points_network_2010/data/full_network_all_users_no_selfloops_merged_small_comm_roles_diff_layers1.5.gml")
  
    Graph_full_info = transform_labels_to_nx(Graph_full_info) 

# i transform labels into id for both networks, so the nodes match.



    for node in H.nodes():  # i remove self loops
        if node in H.neighbors(node):          
            if len(H.neighbors(node))>1:
                H.remove_edge(node,node)             
            else:
                H.remove_node(node)              

        
       # print H.neighbors(node), Graph_full_info.neighbors(node), len(H.neighbors(node)), len(Graph_full_info.neighbors(node))
        

        H.node[node]['degree']= len(H.neighbors(node))
        H.node[node]['percentage_weight_change']= Graph_full_info.node[node]['percentage_weight_change']
        H.node[node]['time_in_system']= Graph_full_info.node[node]['time_in_system']  # OJO!! ESTO ES EL TOTAL, NO PARA EL PERIODO DE TIEMPO AL QUE SE REFIERE LA RED SEMESTRAL/CUATRIMESTRAL!!
        H.node[node]['weight_change']= Graph_full_info.node[node]['weight_change'] # OJO!! ESTO ES EL TOTAL, NO PARA EL PERIODO DE TIEMPO AL QUE SE REFIERE LA RED SEMESTRAL/CUATRIMESTRAL!!
        H.node[node]['activity']= Graph_full_info.node[node]['activity']   # OJO!! ESTO ES EL TOTAL, NO PARA EL PERIODO DE TIEMPO AL QUE SE REFIERE LA RED SEMESTRAL/CUATRIMESTRAL!!     
        H.node[node]['initial_bmi']= Graph_full_info.node[node]['initial_bmi']
        

   


    G= nx.connected_component_subgraphs(H)[0] # Giant component 
   
   
    print "size of the GC:",len(G.nodes())#, "after filtering for adherence!!"
    
   

    #dir=graph_name.split("full_")[0]
    #dir=graph_name.split("master")[0]
    #dir=graph_name.split("method3_")[0]
    #dir=graph_name.split("method3_adh")[0]
    dir=graph_name.split("friends")[0]


    dir=dir+"roles/"
   


   
    time_in_system=50 #minimum amount of time in the sytem for a user to be included in the statistics

    #name=graph_name.split('data/')[1]
    #name=graph_name.split('method3_50/interim/')[1]
    #name=graph_name.split('network_all_users/')[1]
    name=graph_name.split('5_points_network_2010/data/')[1]


   
    name=name.split('.gml')[0]
  
   
    name0=dir+name+"_overlap_R6s_averages_"+str(time_in_system)+"days_exclude_R6s.dat"
    file0=open(name0, 'wt')    
    file0.close()
    



    contador=0
    name12=dir+name+"_slopes_for_the_fits_average_weight_change.dat"           
    file=open(name12, 'wt')
    file.close()



####for the Isolated Clusters:
    list_GC_nodes=[]
    for n in G.nodes():
        list_GC_nodes.append(n)
       # print G.node[n]['percentage_weight_change']

   # print "# users GC:",len(list_GC_nodes),"total:",len(H.nodes())

    



    list_weight_changes_not_GC=[]
    for n in H.nodes():       
        if n not in list_GC_nodes:
            #print n,"not in GC"
            list_weight_changes_not_GC.append(float(H.node[n]['percentage_weight_change'])) 

    #print  "# users not in GC:",len(list_weight_changes_not_GC)


  


   # who="not_GC"
    #Nbins=18
    #histograma(list_weight_changes_not_GC,Nbins,dir,name,who)


 ###########################  



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
    


  #  print "\n\n R6s:\n"
   # for i in  list_R6s_label:
    #    print i

 # studying the possible cumulative effect of more than one R6 on the population:
    for node in G.nodes():
        cont=0
        for n in  G.neighbors(node):
            if str(G.node[n]['role']) == "R6" :
                cont+=1

        G.node[node]["R6_overlap"]=int(cont)











    ##### weight change for people not connected to any R6s:####

    list_weight_changes_no_neighbors=[]
    for node in G.nodes():
        interseccion=list(set(G.neighbors(node)) & set(list_R6s))

       # print node, "intersection:",intersection,len(intersection)
     #   print "because", list_R6s, "and ",G.neighbors(node)
      #  raw_input()
        if len(interseccion)==0:
            list_weight_changes_no_neighbors.append(G.node[node]['percentage_weight_change'])
       

  #  print len(list_weight_changes_no_neighbors),"no_neighbors"



    who="no_neigbors_R6s"
    Nbins=18
    histograma(list_weight_changes_no_neighbors,Nbins,dir,name,who)


# mood test
    mood=stats.mood(list_weight_changes_no_neighbors,list_weight_changes_not_GC) 
    print "mood test for",who, "against not_GC:",mood
    
########
# K-S test:
    ks=stats.ks_2samp(list_weight_changes_no_neighbors,list_weight_changes_not_GC) 
    print "KS test for",who, "against not_GC:",ks
    
    name00="ks_results.dat"
           
    file0=open(dir+name00, 'at')
    print >> file0, "KS test for",who,"of",graph_name, "against not_GC:",ks
    file0.close()
#############################################

    
    













#average percentage weight change as a function of the size of the largest CLIQUE the node belongs to:



   

    absolute_max=1
    for i in G.nodes():        
       
        maximo=1     
        list2=nx.cliques_containing_node(G, i)
       # print i, list2
       
        for elem in list2:
           # print elem,len(elem,)
            if len(elem) > maximo:
                maximo=len(elem)
       # print "\n",maximo
        G.node[i]['max_clique_size']=maximo
       
        if absolute_max < maximo:
            absolute_max = maximo


    #print absolute_max

    lista=list(nx.find_cliques(G)) # crea una lista de cliques (lista de listas)
    max_clique=nx.graph_clique_number(G)  #finds out max size clique
    num_tot_clique=nx.graph_number_of_cliques(G) #finds out total number of cliques

# count number of 2, 3, 4, 5, 6  and 7cliques:

    num_2cliques=0
    num_3cliques=0
    num_4cliques=0
    num_5cliques=0
    num_6cliques=0
    num_7cliques=0
    num_8cliques=0
    num_9cliques=0


   
    for element in lista: 
        if len(element)==2:
            num_2cliques=num_2cliques +1
           
        elif len(element)==3:
            num_3cliques=num_3cliques+1
           
        elif len(element)==4:
            num_4cliques=num_4cliques+1
          
        elif len(element)==5:
            num_5cliques=num_5cliques+1
           
        elif len(element)==6:
            num_6cliques=num_6cliques+1
           
        elif len(element)==7:
            num_7cliques=num_7cliques+1            

        elif len(element)==8:
            num_8cliques=num_8cliques+1    
           
        elif len(element)==9:
            num_9cliques=num_9cliques+1
           
           


 #   print " 2: ",num_2cliques, "     3: ",num_3cliques, "   4: ",num_4cliques, "     5: ",num_5cliques, "   6: ",num_6cliques, "   7: ",num_7cliques, "   8: ",num_8cliques, "   9: ",num_9cliques, "   max_clique_size:",max_clique, "   num_tot_cliques:", num_tot_clique





    name33=dir+name+"_percent_weight_change_vs_largest_clique_size.dat" 
    file11=open(name33, 'wt')  
    file11.close()

    list_of_lists_for_bootstrap=[]

    x_positions_fit=[]
    y_positions_fit=[]
    cum_size_set=float(len(G.nodes()))

    tot_nodes=[]

    for clique_size in range(1,max_clique):
       
        
        clique_size=clique_size+1
        print clique_size

        num_users_set=cum_size_set

        percent_weight_change_that_clique_size=[]
        for n in G.nodes():

            if G.node[n]['max_clique_size']==clique_size:
                percent_weight_change_that_clique_size.append(float(G.node[n]['percentage_weight_change']))
        
                tot_nodes.append(float(G.node[n]['percentage_weight_change']))

                cum_size_set-=1.0


        file11=open(name33, 'at')  
        print >> file11,clique_size,len(percent_weight_change_that_clique_size),num_users_set/float(len(G.nodes())),numpy.mean(percent_weight_change_that_clique_size),numpy.std(percent_weight_change_that_clique_size)
        file11.close()


        if len(x_positions_fit)<=7:
            x_positions_fit.append(clique_size)
            y_positions_fit.append(numpy.mean(percent_weight_change_that_clique_size))

            list_of_lists_for_bootstrap.append(percent_weight_change_that_clique_size)

    slope, intercept, Corr_coef, p_value, std_err =stats.linregress(x_positions_fit,y_positions_fit)  # least squeares polinomial fit

    print "result linear. fit for clique size dependency:"
   
    print "slope:",slope, "intercept:", intercept, "Corr_coef:", Corr_coef, "p_value:", p_value, "std_err:", std_err
   



     
    name11=dir+name+"_fits_clique_size.dat"
           
    file11=open(name11, 'wt')
    for i in range(len(x_positions_fit)):
        print >> file11,x_positions_fit[i],intercept+x_positions_fit[i]*slope

   

    print >> file11,"\n\n","y=",intercept,"+",slope,"*x",
    print   "Bootstrap for clique size:\n"
   
    mean_slope, standard_dev = bootstrap(x_positions_fit[0],x_positions_fit[-1],list_of_lists_for_bootstrap)
    zscore=(slope-mean_slope)/standard_dev

    print >> file11, "bootstrap:\n","actual slope:",slope,"mean_slope:",mean_slope,"standard_dev:",standard_dev,"\n zscore:",zscore


    print x_positions_fit[0],x_positions_fit[-1],"actual slope:",slope,"mean_slope:",mean_slope,"standard_dev:",standard_dev,"\n zscore:",zscore 

    file11.close()



    contador+=1     
    file=open(name12, 'at')
    print >> file,contador,mean_slope,standard_dev, "largest_clique_size"
    file.close()


#######################################









    #####dose effect of the R6s independently########

    name11=dir+name+"_dose_eff_indepently_only_one_R6_"+str(time_in_system)+"days_exclude_R6s.dat" 
    file11=open(name11, 'at')  
    print >> file11,0,"average_no_neighbors","average_no_neighbors","average_no_neighbors",len(list_weight_changes_no_neighbors),numpy.mean(list_weight_changes_no_neighbors),numpy.std(list_weight_changes_no_neighbors)  # the first line of the file is actually for no_neighbors, the rest, for one_and_only_one
    file11.close()
    







    file11=open(name11, 'wt')   
    file11.close()


    cont=1    
    list_all=[]
    list_all_nodes=[]
    for R6 in list_R6s:
        list_weight_changes=[]
        for n in G.neighbors(R6):
            if (G.node[n]['role'] != "R6")  and ( G.node[n]["R6_overlap"]==1) :
                list_weight_changes.append(float(G.node[n]['percentage_weight_change']))


                if n not in list_all_nodes:
                    list_all_nodes.append(n)
                    list_all.append(float(G.node[n]['percentage_weight_change']))


        if len(list_weight_changes)>0:

            file11=open(name11, 'at')  
            print >> file11,cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes),numpy.mean(list_weight_changes),numpy.std(list_weight_changes)
            file11.close()
           # print cont,G.node[R6]['role'],G.node[R6]['label'], len(G.neighbors(R6)),len(list_weight_changes),numpy.mean(list_weight_changes),numpy.std(list_weight_changes)
            cont=cont+1


          

        else:
           # file11=open(name11, 'at')  
            #print >> file11,cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes)
            #file11.close()
           # print cont,G.node[R6]['role'],G.node[R6]['label'],len(G.neighbors(R6)),len(list_weight_changes)
            cont=cont+1


    who="one_and_only_one_R6s"
    Nbins=18
    histograma(list_all,Nbins,dir,name,who)

  


  ####################################



    print "\n\n"


    list_of_lists_for_bootstrap=[]

    x_positions_fit=[]
    y_positions_fit=[]

    averages_larger5_x=[]
    averages_larger5_y=[]
    norm=0.0

    cum_size_set=float(len(G.nodes()))-float(len(list_R6s))
    for  r in range(len(list_R6s)+1):    
       
       # list_BMI_changes=[]               
        list_weight_changes=[]                
        list_percentage_weight_changes=[]    
        list_activities=[]
        
        num_users_set=cum_size_set
        for node in G.nodes():

            if int(G.node[node]["R6_overlap"])==r:

              
                
                if G.node[node]["role"]== "R6":  # i exclude the R6s                    
                    
                    pass
                else:
                    
                    if int(G.node[node]['time_in_system']) > time_in_system:                                               
                        
                       
                     #   list_BMI_changes.append(float(G.node[node]['final_BMI'])-float(G.node[node]['initial_BMI']))
                        list_weight_changes.append(float(G.node[node]['weight_change']))
                        list_percentage_weight_changes.append(float(G.node[node]['percentage_weight_change']))
                        list_activities.append(float(G.node[node]['activity'])/float(G.node[node]['time_in_system']))
                        cum_size_set-=1.0


                     

        if len(list_percentage_weight_changes)>0:
           # average_BMI_change=numpy.mean(list_BMI_changes)
            average_weight_change=numpy.mean(list_weight_changes)
            average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)
            average_activity=numpy.mean(list_activities)
            
            #deviation_BMI=numpy.std(list_BMI_changes)       
            deviation_weight=numpy.std(list_weight_changes)
            deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
            deviation_activity=numpy.std(list_activities) 


#print out
           
            file0=open(name0, 'at')
            print >> file0,r,len(list_percentage_weight_changes),num_users_set/float(len(G.nodes())),average_percentage_weight_change,deviation_percentage_weight,average_weight_change,deviation_weight,average_activity,deviation_activity
            file0.close()
       

            if r <=5:
                x_positions_fit.append(r)
                y_positions_fit.append(average_percentage_weight_change)

                list_of_lists_for_bootstrap.append(list_percentage_weight_changes)


           # else:
            #    aux_x=r*len(list_percentage_weight_changes)
             #   averages_larger5_x.append(aux_x)

              #  aux_y=average_percentage_weight_change*len(list_percentage_weight_changes)
               # averages_larger5_y.append(aux_y)
                #norm+=float(len(list_percentage_weight_changes))

  
#    x_positions_fit.append(numpy.mean(averages_larger5_x)/norm)
 #   y_positions_fit.append(numpy.mean(averages_larger5_y)/norm)



  
   #### averages for every R6's egonetwork:#########
    cont=1  
    list_all_=[]
    list_all_nodes_=[]
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

                if n  not in list_all_nodes_:
                    list_all_nodes_.append(n)               
                    list_all_.append(float(G.node[n]['percentage_weight_change']))

#averages 
        average_weight_change=numpy.mean(list_weight_changes)
      #  average_BMI_change=numpy.mean(list_BMI_changes)
        average_activity=numpy.mean(list_activities)
        average_percentage_weight_change=numpy.mean(list_percentage_weight_changes)

      



#standard deviation
        #deviation_BMI=numpy.std(list_BMI_changes)       
        deviation_weight=numpy.std(list_weight_changes)
        deviation_percentage_weight=numpy.std(list_percentage_weight_changes)
        deviation_activity=numpy.std(list_activities) 
        


#print out
        name2=dir+name+"_ego_R6s_average_weight_change_"+str(time_in_system)+"days.dat"
        file2=open(name2, 'at')
        print >> file2,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_weight_change,deviation_weight
        file2.close()


        name22=dir+name+"_ego_R6s_average_percentage_weight_change_"+str(time_in_system)+"days.dat"
        file22=open(name22, 'at')
        print >> file22,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_percentage_weight_change,deviation_percentage_weight
        file22.close()


        name3=dir+name+"_ego_R6s_average_activity_"+str(time_in_system)+"days.dat"
        file3=open(name3, 'at')
        print >> file3,cont,G.node[node]['role'],G.node[node]['label'],len(G.neighbors(node)),average_activity,deviation_activity
        file3.close()


   


        cont=cont+1




    who="R6s_egonetworks_all"
    Nbins=18
    histograma(list_all_,Nbins,dir,name,who)

  #  print "intersection:",len(set(list_all_)&set(list_all)),len(list_all_),len(list_all)
       #############just checking what happens if we remove the 40155 guy








##### percent weight change vs. role:

    list_roles=["R1","R2","R3","R4","R5","R6","R7"]

    file = open(dir+name+"_percentage_weight_change_vs_role",'wt')
    cont=1
    for role in list_roles:

        list_weight_changes_role=[]
        for n in G.nodes():
            if G.node[n]['role']==role:
                list_weight_changes_role.append(G.node[n]['percentage_weight_change'])
                
        print >> file, cont, role, len(list_weight_changes_role),numpy.mean(list_weight_changes_role),numpy.std(list_weight_changes_role)

        cont+=1

    file.close()



#############################







############## percentage weight change vs k
    x_positions_fit=[]
    y_positions_fit=[]
   
    cum_size_set=float(len(G.nodes()))

    
    list_of_lists_for_bootstrap=[]

    list_k=[]
    for n in G.nodes():
        list_k.append(len(G.neighbors(n)))        

    max_k=max(list_k)

   

    file = open(dir+name+"_percentage_weight_change_vs_k.dat",'wt')
    max_k=max_k+1
    for k in range(1,max_k):   

        num_users_set=cum_size_set
    
        list_percent_weight_change_k=[]
        for n in G.nodes():
            if len(G.neighbors(n))==k:
                list_percent_weight_change_k.append(G.node[n]['percentage_weight_change'])
                cum_size_set-=1.0

        if len(list_percent_weight_change_k)>0:
            print >> file,k, len(list_percent_weight_change_k),num_users_set/float(len(G.nodes())),numpy.mean(list_percent_weight_change_k),numpy.std(list_percent_weight_change_k)

            if len(x_positions_fit)<=7:
                x_positions_fit.append(k)
                y_positions_fit.append(numpy.mean(list_percent_weight_change_k))

                list_of_lists_for_bootstrap.append(list_percent_weight_change_k)


                

   
    slope, intercept, Corr_coef, p_value, std_err =stats.linregress(x_positions_fit,y_positions_fit)  # least squeares polinomial fit

    print "result linear. fit for degree dependency:"   
    print "slope:",slope, "intercept:", intercept, "Corr_coef:", Corr_coef, "p_value:", p_value, "std_err:", std_err
   
    file.close()



########################################













    new_name=graph_name.split(".gml")[0]

    new_name=new_name+"_adherent_num_R6s_largest_clique.gml"

    nx.write_gml(G,new_name)

    nx.write_gml(H,graph_name.strip('.gml')+"_attributes.gml")
    print "written network at:", graph_name.strip('.gml')+"_attributes.gml"









######################################3

#####################################






####################################3
def histograma(list,Nbins,dir,name,who):
                      #who es una etiqueta para saber sobre que poblacion hago el histograma

    hist, bin_edges= numpy.histogram(list, bins=Nbins,range=(-45.0,22.0))
#if i wanna compare several distrib. i MUST give same Nbins and max_min range too!!!
   
    print who, list
    print "max:",max(list),"min:",min(list)
    print hist, bin_edges

   
    area=0.0
    origin=float(bin_edges[0])
    file = open(dir+name+"_histogram_weight_change_"+who,'wt')
    for b in range (len(bin_edges)-1):        
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0, hist[b], float(hist[b])/float(len(list))

        area=area+float(hist[b])/float(len(list))
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()



    #print "area for",who,":",area


        
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




####################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
