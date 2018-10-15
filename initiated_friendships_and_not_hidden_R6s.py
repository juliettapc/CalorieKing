
#! /usr/bin/env python

"""
Created by Julia Poncela of June 2012

Analyze weight change after a gap.



"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import networkx as nx
import random


def main (graph_name1, graph_name2):



    list_ratio_initiated_R6s=[]
    list_ratio_initiated_hubs=[]
    list_ratio_initiated_kshells=[]
    list_ratio_initiated_all_networked_users=[]

    not_hidden_tot_population=0.
    not_hidden_networked_users=0.
    not_hidden_R6s=0.
    not_hidden_hubs=0.
    not_hidden_kshells=0.




    list_not_hidden_tot_population=[]
    list_not_hidden_networked_users=[]
    list_not_hidden_R6s=[]
    list_not_hidden_hubs=[]
    list_not_hidden_kshells=[]


    num_networked_users=0.
    num_R6s=0.
    num_hubs=0. 
    num_kshells=0.
    num_users=0.



    H1 = nx.read_gml(graph_name1)   
    G1 = nx.connected_component_subgraphs(H1)[0] # Giant component 



    H2 = nx.read_gml(graph_name2)   
    G2 = nx.connected_component_subgraphs(H2)[0] # Giant component 


    list_hub_ids=[]
    list_R6_ids=[]
    for node in G1.nodes():
        if (G1.node[node]['role'] =="R6"):
            list_R6_ids.append(int(G1.node[node]['label']))# this actually corresponds to the id from the users table in the DB

        if (int(G1.node[node]['degree']) >=30):
            list_hub_ids.append(int(G1.node[node]['label']))
              



  


    top_kshell=12




    list_top_kshell_ids=[]
    for node in G2.nodes():
        if (int(G2.node[node]['kshell_index']) == top_kshell):           
            list_top_kshell_ids.append(int(G2.node[node]['label']))# this actually corresponds to the id from the users table in the DB



    print  "# R6s: ",len(list_R6_ids),"# hubs: ",len(list_hub_ids),"# 12-kshells: ",len(list_top_kshell_ids)   ## 55 of them

    print "intersection R6s and hubs:",len(list(set(list_R6_ids) & set(list_hub_ids))),"   intersection R6s and 12-kshells:",len(list(set(list_R6_ids) & set(list_top_kshell_ids))), "   intersection 12-kshells and hubs:",len(list(set(list_top_kshell_ids) & set(list_hub_ids)))

   # raw_input()






    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



    query1="""select * from users"""    
    result1 = db.query(query1)  # is a list of dict.


    

       
    for r1 in result1:   #loop over users to get their gap info
      num_users+=1.

    # if num_users <=500:    # JUST TO TEST THE CODE
      ck_id=r1['ck_id']      
      id=int(r1['id'])

      query5="select  * from public_diary where (ck_id ='"+str(ck_id)+"')  "
      result5= db.query(query5)
      
      visibility=str(result5[0]['visibility'])
     


      if visibility!="HIDDEN":                  
          not_hidden_tot_population+=1.
          list_not_hidden_tot_population.append(1.)
      else:
          list_not_hidden_tot_population.append(0.)



      query4="select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"')  "
      result4= db.query(query4)

      degree=len(result4)
      initiated=0.

      if len(result4)>0:  # if they have friends
          num_networked_users+=1.
                             
          for r4 in result4:
              if r4['src']==ck_id:
                  initiated+=1.

          print "id:",id#, " k:",degree, " ratio:",initiated/degree
          
          list_ratio_initiated_all_networked_users.append(initiated/degree)
          
         


         
          #print ck_id,len(result5), visibility
          if visibility !="HIDDEN":
              not_hidden_networked_users+=1.
              list_not_hidden_networked_users.append(1.)
          else:
              list_not_hidden_networked_users.append(0.)



          if id in list_R6_ids:  #  R6s
              num_R6s+=1.

              list_ratio_initiated_R6s.append(initiated/degree)

              if visibility!="HIDDEN":                  
                  not_hidden_R6s+=1.
                  list_not_hidden_R6s.append(1.)
              else:
                  list_not_hidden_R6s.append(0.)


           

          if id in list_hub_ids:  #  hubs
              num_hubs+=1.

              list_ratio_initiated_hubs.append(initiated/degree)

              if visibility!="HIDDEN":                  
                  not_hidden_hubs+=1.
                  list_not_hidden_hubs.append(1.)
              else:
                  list_not_hidden_hubs.append(0.)


           

          if id in list_top_kshell_ids:  #  top kshell
              num_kshells+=1.

              list_ratio_initiated_kshells.append(initiated/degree)

              if visibility!="HIDDEN":                  
                  not_hidden_kshells+=1.
                  list_not_hidden_kshells.append(1.)
              else:
                  list_not_hidden_kshells.append(0.)


           








                  print "len(H1.nodes):",len(H1.nodes()),"# users with friends",num_networked_users, " average ratio initiated/degree ntwrk:",numpy.mean(list_ratio_initiated_all_networked_users),numpy.std(list_ratio_initiated_all_networked_users), " average ratio initiated/degree R6s:",numpy.mean(list_ratio_initiated_R6s),numpy.std(list_ratio_initiated_R6s) 


    print  "# hubs:", len(list_hub_ids),"ratio initiated/degree:", numpy.mean(list_ratio_initiated_hubs),numpy.std(list_ratio_initiated_hubs)

    print  "# 12kshells:", len(list_top_kshell_ids),"ratio initiated/degree:", numpy.mean(list_ratio_initiated_kshells),numpy.std(list_ratio_initiated_kshells)

  



    print "zscore between network and R6 initiated friendships:",bootstrap(list_ratio_initiated_all_networked_users, len(list_ratio_initiated_R6s),numpy.mean(list_ratio_initiated_R6s),5000),"5000iter",len(list_ratio_initiated_all_networked_users),len(list_ratio_initiated_R6s)

    print "zscore between network and hubs initiated friendships:",bootstrap(list_ratio_initiated_all_networked_users, len(list_ratio_initiated_hubs),numpy.mean(list_ratio_initiated_hubs),5000),"5000iter",len(list_ratio_initiated_all_networked_users),len(list_ratio_initiated_hubs)

    print "zscore between network and 12-kshell initiated friendships:",bootstrap(list_ratio_initiated_all_networked_users, len(list_ratio_initiated_kshells),numpy.mean(list_ratio_initiated_kshells),5000),"5000iter",len(list_ratio_initiated_all_networked_users),len(list_ratio_initiated_kshells)







    print "not hidden, total:",not_hidden_tot_population,numpy.mean(list_not_hidden_tot_population)," id. ntwrk:", not_hidden_networked_users,numpy.mean(list_not_hidden_networked_users)," id. R6s:",not_hidden_R6s,numpy.mean(list_not_hidden_R6s)

   
    print "not hidden hubs:",not_hidden_hubs,numpy.mean(list_not_hidden_hubs)

   

    print "not hidden, total 12-kshells:",not_hidden_kshells,numpy.mean(list_not_hidden_kshells)

   










        
#######################################
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
def bootstrap(list, sample_size,real_average_value,Niter):
    
    
    list_synth_average_values=[]

   
    for iter in range (Niter):
        
        list_synth=sample_with_replacement(list,sample_size)

        list_synth_average_values.append(numpy.mean(list_synth))



    zscore=(real_average_value-numpy.mean(list_synth_average_values))/numpy.std(list_synth_average_values)
  

    return zscore




#############################################
def bootstrap_original(first_x,last_x,list_of_lists_for_bootstrap):
    
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





#mean_slope, standard_dev = bootstrap_original(x_positions_fit[0],x_positions_fit[-1],list_of_lists_for_bootstrap)





#########################
          
if __name__ == '__main__':
    if len(sys.argv) > 2:
        graph_filename1 = sys.argv[1]
        graph_filename2 = sys.argv[2]


        main(graph_filename1,graph_filename2)
    else:
        print "usage: python whatever.py path/network_file1_R6s_info.gml  path/network_file2_kshell_info.gml "

  
     

##############################################
