#!/usr/bin/env python


'''
Create segments of the original weigh time series, only including the first
membership periods, defined as the membership_period form the database table
or if two are separated by less than 30days. These segments will be used 
to study the evolution of the weight in the "initiation" part of their stay in the system.

Created by Julia Poncela, June  2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from datetime import *
from database import *   #package to handle databases


def main():
 

    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 



    small_membership_gap=30  # days  (to consider two membership periods as one)
    end_initiation=182 # days


    last_day=datetime(2012,12,31)  # to close the open memberships


    ######## i filter out the users with activity prior 2009
    dict_ck_id_list_membership_periods={}
    query1="""select * from users"""    
    result1 = db.query(query1)       
    list_users=[]
    for r1 in result1:  # i create the empty dict
        ck_id=r1['ck_id']

        if r1['act_prior2009']=="NO":   # there are 158 users with act prior 2009
            list_periods_one_user=[]
            dict_ck_id_list_membership_periods[ck_id]=list_periods_one_user
            list_users.append(ck_id)

   

    ####### i get the membership periods for the users
    query2="""select * from membership_periods order by ck_id, start_date"""    
    result2 = db.query(query2)         
    cont=1
    for r2 in result2:  # list of dicts
        ck_id=r2['ck_id']
        start_date=r2['start_date']
        end_date=r2['end_date']
        list_start_end=[]

        if ck_id in list_users:  # only users whose first act is after Januray 2009         
            if start_date <=last_day  :  # i dont include membership periods newer than that
                list_start_end.append(start_date)
                list_start_end.append(end_date)
                dict_ck_id_list_membership_periods[ck_id].append(list_start_end)
                

        print cont," / 80970"   # max
        cont +=1


    ####### i get the last day from the first membership period:   
    user=1
    dict_ck_id_last_day_first_period={}
    for ck_id in dict_ck_id_list_membership_periods:
        #print "\n",ck_id, dict_ck_id_list_membership_periods[ck_id]

        dict_ck_id_last_day_first_period[ck_id]=None

        list_periods=dict_ck_id_list_membership_periods[ck_id]
        if len(list_periods) >1:
            cont=0              
            for item in list_periods:
                start_date= item[0]
                end_date=item[1]
                if cont >0:                      
                    if (start_date - previous_date ).days > small_membership_gap:  # the first big gap i find, defines the end of the first period
                        dict_ck_id_last_day_first_period[ck_id]=previous_date
                        #print  "last day of the first period:", previous_date
                        break

      
                previous_date=end_date
                cont +=1         
           
        user +=1
        print user, " / ",len(dict_ck_id_list_membership_periods)


    ####### i create a new table in the db only including the first period of each user's time series
    db.execute ("DROP TABLE IF EXISTS first_period_weigh_in_history")
    db.execute ("""                      
            CREATE TABLE  first_period_weigh_in_history  
            (        
             on_day           DATETIME,
             ck_id            CHAR(36),     
             weight           FLOAT,                        
             id               INT(11),
             activity_flag    CHAR(3)                 
            )
          """) 



    cont=1
    for ck_id in list_users:  # list of dicts

        query3="""select * from weigh_in_history where ck_id='""" +str(ck_id)+ """' order by on_day"""    
        result3 = db.query(query3)        # list of dicts         

        first_wi_date=result3[0]['on_day']

        for r3 in result3:
            on_day=r3['on_day']
            weight=r3['weight']
            activity_flag=r3['activity_flag']
            index=r3['id']  # this id will match the one in the original weigh_in history

           
            if (on_day-first_wi_date).days < end_initiation:   # i only take the first 6months: initiation period
                
                if dict_ck_id_last_day_first_period[ck_id]:  # if there is a big membership gap, that defines the end of first period
                    if on_day <= dict_ck_id_last_day_first_period[ck_id]:     
                        db.execute ("""
                     INSERT INTO first_period_weigh_in_history (on_day , ck_id, weight, id, activity_flag)
                     VALUES (%s, %s, %s, %s, %s)
                     """, str(on_day),str(ck_id),str(weight), str(index),str(activity_flag) )

                else:
                    db.execute ("""
                INSERT INTO first_period_weigh_in_history (on_day , ck_id, weight, id, activity_flag)
                VALUES (%s, %s, %s, %s, %s)
                """, str(on_day),str(ck_id),str(weight), str(index),str(activity_flag) )


            print cont,  " / 640979"
            cont+=1



##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    filename = sys.argv[1]
   
    main()
    #else:
     #   print "Usage: python script.py path/filename"
