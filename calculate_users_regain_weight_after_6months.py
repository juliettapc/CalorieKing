#! /usr/bin/env python

"""
Created by Julia Poncela of February 2013.

It doesn't take any arguments. Reads from the ck database.

Count fraction of users that regain weight after 6month mark, and also
weight change until 6months, and weight change from that point until the end.

"""


import sys
import os
import datetime
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import networkx as nx
import random
import histograma_gral
import histograma_bines_gral
import csv

def main ():


    minimum_time=180
    min_num_weigh_ins=2
   
    impossible_weight_change=80.  # plus or minus, it is a mistake


    for_testing_max_num_queries=1000


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    query1="""select * from users"""    
    result1 = db.query(query1)  # is a list of dict.

    num_impossible_weight_changes=0  # values larger than 100 or smaller than -100
    tot_users=0
    tot_users_2weigh_ins=0
    tot_users_6months=0
    tot_users_2weigh_ins_6months=0

    list_weight_changes_before_6months=[]
    list_weight_changes_after_6months=[]

    list_days_before_6months=[]
    list_days_after_6months=[]


    contador=0

    for r1 in result1:
     
    #  if contador <= for_testing_max_num_queries:
        contador+=1


        ck_id=r1['ck_id']     
       
        tot_users+=1

        list_before_6months=[]
        list_after_6months=[]

      
        
        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"') order by on_day" 
        result2 = db.query(query2)  # is a list of dicts.

        if len(result2)>min_num_weigh_ins:
          tot_users_2weigh_ins+=1
        
          first_date=result2[0]['on_day']
          last_date=result2[-1]['on_day']
          time_system=(last_date-first_date).days+1

          if time_system >= minimum_time :

            tot_users_6months+=1

            if len(result2)>min_num_weigh_ins:
                tot_users_2weigh_ins_6months+=1
                print tot_users,tot_users_2weigh_ins_6months

          #  print ck_id

            for r2 in result2:
                fecha= r2['on_day']
                weight=r2['weight']
                num_days=(fecha-first_date).days+1

                lista=[]
                lista.append(num_days)
                lista.append(weight)
               
                if num_days < minimum_time:
                   list_before_6months.append(lista)
                else:
                    list_after_6months.append(lista)

              #  print fecha, num_days,weight
          
            weight_change_before=list_before_6months[-1][1]-list_before_6months[0][1]
            if weight_change_before < impossible_weight_change and weight_change_before > -impossible_weight_change :
                list_weight_changes_before_6months.append(weight_change_before)
            else:
                num_impossible_weight_changes+=1

           
            weight_change_after=list_after_6months[-1][1]-list_after_6months[0][1]
            if weight_change_after < 100. and weight_change_after > -100. :
                list_weight_changes_after_6months.append(weight_change_after)
            else:
                num_impossible_weight_changes+=1


            days_after=list_after_6months[-1][0]-list_after_6months[0][0]
            list_days_after_6months.append(days_after)

            days_before=list_before_6months[-1][0]-list_before_6months[0][0]
            list_days_before_6months.append(days_before)


           # print 'weight change before 6months:',weight_change_before,'  over:',days_before,'days,  counting',len(list_before_6months),'weigh_ins'
            #print 'and after:',weight_change_after, 'over:',days_after,'days,  counting',len(list_after_6months),'weigh_ins\n'
            



    print "tot number of users:",len(result1),"  ||  num users >= 2 weigh-ins:", tot_users_2weigh_ins , "  ||  num users  >= 6months:", tot_users_6months, "  ||  num users >= 2 weigh-ins and >= 6months:", tot_users_2weigh_ins_6months,"\n"

    print  "average weight change before 6months:", numpy.mean(list_weight_changes_before_6months), "SD:", numpy.std(list_weight_changes_before_6months), \
        "over:", numpy.mean(list_days_before_6months), "days on average, SD:",numpy.std(list_days_before_6months)
    print  "average weight change after 6months:", numpy.mean(list_weight_changes_after_6months), "SD:", numpy.std(list_weight_changes_after_6months), \
        "over:", numpy.mean(list_days_after_6months), "days on average, SD:",numpy.std(list_days_after_6months),"\n"



   

    ks=stats.ks_2samp(list_weight_changes_before_6months,list_weight_changes_after_6months) 
    print "KS test for list weight changes before vs after the 6months:",ks

    print "number of impossible weight changes:",num_impossible_weight_changes


    num_users_regain=0.
    for item in list_weight_changes_after_6months:
        if item >0.:
            num_users_regain+=1.

    print "fraction users who (re)gain weight from the 6month mark on:",num_users_regain/float(len(list_weight_changes_after_6months)), "(average over",len(list_weight_changes_after_6months), "users)"

    num_users_gain=0.
    for item in list_weight_changes_before_6months:
        if item >0.:
            num_users_gain+=1.

    print "fraction users who gain weight during the first 6months:",num_users_gain/float(len(list_weight_changes_after_6months)), "(average over",len(list_weight_changes_after_6months), "users)"



    histograma_bines_gral.histograma_bins(list_weight_changes_before_6months,30, "weight_change_before_6months")
    histograma_bines_gral.histograma_bins(list_weight_changes_after_6months,30, "weight_change_after_6months")

################################################

          
if __name__ == '__main__':
  

    main()
   
     

##############################################
