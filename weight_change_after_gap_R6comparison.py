 
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
import datetime
import random
import networkx as nx


 
def main (graph_name1, graph_name2):

    max_index=5000  # just to try out the program with a few time series    
    index=-1

    min_num_weigh_ins=30   # according to the time series filtering we agree on

    few_points=4  # to classify gaps in the beginning/ end of the time series


    Niter_bootstrap=1000

    ending_date_DB=datetime.datetime(2010, 12, 31, 0, 0)  
    reasonable_ending=datetime.datetime(2010, 12, 1, 0, 0)   # i only consider users active until 1month  before the ending date for the DB





    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 

    query="""select * from users""" 
    result1 = db.query(query)  # is a list of dict.




   # cont=0
    #num_friendships=0

   # for r1 in result1:
     #   ck_id=r1['ck_id']     

     #   query4="select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"')  "
     #   result4= db.query(query4)
     #   if len(result4)>0:
      #      cont+=1
      #      num_friendships+=len(result4)
    
  #  query11="""SELECT * FROM private_messages"""
  #  result11 = db.query(query11)

  #  query22="""SELECT * FROM forum_posts"""
 #   result22 = db.query(query22)

 #   query33="""SELECT * FROM blog_comments """
 #   result33 = db.query(query33)

  #  query44="""SELECT * FROM homepage_comment"""
  #  result44 = db.query(query44)


   # print "number of users with k>0",cont,"num links:",float(num_friendships)/2., "tot. num. messages",len(result11), "tot. num. forum posts",len(result22), "tot. num. blog posts",len(result33), "tot. num. homepage posts",len(result44)

  #  exit()


    H1 = nx.read_gml(graph_name1)  
    G1 = nx.connected_component_subgraphs(H1)[0] # Giant component 



    H2 = nx.read_gml(graph_name2)   
    G2 = nx.connected_component_subgraphs(H2)[0] # Giant component 

    dict_R6overlap={}
    for i in range(max(list(G1.degree().values()))):       
        dict_R6overlap[i]=[]  # {0:[],1:[],2:[],...}  dict of lists of nodes with 0, 1, 2,... R6s_overlap
       
    


    list_hub_ids=[]
    list_R6_ids=[]
    list_R6overlap_ids=[]  # connected to R6s
    for node in G1.nodes():
        if (G1.node[node]['role'] =="R6"):
            list_R6_ids.append(int(G1.node[node]['label']))# this actually corresponds to the id from the users table in the DB

        if (int(G1.node[node]['degree']) >=30):
            list_hub_ids.append(int(G1.node[node]['label']))


        if (int(G1.node[node]['R6_overlap']) >0):
            list_R6overlap_ids.append(int(G1.node[node]['label']))

            index=int(G1.node[node]['R6_overlap'])
            dict_R6overlap[index].append(int(G1.node[node]['label']))
        else:  
            dict_R6overlap[0].append(int(G1.node[node]['label']))

  


    top_kshell=12   # because i know is that so
    list_top_kshell_ids=[]
    for node in G2.nodes():
        if (int(G2.node[node]['kshell_index']) >= top_kshell):           
            list_top_kshell_ids.append(int(G2.node[node]['label']))# this actually corresponds to the id from the users table in the DB



    print  "# R6s: ",len(list_R6_ids),"# hubs: ",len(list_hub_ids),"# 12-kshells: ",len(list_top_kshell_ids)   ## 55 of them





    list_weight_changes_gaps=[]
    list_weight_changes_gaps_network=[]
    list_weight_changes_gaps_R6s=[]
    list_weight_changes_gaps_hubs=[]
    list_weight_changes_gaps_top_kshells=[]
    list_weight_changes_gaps_R6overlap=[]  # people connected to R6s


    list_all_weight_changes=[]
    list_all_weight_changes_network=[] 
    list_all_weight_changes_R6s=[] 
    list_all_weight_changes_hubs=[] 
    list_all_weight_changes_top_kshells=[] 
    list_all_weight_changes_R6overlap=[] 


    list_net_weight_changes=[]
    list_net_weight_changes_network=[]
    list_net_weight_changes_R6s=[]           
    list_net_weight_changes_hubs=[]           
    list_net_weight_changes_top_kshells=[]
    list_net_weight_changes_R6overlap=[]      


    num_users=0.
    num_users_with_gaps=0.
    num_network_users_with_gaps=0.
    num_network_users=0.

    list_gaps_no_gaps_all=[]    # prob. of having a gap
    list_gaps_no_gaps_network=[]
    list_gaps_no_gaps_R6s=[]   
    list_gaps_no_gaps_hubs=[]
    list_gaps_no_gaps_top_kshells=[]
    list_gaps_no_gaps_R6overlap=[]   

    list_weight_gain_after_gap_all=[]    # prob. of gaining weight after a gap
    list_weight_gain_after_gap_network=[]
    list_weight_gain_after_gap_R6s=[]
    list_weight_gain_after_gap_hubs=[]
    list_weight_gain_after_gap_top_kshells=[]
    list_weight_gain_after_gap_R6overlap=[]


    list_init_gap_all=[]      # prob. of having a gap initally/in the middle/ at the end
    list_init_gap_network=[]
    list_init_gap_R6s=[]      
    list_init_gap_hubs=[]
    list_init_gap_top_kshells=[]
    list_init_gap_R6overlap=[]      

    list_middle_gap_all=[]
    list_middle_gap_network=[]
    list_middle_gap_R6s=[]      
    list_middle_gap_hubs=[]
    list_middle_gap_top_kshells=[]
    list_middle_gap_R6overlap=[]      

    list_end_gap_all=[]
    list_end_gap_network=[]
    list_end_gap_R6s=[]     
    list_end_gap_hubs=[]
    list_end_gap_top_kshells=[]
    list_end_gap_R6overlap=[]     


    for r1 in result1:   #loop over users to get their gap info


      index+=1
   #  if index <= max_index:  # just to try out the program with a few time series    

      print index

      ck_id=r1['ck_id']      
      n_id=int(r1['id'])  #this corresponds with the 'label' attribute in the .gml file




      query2="select  * from gaps_by_frequency where (ck_id ='"+str(ck_id)+"')  order by start_day asc"
      result2 = db.query(query2)



      query3="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
      result3 = db.query(query3)



      query4="select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"')  "
      result4= db.query(query4)
  



      if  len(result3)>=min_num_weigh_ins:  ################### ONLY  if more than X weigh-ins
        num_users+=1.


        cont=0
        initial_weight=float(result3[0]['weight'])
        for r3 in result3:  # to calculate weight-change, i skip the first entry
             if cont>0:
                 list_all_weight_changes.append(float(r3['weight'])-initial_weight)

                 if len(result4)>0:   # if he/she has friends
                     list_all_weight_changes_network.append(float(r3['weight'])-initial_weight)

                     if n_id in list_R6_ids:
                         list_all_weight_changes_R6s.append(float(r3['weight'])-initial_weight) 
                     if n_id in list_hub_ids:
                         list_all_weight_changes_hubs.append(float(r3['weight'])-initial_weight)
                     if n_id in list_top_kshell_ids:
                         list_all_weight_changes_top_kshells.append(float(r3['weight'])-initial_weight)     

                     if n_id in list_R6overlap_ids:
                         list_all_weight_changes_R6overlap.append(float(r3['weight'])-initial_weight) 
                    



             initial_weight=float(r3['weight'])                    
             cont+=1
        list_net_weight_changes.append(float(result3[-1]['weight'])-float(result3[0]['weight']))
      

        if len(result4)>0:
            num_network_users+=1.
            list_net_weight_changes_network.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 

            if n_id in list_R6_ids:
                list_net_weight_changes_R6s.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 
            if n_id in list_hub_ids:
                list_net_weight_changes_hubs.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 
            if n_id in list_top_kshell_ids:
                list_net_weight_changes_top_kshells.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 

            if n_id in list_R6overlap_ids:
                list_net_weight_changes_R6overlap.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 


        if len(result2)>0:  # if there is a gap record for that user            
            num_users_with_gaps+=1.            
            list_gaps_no_gaps_all.append(1.)
            
            if len(result4)>0:
                num_network_users_with_gaps+=1.
   
          
                list_gaps_no_gaps_network.append(1.)  

                if n_id in list_R6_ids:
                    list_gaps_no_gaps_R6s.append(1.)
                if n_id in list_hub_ids:
                    list_gaps_no_gaps_hubs.append(1.)
                if n_id in list_top_kshell_ids:
                    list_gaps_no_gaps_top_kshells.append(1.)
                if n_id in list_R6overlap_ids:
                    list_gaps_no_gaps_R6overlap.append(1.)
          

            for r2 in result2:                               

                start_index=int(r2['index_start_day'])  # index for the entry in the gaps_by_frequency  table where the gap is (point number...): starting on 0
                end_index=int(r2['index_end_day'])
       



# to compute probabilities of having gaps at the beginning/middle/end, i am carefull about the time series
# not ending JUST because the DB ended

                date_end_serie=result3[-1]['on_day']                
                if date_end_serie <=reasonable_ending:
                   # print "gap",date_end_serie,"prior to the reasonable ending date of the DB",ending_date_DB
   

                    if start_index <= few_points:
                        list_init_gap_all.append(1.0)      # prob. of having a gap initally/in the middle/ at the end
                        list_middle_gap_all.append(0.0)
                        list_end_gap_all.append(0.0)

                        if len(result4)>0:
                            list_init_gap_network.append(1.0) 
                            list_middle_gap_network.append(0.0)
                            list_end_gap_network.append(0.0)


                            if n_id in list_R6_ids:
                                list_init_gap_R6s.append(1.0)  
                                list_middle_gap_R6s.append(0.0)  
                                list_end_gap_R6s.append(0.0)    
                            if n_id in list_hub_ids:
                                list_init_gap_hubs.append(1.0)  
                                list_middle_gap_hubs.append(0.0)  
                                list_end_gap_hubs.append(0.0)  
                            if n_id in list_top_kshell_ids:
                                list_init_gap_top_kshells.append(1.0)  
                                list_middle_gap_top_kshells.append(0.0)  
                                list_end_gap_top_kshells.append(0.0)  
                            if n_id in list_R6overlap_ids:
                                list_init_gap_R6overlap.append(1.0)  
                                list_middle_gap_R6overlap.append(0.0)  
                                list_end_gap_R6overlap.append(0.0)    

     
                    elif len(result3)-int(end_index)<=few_points:                   
                        list_init_gap_all.append(0.0)    
                        list_middle_gap_all.append(0.0)
                        list_end_gap_all.append(1.0)

                        if len(result4)>0:                                              
                            list_init_gap_network.append(0.0)
                            list_middle_gap_network.append(0.0)
                            list_end_gap_network.append(1.0)

                            if n_id in list_R6_ids:
                                list_init_gap_R6s.append(0.0)  
                                list_middle_gap_R6s.append(0.0)  
                                list_end_gap_R6s.append(1.0)    
                            if n_id in list_hub_ids:
                                list_init_gap_hubs.append(0.0)  
                                list_middle_gap_hubs.append(0.0)  
                                list_end_gap_hubs.append(1.0)  
                            if n_id in list_top_kshell_ids:
                                list_init_gap_top_kshells.append(0.0)  
                                list_middle_gap_top_kshells.append(0.0)  
                                list_end_gap_top_kshells.append(1.0)  
                            if n_id in list_R6overlap_ids:
                                list_init_gap_R6overlap.append(0.0)  
                                list_middle_gap_R6overlap.append(0.0)  
                                list_end_gap_R6overlap.append(1.0)    

                    else:
                        list_init_gap_all.append(0.0)
                        list_middle_gap_all.append(1.0) 
                        list_end_gap_all.append(0.0)

                        if len(result4)>0:
                            list_init_gap_network.append(0.0)
                            list_middle_gap_network.append(1.0) 
                            list_end_gap_network.append(0.0)

                            if n_id in list_R6_ids:
                                list_init_gap_R6s.append(0.0)  
                                list_middle_gap_R6s.append(1.0)  
                                list_end_gap_R6s.append(0.0)    
                            if n_id in list_hub_ids:
                                list_init_gap_hubs.append(0.0)  
                                list_middle_gap_hubs.append(1.0)  
                                list_end_gap_hubs.append(0.0)  
                            if n_id in list_top_kshell_ids:
                                list_init_gap_top_kshells.append(0.0)  
                                list_middle_gap_top_kshells.append(1.0)  
                                list_end_gap_top_kshells.append(0.0)  
                            if n_id in list_R6overlap_ids:
                                list_init_gap_R6overlap.append(0.0)  
                                list_middle_gap_R6overlap.append(1.0)  
                                list_end_gap_R6overlap.append(0.0)    
                else:   #i dont consider a gap too close to the end of the DB final date
                    print date_end_serie,"after reasonable ending date of the DB",ending_date_DB                   

                
                tot_weight_change_gap=float(result3[end_index]['weight'])-float(result3[start_index]['weight']) 
                
                list_weight_changes_gaps.append(tot_weight_change_gap)
            
           
                if tot_weight_change_gap>=0.:
                    list_weight_gain_after_gap_all.append(1.)
                else:
                    list_weight_gain_after_gap_all.append(0.)
                
   

                if len(result4)>0:
                                   
                    if tot_weight_change_gap>=0.:
                        list_weight_gain_after_gap_network.append(1.)

                        if n_id in list_R6_ids:
                            list_weight_gain_after_gap_R6s.append(1.)
                        if n_id in list_hub_ids:
                            list_weight_gain_after_gap_hubs.append(1.)
                        if n_id in list_top_kshell_ids:
                            list_weight_gain_after_gap_top_kshells.append(1.)
                        if n_id in list_R6overlap_ids:
                            list_weight_gain_after_gap_R6overlap.append(1.)
                    else:
                        list_weight_gain_after_gap_network.append(0.)
                        
                        if n_id in list_R6_ids:
                            list_weight_gain_after_gap_R6s.append(0.)
                        if n_id in list_hub_ids:
                            list_weight_gain_after_gap_hubs.append(0.)
                        if n_id in list_top_kshell_ids:
                            list_weight_gain_after_gap_top_kshells.append(0.)
                        if n_id in list_R6overlap_ids:
                            list_weight_gain_after_gap_R6overlap.append(0.)

                   


                    list_weight_changes_gaps_network.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight'])  )

                    if n_id in list_R6_ids:
                        list_weight_changes_gaps_R6s.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight']))
                    if n_id in list_hub_ids:
                        list_weight_changes_gaps_hubs.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight']))
                    if n_id in list_top_kshell_ids:
                        list_weight_changes_gaps_top_kshells.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight']))

                    if n_id in list_R6overlap_ids:
                        list_weight_changes_gaps_R6overlap.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight']))




        else:   # no gaps
            list_gaps_no_gaps_all.append(0.)
            if len(result4)>0:
                 list_gaps_no_gaps_network.append(0.)

                 if n_id in list_R6_ids:
                     list_gaps_no_gaps_R6s.append(0.)
                 if n_id in list_hub_ids:
                     list_gaps_no_gaps_hubs.append(0.)
                 if n_id in list_top_kshell_ids:
                     list_gaps_no_gaps_top_kshells.append(0.)
                 if n_id in list_R6overlap_ids:
                     list_gaps_no_gaps_R6overlap.append(0.)



    print 'total # users with >=',min_num_weigh_ins,'w-ins: ',num_users,'   total # users with gaps: ',num_users_with_gaps
    print 'network users with >=',min_num_weigh_ins, 'w-ins: ',num_network_users,'   network users with gaps: ',num_network_users_with_gaps,"\n"


    print 'weight_change gaps all users:',numpy.mean(list_weight_changes_gaps),' +/- ',numpy.std(list_weight_changes_gaps)
    print '   ntwk users:',numpy.mean(list_weight_changes_gaps_network),' +/- ',numpy.std(list_weight_changes_gaps_network)
    print '   R6s:',numpy.mean(list_weight_changes_gaps_R6s),' +/- ',numpy.std(list_weight_changes_gaps_R6s)
    print '   hubs:',numpy.mean(list_weight_changes_gaps_hubs),' +/- ',numpy.std(list_weight_changes_gaps_hubs)
    print '   top kshells:',numpy.mean(list_weight_changes_gaps_top_kshells),' +/- ',numpy.std(list_weight_changes_gaps_top_kshells)
    print '   R6overlap:',numpy.mean(list_weight_changes_gaps_R6overlap),' +/- ',numpy.std(list_weight_changes_gaps_R6overlap),"\n"


    print 'average weight change all changes, all users:',numpy.mean(list_all_weight_changes),' +/- ',numpy.std(list_all_weight_changes)
    print 'average weight change all changes, network users:',numpy.mean(list_all_weight_changes_network),' +/- ',numpy.std(list_all_weight_changes_network),"\n"



    print '# all weight changes:',len(list_all_weight_changes),'  # gap changes all users:',len(list_weight_changes_gaps),'  # gap changes network users:',len(list_weight_changes_gaps_network),"\n"



    print '# net weight changes all users:',numpy.mean(list_net_weight_changes),numpy.std(list_net_weight_changes),' # events::',len(list_net_weight_changes)
    print '#    network:',numpy.mean(list_net_weight_changes_network),numpy.std(list_net_weight_changes_network),' # events:',len(list_net_weight_changes_network)
    print '#    R6s:',numpy.mean(list_net_weight_changes_R6s),numpy.std(list_net_weight_changes_R6s),' # events:',len(list_net_weight_changes_R6s)
    print '#    hubs:',numpy.mean(list_net_weight_changes_hubs),numpy.std(list_net_weight_changes_hubs),' # events:',len(list_net_weight_changes_hubs)
    print '#    top kshells:',numpy.mean(list_net_weight_changes_top_kshells),numpy.std(list_net_weight_changes_top_kshells),' # events:',len(list_net_weight_changes_top_kshells)
    print '#    R6overlap:',numpy.mean(list_net_weight_changes_R6overlap),numpy.std(list_net_weight_changes_R6overlap),' # events:',len(list_net_weight_changes_R6overlap),"\n"

    
    
    print "prob. having a gap for tot population with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_all)," # events:",len(list_gaps_no_gaps_all)
    print "    for network population with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_network),"# events: ",len(list_gaps_no_gaps_network)
    print "    for R6s with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_R6s),"# events: ",len(list_gaps_no_gaps_R6s)
    print "    for hubs with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_hubs),"# events: ",len(list_gaps_no_gaps_hubs)
    print "    for 12-kshells with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_top_kshells),"# events: ",len(list_gaps_no_gaps_top_kshells)
    print "    for R6overlap with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_R6overlap),"# events: ",len(list_gaps_no_gaps_R6overlap),"\n"



    print "prob. gaining weight after a gap, for tot population with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_all)," # events:",len(list_weight_gain_after_gap_all)
    print "   for network population with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_network)," # events:",len(list_weight_gain_after_gap_network)
    print "   for R6s with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_R6s)," # events:",len(list_weight_gain_after_gap_R6s)
    print "   for hubs with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_hubs)," # events:",len(list_weight_gain_after_gap_hubs)
    print "   for 12-kshells with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_top_kshells)," # events:",len(list_weight_gain_after_gap_top_kshells)
    print "   for R6overlap with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_R6overlap)," # events:",len(list_weight_gain_after_gap_R6overlap),"\n"




    print "prob. init. gap for all:",numpy.mean(list_init_gap_all)," middle:",numpy.mean(list_middle_gap_all)," end:",numpy.mean(list_end_gap_all)
    print "    for network:",numpy.mean(list_init_gap_network)," middle:",numpy.mean(list_middle_gap_network)," end:",numpy.mean(list_end_gap_network)
    print "    for R6s:",numpy.mean(list_init_gap_R6s)," middle:",numpy.mean(list_middle_gap_R6s)," end:",numpy.mean(list_end_gap_R6s)
    print "    for hubs:",numpy.mean(list_init_gap_hubs)," middle:",numpy.mean(list_middle_gap_hubs)," end:",numpy.mean(list_end_gap_hubs)
    print "    for top kshell:",numpy.mean(list_init_gap_top_kshells)," middle:",numpy.mean(list_middle_gap_top_kshells)," end:",numpy.mean(list_end_gap_top_kshells)

    print "    for R6overlap:",numpy.mean(list_init_gap_R6overlap)," middle:",numpy.mean(list_middle_gap_R6overlap)," end:",numpy.mean(list_end_gap_R6overlap),"\n"



    print "zscore between all weight changes and gap changes (All):",bootstrap(list_all_weight_changes, len(list_weight_changes_gaps),numpy.std(list_weight_changes_gaps),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes), len(list_weight_changes_gaps)

    print "zscore between all weight changes and gap changes (Network):",bootstrap(list_all_weight_changes_network, len(list_weight_changes_gaps_network),numpy.std(list_weight_changes_gaps_network),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_network), len(list_weight_changes_gaps_network)  # which of the 2 comparisons makes more sense??

    print "zscore between all weight changes (R6s) and gap changes (R6s):",bootstrap(list_all_weight_changes_R6s,  len(list_weight_changes_gaps_R6s),numpy.std(list_weight_changes_gaps_R6s),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_R6s), len(list_weight_changes_gaps_R6s)
     
    print "zscore between all weight changes (hubs) and gap changes (hubs):",bootstrap(list_all_weight_changes_hubs,  len(list_weight_changes_gaps_hubs),numpy.std(list_weight_changes_gaps_hubs),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_hubs), len(list_weight_changes_gaps_hubs)
    
    print "zscore between all weight changes (top kshells) and gap changes (top kshells):",bootstrap(list_all_weight_changes_top_kshells,  len(list_weight_changes_gaps_top_kshells),numpy.std(list_weight_changes_gaps_top_kshells),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_top_kshells), len(list_weight_changes_gaps_top_kshells)
     
    print "zscore between all weight changes (R6overlap) and gap changes (R6overlap):",bootstrap(list_all_weight_changes_R6overlap,  len(list_weight_changes_gaps_R6overlap),numpy.std(list_weight_changes_gaps_R6overlap),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_R6overlap), len(list_weight_changes_gaps_R6overlap),"\n"




    print "zscore between gap changes (All) and gap changes (Network):",bootstrap(list_weight_changes_gaps, len(list_weight_changes_gaps_network),numpy.std(list_weight_changes_gaps_network),Niter_bootstrap),Niter_bootstrap,"iter",len(list_weight_changes_gaps), numpy.mean(list_weight_changes_gaps), numpy.std(list_weight_changes_gaps),len(list_weight_changes_gaps_network),numpy.mean(list_weight_changes_gaps_network),numpy.std(list_weight_changes_gaps_network)   # which of the 2 comparisons makes more sense??
   
    print "zscore between gap changes (All) and gap changes (R6overlap):",bootstrap(list_weight_changes_gaps, len(list_weight_changes_gaps_R6overlap),numpy.std(list_weight_changes_gaps_R6overlap),Niter_bootstrap),Niter_bootstrap,"iter",len(list_weight_changes_gaps), numpy.mean(list_weight_changes_gaps), numpy.std(list_weight_changes_gaps),len(list_weight_changes_gaps_R6overlap) ,numpy.mean(list_weight_changes_gaps_R6overlap),numpy.std(list_weight_changes_gaps_R6overlap)

    print "zscore between gap changes (Networked) and gap changes (R6overlap):",bootstrap(list_weight_changes_gaps_network, len(list_weight_changes_gaps_R6overlap),numpy.std(list_weight_changes_gaps_R6overlap),Niter_bootstrap),Niter_bootstrap,"iter",len(list_weight_changes_gaps_network), numpy.mean(list_weight_changes_gaps_network), numpy.std(list_weight_changes_gaps_network),len(list_all_weight_changes_R6overlap), numpy.mean(list_weight_changes_gaps_R6overlap), numpy.std(list_weight_changes_gaps_R6overlap)


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
def bootstrap(lista, sample_size,real_average_value,Niter):
    
    
    list_synth_average_values=[]

   
    for iter in range (Niter):
        
        list_synth=sample_with_replacement(lista,sample_size)

        list_synth_average_values.append(numpy.mean(list_synth))



    zscore=(real_average_value-numpy.mean(list_synth_average_values))/numpy.std(list_synth_average_values)
  

    return zscore




#########################
          
if __name__== "__main__":
    if len(sys.argv) > 2:
        graph_filename1 = sys.argv[1]
        graph_filename2 = sys.argv[2]


        main(graph_filename1,graph_filename2)
    else:
        print "usage: python whatever.py path/network_file1_R6s_info.gml  path/network_file2_kshell_info.gml "

   
    
     

##############################################
