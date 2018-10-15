 
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

 
def main ():

    max_index=2000  # just to try out the program with a few time series    
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



    list_weight_changes_gaps=[]
    list_weight_changes_gaps_network=[]
    list_all_weight_changes=[]
    list_all_weight_changes_network=[] 

    list_net_weight_changes=[]
    list_net_weight_changes_network=[] 

    num_users=0.
    num_users_with_gaps=0.
    num_network_users_with_gaps=0.
    num_network_users=0.

    list_gaps_no_gaps_all=[]    # prob. of having a gap
    list_gaps_no_gaps_network=[]


    list_weight_gain_after_gap_all=[]    # prob. of gaining weight after a gap
    list_weight_gain_after_gap_network=[]


    list_init_gap_all=[]      # prob. of having a gap initally/in the middle/ at the end
    list_init_gap_network=[]

    list_middle_gap_all=[]
    list_middle_gap_network=[]

    list_end_gap_all=[]
    list_end_gap_network=[]



    for r1 in result1:   #loop over users to get their gap info


      index+=1
     #if index <= max_index:  # just to try out the program with a few time series    

      print index

      ck_id=r1['ck_id']      



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

             initial_weight=float(r3['weight'])                    
             cont+=1
        list_net_weight_changes.append(float(result3[-1]['weight'])-float(result3[0]['weight']))
      

        if len(result4)>0:
            num_network_users+=1.
            list_net_weight_changes_network.append(float(result3[-1]['weight'])-float(result3[0]['weight'])) 
    

        if len(result2)>0:  # if there is a gap record for that user            
            num_users_with_gaps+=1.            
            list_gaps_no_gaps_all.append(1.)
            
            if len(result4)>0:
                num_network_users_with_gaps+=1.
   
          

          

            for r2 in result2:                               

                start_index=int(r2['index_start_day'])  # index for the entry in the weigh_in_history table where the gap is (point number...): starting on 0
                end_index=int(r2['index_end_day'])
       



# to compute probabilities of having gaps at the beginning/middle/end, i am carefull about the time series
# not ending JUST because the DB ended

                date_end_serie=result3[-1]['on_day']                
                if date_end_serie <=reasonable_ending:
                    print "gap",date_end_serie,"prior to the reasonable ending date of the DB",ending_date_DB
   

                    if start_index <= few_points:
                        list_init_gap_all.append(1.0)      # prob. of having a gap initally/in the middle/ at the end
                        list_middle_gap_all.append(0.0)
                        list_end_gap_all.append(0.0)

                        if len(result4)>0:
                            list_init_gap_network.append(1.0) 
                            list_middle_gap_network.append(0.0)
                            list_end_gap_network.append(0.0)
     
                    elif len(result3)-int(end_index)<=few_points:                   
                        list_init_gap_all.append(0.0)    
                        list_middle_gap_all.append(0.0)
                        list_end_gap_all.append(1.0)

                        if len(result4)>0:                                              
                            list_init_gap_network.append(0.0)
                            list_middle_gap_network.append(0.0)
                            list_end_gap_network.append(1.0)

                    else:
                        list_init_gap_all.append(0.0)
                        list_middle_gap_all.append(1.0) 
                        list_end_gap_all.append(0.0)

                        if len(result4)>0:
                            list_init_gap_network.append(0.0)
                            list_middle_gap_network.append(1.0) 
                            list_end_gap_network.append(0.0)

 
                else:
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
                    else:
                        list_weight_gain_after_gap_network.append(0.)
                        

                    list_gaps_no_gaps_network.append(1.)
                    list_weight_changes_gaps_network.append(float(result3[end_index]['weight'])- float(result3[start_index]['weight'])  )
                        



        else:   # no gaps
            list_gaps_no_gaps_all.append(0.)
            if len(result4)>0:
                 list_gaps_no_gaps_network.append(0.)



    print 'total # users with >=30 w-ins: ',num_users,'   total # users with gaps: ',num_users_with_gaps
    print 'network users with >=30 w-ins: ',num_network_users,'   network users with gaps: ',num_network_users_with_gaps,"\n"


    print 'num_users_with_gaps/num_users:',num_users_with_gaps/num_users,'  weight_change gaps all users:',numpy.mean(list_weight_changes_gaps),' +/- ',numpy.std(list_weight_changes_gaps)
    print 'num_network_users_with_gaps/num_network_users',num_network_users_with_gaps/num_network_users,' weight_change gaps all ntwk users:',numpy.mean(list_weight_changes_gaps_network),' +/- ',numpy.std(list_weight_changes_gaps_network),"\n"

    print 'average weight change all changes, all users:',numpy.mean(list_all_weight_changes),' +/- ',numpy.std(list_all_weight_changes)
    print 'average weight change all changes, network users:',numpy.mean(list_all_weight_changes_network),' +/- ',numpy.std(list_all_weight_changes_network)


    print '# all weight changes:',len(list_all_weight_changes),'  # gap changes all users:',len(list_weight_changes_gaps),'  # gap changes network users:',len(list_weight_changes_gaps_network),"\n"



    print '# net weight changes:',numpy.mean(list_net_weight_changes),numpy.std(list_net_weight_changes),' # events::',len(list_net_weight_changes)
    print '# net weight changes network:',numpy.mean(list_net_weight_changes_network),numpy.std(list_net_weight_changes_network),' # events:',len(list_net_weight_changes_network),"\n"




    print "prob. having a gap for tot population with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_all)," # events:",len(list_gaps_no_gaps_all)
    print "prob. having a gap for network population with more than 30weigh-ins:",numpy.mean(list_gaps_no_gaps_network),"# events: ",len(list_gaps_no_gaps_network),"\n"



    print "prob. gaining weight after a gap, for tot population with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_all)," # events:",len(list_weight_gain_after_gap_all)
    print "prob. gaining weight after a gap, for network population with gaps and more than 30weigh-ins:",numpy.mean(list_weight_gain_after_gap_network)," # events:",len(list_weight_gain_after_gap_network),"\n"



    print "prob. init. gap all:",numpy.mean(list_init_gap_all)," middle:",numpy.mean(list_middle_gap_all)," end:",numpy.mean(list_end_gap_all)
    print "prob. init. gap network:",numpy.mean(list_init_gap_network)," middle:",numpy.mean(list_middle_gap_network)," end:",numpy.mean(list_end_gap_network),"\n"




    print "zscore between all weight changes and gap changes (All):",bootstrap(list_all_weight_changes, len(list_weight_changes_gaps),numpy.std(list_weight_changes_gaps),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes), len(list_weight_changes_gaps)

    print "zscore between all weight changes and gap changes (Network):",bootstrap(list_all_weight_changes_network, len(list_weight_changes_gaps_network),numpy.std(list_weight_changes_gaps_network),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes_network), len(list_weight_changes_gaps_network)

    print "zscore between all weight changes (All) and gap changes (Network):",bootstrap(list_all_weight_changes, len(list_weight_changes_gaps_network),numpy.std(list_weight_changes_gaps_network),Niter_bootstrap),Niter_bootstrap,"iter",len(list_all_weight_changes), len(list_weight_changes_gaps_network)






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




#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
