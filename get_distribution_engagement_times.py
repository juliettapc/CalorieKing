#!/usr/bin/env python


'''
Code to read the CK database and the .gml file(s) to collect all info
on all users and create a csv master file for weight change and activity until 6months

Created by Julia Poncela, on September, 2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from database import *   
from datetime import *
import dateutil
import histograma_gral


def main():
 


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 




    ################

    end_initiation=182 # days
    first_day=datetime(2009,01,01)  # to exclude users with prior act




    ########### output file names for the histograms
    filename0="./analysis_time_bins_bmi_groups/survival_curve_all.txt"
    
    filename1="./analysis_time_bins_bmi_groups/survival_curve_2weigh_ins.txt"

    filename2="./analysis_time_bins_bmi_groups/survival_curve_networked.txt"
    ###
    filename3="./analysis_time_bins_bmi_groups/distribution_delta_times_to_6month_mark_all.txt"
    
    filename4="./analysis_time_bins_bmi_groups/distribution_delta_times_to_6month_mark_2wins.txt"

    filename5="./analysis_time_bins_bmi_groups/distribution_delta_times_to_6month_mark_networked.txt"
    
    
    ############






   ################
    csv_file="analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_2w_ins.txt"

    num_degree_nonzero=0
    num_pfriends1=0
    dict_ck_id_friends={}
    file_csv_info=open(csv_file,'r')
    list_lines_file_csv_info=file_csv_info.readlines() 
    cont=0
    for line in list_lines_file_csv_info:
        if cont >0: 
            list_elements_line=line.strip("\r\n").split(" ")
            
            ck_id=str(list_elements_line[0])     
            label=str(list_elements_line[1])      
            degree=int(list_elements_line[26])
            p_friends=int(list_elements_line[20])

#            if degree >0 :  # 2277
 #               num_degree_nonzero+=1

   #         if p_friends >0:  # 2277
  #              num_pfriends1 +=1

            dict_ck_id_friends[ck_id]=degree
        cont+=1

    #print num_degree_nonzero, num_pfriends1

#    print len(dict_ck_id_friends)    # 26653



    print "getting users with activity prior 2009 (to be excluded)....."
    #########################                     
    query4="select  * from activity_combined order by activity_date asc"
    result4= db.query(query4)                

    list_users_prior2009=[]
    for r4 in result4:

        ck_id=r4['ck_id']
        act_date=r4['activity_date']
        act_date=datetime(act_date.year, act_date.month, act_date.day)    # convert date to datetime

        if act_date < first_day:
            if ck_id not in list_users_prior2009:
                list_users_prior2009.append(ck_id)

    print  "# users activity prior 2009:", len(list_users_prior2009)





    print "getting list of users from dB....."
    #########################                     
    dict_master_user_info={}


    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict.   
    list_users=[] 

    
    testing_cont=0
    for r1 in result1:

      #  if   testing_cont <= 1000 :  # TO TEST THE CODE
            ck_id =str(r1['ck_id'])
            join_date=r1['join_date']
            
            if ck_id not in list_users_prior2009:
                
                list_users.append(ck_id)
                dict_master_user_info[ck_id]={}
                
                dict_master_user_info[ck_id]['join_date']=join_date
  

       # testing_cont+=1


    print "getting users' activity info..."
    #########################   

    list_time_in_sytem_all=[]
    list_time_system_2w_ins=[]
    list_time_system_networked=[]

    list_time_to_6month_mark_all=[]
    list_time_to_6month_mark_2wins=[]
    list_time_to_6month_mark_networked=[]


    cont=0
    for user in list_users:       
        cont+=1
        print cont,"/ 47000"

        list_dates=[]

        join_date= dict_master_user_info[user]['join_date']
        last_date_6months_user=join_date + timedelta(days=end_initiation)               
        last_date_6months_user=datetime(last_date_6months_user.year, last_date_6months_user.month, last_date_6months_user.day)    # convert date to datetime
      
       
       # print user, join_date, last_date_6months_user,"act",last_date_6months_user-join_date

        query4="select  * from activity_combined where ck_id ='"+str(user)+"' order by activity_date asc"      #and activity_flag != '"+str("WI")+"'  and activity_date <= '"+str(last_date_6months_user)+ "' order by activity_date asc"
        result4= db.query(query4)  
    
        
       



        #dict_master_user_info[user]['time_in_system']=(result4[-1]['activity_date']- result4[0]['activity_date']).days #total time in system
        time_in_system=(result4[-1]['activity_date']- result4[0]['activity_date']).days #total time in system
        list_time_in_sytem_all.append(time_in_system)



        num_w_ins=0
        for r4 in result4:
            activity_flag=r4['activity_flag']
            activity_date=r4['activity_date']
            activity_date=datetime(activity_date.year, activity_date.month, activity_date.day) 

            if activity_date <= last_date_6months_user :
                list_dates.append(activity_date)

            if activity_flag =="WI":
                num_w_ins +=1


        if num_w_ins >=2:
            list_time_system_2w_ins.append(time_in_system)

        if user in dict_ck_id_friends:  # the dict only has people with at least 2 weigh-ins
            if dict_ck_id_friends[user] >0:
                list_time_system_networked.append(time_in_system)


        if len(list_dates) > 0:
            last_activity_before_6months=list_dates[-1]
            list_time_to_6month_mark_all.append((last_date_6months_user-last_activity_before_6months).days)
            if num_w_ins >=2:
                list_time_to_6month_mark_2wins.append((last_date_6months_user-last_activity_before_6months).days)

            if user in dict_ck_id_friends:  # the dict only has people with at least 2 weigh-ins
                if dict_ck_id_friends[user] >0:
                    list_time_to_6month_mark_networked.append((last_date_6months_user-last_activity_before_6months).days)


        else:
            print user, "doesnt have act in the first 6months"


    histograma_gral.histograma(list_time_in_sytem_all, filename0)
    histograma_gral.histograma(list_time_system_2w_ins, filename1)
    histograma_gral.histograma(list_time_system_networked, filename2)

    histograma_gral.histograma(list_time_to_6month_mark_all, filename3)
    histograma_gral.histograma(list_time_to_6month_mark_2wins, filename4)
    histograma_gral.histograma(list_time_to_6month_mark_networked, filename5)
  




##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename_network1 = sys.argv[1]
    #    filename_network_for_kshell = sys.argv[2]
   
     #   main(filename_network1,filename_network_for_kshell)
    #else:
     #   print "Usage: python script.py path/filename.gml  path/filename_for_kshell.gml"

    
    main()
