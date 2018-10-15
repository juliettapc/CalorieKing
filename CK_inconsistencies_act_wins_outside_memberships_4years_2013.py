#! /usr/bin/env python

'''
Code to check the different activity tables (blogs, forums, steps, w-ins) and compare against the membership
 periods for each user, to see if they are consistent or they have activity outside them.


Written by Julia Poncela-Casasnvas on June 2013.

'''


import csv
import networkx as nx
import numpy
import sys
import operator
from scipy import stats
import ols   # script to do multi variable linear regressions
from database import *   #package to handle databases
import pickle
import matplotlib.pyplot as plt
from datetime import *
import dateutil
import histograma_bines_gral
import histograma_gral


def main():




  
    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 





    filename0="./analysis_time_bins_bmi_groups/inconsistent_users_steps_outside_membership_periods_2013.dat"
    file0 = open(filename0,'wt')
    print >> file0, "ck_id  [start_date, stop_date]s   'step_date:' step_date "



    filename1="./analysis_time_bins_bmi_groups/inconsistent_users_activity_outside_membership_periods_2013.dat"
    file1 = open(filename1,'wt')
    print >> file1, "ck_id  [start_date, stop_date]s   'act_date:' act_date "



    filename2="./analysis_time_bins_bmi_groups/inconsistent_users_weigh_ins_outside_membership_periods_2013.dat"
    file2 = open(filename2,'wt')
    print >> file2, "ck_id  [start_date, stop_date]s   'w_date:' weigh_in_date "


  


    filename12="./analysis_time_bins_bmi_groups/inconsistent_users_join_date_start_membership_2013.dat"
    file12 = open(filename12,'wt')
    print >> file12, "ck_id  join_date  membership_start   discrepancy_days"


    filename4="./analysis_time_bins_bmi_groups/scatter_plot_membership_vs_tot_engagement_times_2013.dat"
    file4 = open(filename4,'wt')

    filename5="./analysis_time_bins_bmi_groups/scatter_plot_membership_vs_tot_engagement_for_Activity_times_2013.dat"
    file5 = open(filename5,'wt')
      

    dict_users_membership_periods={}


    last_day_of_database=datetime(2012,12,31)   #datetime(yy,mm,ddt)   
    starting_date=datetime(2009,1,1)   #datetime(yy,mm,ddt)

    current_date=starting_date


    dict_ck_id_delta_activity_combined={}
    dict_ck_id_delta_activity={}


    dict_num_users_first_win_month={}
    dict_num_users_first_act_month={}  
    dict_num_users_first_steps_month={}  
    dict_num_users_first_tot_act_month={}   # activity (not weigh_ins) plus steps
    dict_num_users_first_tot_act_month={}   # activity (not weigh_ins) plus steps
    dict_num_users_join_month={}   # activity (not weigh_ins) plus steps

    for i in range(24):   # 2 years, month by month, to save number of users
       # print current_date   # that start their w-in history and act then 
        dict_num_users_first_win_month[current_date]=[]
        dict_num_users_first_act_month[current_date]=[]     
        dict_num_users_first_steps_month[current_date]=[]     
        dict_num_users_first_tot_act_month[current_date]=[]   
        dict_num_users_join_month[current_date]=[]   

        current_date+= dateutil.relativedelta.relativedelta(months=1) #timedelta(months=1) DOESNT EXIST!!

             

    cont_num_users=0
    cont_num_users_with_wins=0
    matching_users_join_first_win=0
    aprox_matching_users_join_first_win =0
    
    num_users_with_start=0   # for membership periods
    num_users_with_stop=0
    num_users_same_join_start=0
    num_users_multiple_period=0
 
    list_join_dates_inconsistent_users=[]
    list_day_discrepancies_inconsistent_users=[]
    
    list_users=[]
    list_users_outside_w_in=[]
    list_users_outside_act=[]
    list_users_outside_steps=[]
    

    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict.       
    
    initial_date_table_users=result1[0]['join_date'].replace( hour=0, minute=0, second=0)   # because some tables have h/min/sec and other dont               
    final_date_table_users=result1[-1]['join_date'].replace( hour=0, minute=0, second=0)                 


    for r1 in result1:      # loop over users
          

  #    if cont_num_users<1000:   ####################### just to test the code out





          if r1['act_prior2009']=="NO":   # there are 158 users with act prior 2009


           
            cont_num_users+=1
       

            ck_id =str(r1['ck_id'])
            join_date=r1['join_date'].replace( hour=0, minute=0, second=0)               
            print cont_num_users
                        #if join_date >=  initial_date_table_users:   # everybody fullfils this condition    
           
            if ck_id not in list_users:
                list_users.append(ck_id)

            dict_users_membership_periods[ck_id]={}

            for llave_date in dict_num_users_join_month:  # find out number user with join_in date on every month              
                if (join_date >= llave_date)  and  (join_date < llave_date + dateutil.relativedelta.relativedelta(months=1)):
                    dict_num_users_join_month[llave_date].append(ck_id)





            dict_ck_id_delta_activity[ck_id]=0
            dict_ck_id_delta_activity_combined[ck_id]=0

            ######### activity records for the scatter plot membership vs engagement times
            query6="select  * from activity_combined where ck_id ='"+str(ck_id)+"'  order by activity_date asc"
            result6= db.query(query6)   

            if len(result6)>0:
                first_act_date=result6[0]['activity_date'].replace( hour=0, minute=0, second=0)                  
                last_act_date=result6[-1]['activity_date'].replace( hour=0, minute=0, second=0)   
               

                delta_activity=(last_act_date-first_act_date).days + 1
                dict_ck_id_delta_activity_combined[ck_id]=delta_activity   # for the scatter plot engagement vs. membership
                                
            
            



            ############# membership periods
            query5_asc="select  * from membership_periods where ck_id ='"+str(ck_id)+"' order by start_date"  
            result5_asc= db.query(query5_asc)            

            # each row is a membership period, with start and stop (or open date), associated payment plan etc

            flag_start=0           
            flag_end=None
            multiple_periods=len(result5_asc)
           
          
            
            cont_pairs=0
           
            for r5 in result5_asc:            
               
                membership_start=r5['start_date'].replace( hour=0, minute=0, second=0)      
                try:    
                    membership_stop=r5['end_date'].replace( hour=0, minute=0, second=0)      
                except AttributeError:
                          membership_stop=r5['end_date']  # if its value is None
                       

                pair_start_end=[]

                pair_start_end.append(membership_start)
                pair_start_end.append(membership_stop) 

                dict_users_membership_periods[ck_id][cont_pairs]=pair_start_end
     
                cont_pairs+=1                    

            
            for i in range(len(dict_users_membership_periods[ck_id])):
                 # because this index starts at 1
                start=dict_users_membership_periods[ck_id][i][0]
                if dict_users_membership_periods[ck_id][i][1]  != None:
                    stop=dict_users_membership_periods[ck_id][i][1]
                else:
                    stop=last_day_of_database
            


                delta_time_start_stop=calculate_proper_delta_times(start, stop)
                  

                print >> file4, delta_time_start_stop,dict_ck_id_delta_activity_combined[ck_id]                        
              
           
            if multiple_periods>1:
                num_users_multiple_period+=1
           

            
            if  calculate_proper_delta_times( dict_users_membership_periods[ck_id][0][0], join_date) == 0  : 
                num_users_same_join_start+=1







            ######### weigh_ins records
            query2="select  * from weigh_in_history where ck_id ='"+str(ck_id)+"' order by on_day asc"
            result2= db.query(query2)   

            first_weigh_in_date=result2[0]['on_day']
            last_weigh_in_date=result2[-1]['on_day']
       

            if (first_weigh_in_date >= initial_date_table_users  and first_weigh_in_date <= final_date_table_users)  or  ( last_weigh_in_date >= initial_date_table_users  and last_weigh_in_date <= final_date_table_users)  or  ( first_weigh_in_date <= initial_date_table_users  and last_weigh_in_date >= final_date_table_users ):
                cont_num_users_with_wins+=1



            for llave_date in dict_num_users_first_win_month:  # find out number user with first w-in on every month
              
                if (first_weigh_in_date >= llave_date)  and  (first_weigh_in_date < llave_date + dateutil.relativedelta.relativedelta(months=1)):
                    dict_num_users_first_win_month[llave_date].append(ck_id)


            last_start=starting_date
            last_stop=starting_date
            flag_open_close="close"   # either the user has and open end, or a closed one
            for llave in dict_users_membership_periods[ck_id]:   # loop over membership periods
                pair_start_stop=dict_users_membership_periods[ck_id][llave]

                if pair_start_stop[1]== None:
                    flag_open_close="open" 
                    last_stop=last_day_of_database
                else:
                    if pair_start_stop[1] >=last_stop:
                        last_stop= pair_start_stop[1]


                if pair_start_stop[0] >=last_start:
                    last_start= pair_start_stop[0]

               
           
            for r2 in result2:   #loop over weigh-ins


              flag_outside=1   # if w-in recordd outside membership period                              
              weigh_in_date=r2['on_day']


              if  weigh_in_date <=  last_day_of_database and weigh_in_date >= starting_date  :    


                for llave in dict_users_membership_periods[ck_id]:   # loop over membership periods
                    pair_start_stop=dict_users_membership_periods[ck_id][llave]
                    
                    start_period_date=pair_start_stop[0]
                    if pair_start_stop[1] != None:
                        stop_period_date=pair_start_stop[1]
                    else:
                        stop_period_date=last_day_of_database                        
                  

                    if weigh_in_date >= start_period_date and  weigh_in_date <= stop_period_date:
                        flag_outside =0
                        break
                    if weigh_in_date >=last_day_of_database and flag_open_close=="open" :# weigh-ins after the end of database for open accounts dont worry me
                        flag_outside =0
                        break


                if flag_outside == 1:
                    print >> file2, ck_id,  dict_users_membership_periods[ck_id],"  w_date:", weigh_in_date
                    print ck_id, dict_users_membership_periods[ck_id],"  w_date:", weigh_in_date
                
                     
                    if ck_id not in list_users_outside_w_in:
                        list_users_outside_w_in.append(ck_id)
     


            


            ######### activity (excluding weigh_ins) records
            query3="select  * from activity_combined where ck_id ='"+str(ck_id)+"' and activity_flag !='WI' order by activity_date asc"
            result3= db.query(query3)            

            if len(result3)>0:
                first_act_date=result3[0]['activity_date'].replace( hour=0, minute=0, second=0)
                last_act_date=result3[-1]['activity_date'].replace( hour=0, minute=0, second=0)
               
                for llave_date in dict_num_users_first_act_month:  # find out number user with first act on every month
                    if (first_act_date >= llave_date)  and  (first_act_date < llave_date + dateutil.relativedelta.relativedelta(months=1)):
                        dict_num_users_first_act_month[llave_date].append(ck_id)
                        


                delta_activity=(last_act_date-first_act_date).days + 1
                dict_ck_id_delta_activity[ck_id]=delta_activity

 

                for r3 in result3:   #loop over act

                  flag_outside=1   # if act recordd outside membership period                              
                  act_date=r3['activity_date'].replace( hour=0, minute=0, second=0)
                 
    
                  if  act_date <=  last_day_of_database and act_date >= starting_date :    # i ignore steps  pst dec 2012


                    for llave in dict_users_membership_periods[ck_id]:   # loop over membership periods
                        pair_start_stop=dict_users_membership_periods[ck_id][llave]
                        
                        start_period_date=pair_start_stop[0]
                        if pair_start_stop[1] != None:
                            stop_period_date=pair_start_stop[1]
                        else:
                            stop_period_date=last_day_of_database                        
                  

                        if act_date >= start_period_date and  act_date <= stop_period_date:
                            flag_outside =0
                            break
                        if act_date >=last_day_of_database and flag_open_close=="open" :# act after the end of database for open accounts dont worry me
                            flag_outside =0
                            break

                    if flag_outside == 1:
                        print >> file1, ck_id,   dict_users_membership_periods[ck_id],"  act_date:", act_date
                        print ck_id, dict_users_membership_periods[ck_id],"  act_date:", act_date
                        
                         

                   # else:
                    #    print ck_id, dict_users_membership_periods[ck_id],"  act_date:", act_date

                        if ck_id not in list_users_outside_act:
                            list_users_outside_act.append(ck_id)
     






            ############## daily steps records
            query4="select  * from daily_steps where ck_id ='"+str(ck_id)+"'  order by on_day asc"
            result4= db.query(query4)  
            
            if len(result4)>0:
                first_steps_date=result4[0]['on_day']                            
                last_steps_date=result4[-1]['on_day']
                               
                
                for llave_date in dict_num_users_first_steps_month:  # find out number user with first steps on every month
                    if (first_steps_date >= llave_date)  and  (first_steps_date < llave_date + dateutil.relativedelta.relativedelta(months=1)):
                        dict_num_users_first_steps_month[llave_date].append(ck_id)
                        

                for r4 in result4:   #loop over steps

                  flag_outside=1   # if w-in recordd outside membership period                              
                  step_date=r4['on_day']
                 
          
                  if  step_date <=  last_day_of_database and step_date >= starting_date :  


                    for llave in dict_users_membership_periods[ck_id]:   # loop over membership periods
                        pair_start_stop=dict_users_membership_periods[ck_id][llave]
                        
                        start_period_date=pair_start_stop[0]
                        if pair_start_stop[1] != None:
                            stop_period_date=pair_start_stop[1]
                        else:
                            stop_period_date=last_day_of_database                        
                  

                        if step_date >= start_period_date and  step_date <= stop_period_date:
                            flag_outside =0
                            break
                        if step_date >=last_day_of_database and flag_open_close=="open" :# weigh-ins after the end of database for open accounts dont worry me
                            flag_outside =0
                            break

                    if flag_outside == 1:
                        print >> file0, ck_id,   dict_users_membership_periods[ck_id],"  step_date:", step_date
                        print ck_id, dict_users_membership_periods[ck_id],"  step_date:", step_date
                    
                        if ck_id not in list_users_outside_steps:
                            list_users_outside_steps.append(ck_id)
                        
                       
               
            if calculate_proper_delta_times(first_weigh_in_date , join_date) == 0  : 
                matching_users_join_first_win +=1

            if abs(calculate_proper_delta_times(first_weigh_in_date , join_date)) <=1  : 
                aprox_matching_users_join_first_win +=1
            else:
                list_join_dates_inconsistent_users.append(join_date)
                list_day_discrepancies_inconsistent_users.append(calculate_proper_delta_times(first_weigh_in_date , join_date))



    ######## for the scatter plot
    for ck_id in list_users:
        for i in range(len(dict_users_membership_periods[ck_id])):
             # because this index starts at 1
            start=dict_users_membership_periods[ck_id][i][0]
            if dict_users_membership_periods[ck_id][i][1]  != None:
                stop=dict_users_membership_periods[ck_id][i][1]
            else:
                stop=last_day_of_database
                
                
                
                delta_time_start_stop=calculate_proper_delta_times(start, stop)
                

            print >> file5, delta_time_start_stop,dict_ck_id_delta_activity[ck_id]
            


                    
    print "tot number users who joined after", initial_date_table_users, "is:", cont_num_users
    print "tot number users who joined after and have weigh ins within those 2years",  cont_num_users_with_wins

    print "\nnum users for whom join_date = first_weigh_in:",matching_users_join_first_win
    print "num users for whom join_date aprox first_weigh_in (within +/- 1days):", aprox_matching_users_join_first_win

    print "\nnumber of users with start membership info:",num_users_with_start
    print "number of users with stop membership info:",num_users_with_stop

    print "\nnumber of users same join & membership first date:",num_users_same_join_start
    print "number of users multiple memberships:", num_users_multiple_period

    list_sorted_w_ins = sorted(dict_num_users_first_win_month.items(), key=lambda x: x[0])  # if 0: by key, if 1: value
    list_sorted_act = sorted(dict_num_users_first_act_month.items(), key=lambda x: x[0])  
    list_sorted_steps = sorted(dict_num_users_first_steps_month.items(), key=lambda x: x[0])  
    list_sorted_join = sorted(dict_num_users_join_month.items(), key=lambda x: x[0])

    filename="./analysis_time_bins_bmi_groups/num_users_first_w_in_act_month_2013.dat"
    file1 = open(filename,'wt')
    for i in range(len(list_sorted_w_ins)):
      #  print i, len(list_sorted_w_ins[i][1]), len(list_sorted_act[i][1]),list_sorted_w_ins[i][0]
        print >> file1,i, len(list_sorted_w_ins[i][1]), len(list_sorted_act[i][1]), len(list_sorted_steps[i][1]),len(list_sorted_join[i][1]),list_sorted_w_ins[i][0]

 


  

    file0.close()
    file1.close()
    file2.close()  
    file4.close()
    file5.close()


    print "written file:",filename0
    print "written file:",filename1
    print "written file:",filename2
    print "written file:",filename4  
    print "written file:",filename5



    print "\n# users with outside w-in:",len(list_users_outside_w_in)
    print "# users with outside act:",len(list_users_outside_act)
    print "# users with outside steps:",len(list_users_outside_steps)

    print "\n# users with outside act and outside w-ins", len(list(set(list_users_outside_act).intersection(list_users_outside_w_in)))
    print "# users with outside act and outside steps", len(list(set(list_users_outside_steps).intersection(list_users_outside_w_in)))

   

    print "written file for scatter plot engagement vs. membership:",filename4
    print "written file for scatter plot engagement (concerning activity) vs. membership:",filename5

###################################################
def calculate_proper_delta_times(date_ini, date_fin):   # 27 20     # 20  26

   # print date_ini, date_fin,
    if date_fin >=date_ini :
        dif= (date_fin-date_ini ).days
     
    elif date_fin < date_ini:
        dif = -(date_ini-date_fin).days   # REMEMBER!  2009-01-01 12:18:01 - 2009-01-01 00:00:00 = -1

    #print dif
    return dif

  



################################################
################################################

          
if __name__ == '__main__':
#    if len(sys.argv) > 2:
 #       master_csv = sys.argv[1]
  #      strength_links_csv = sys.argv[2]
       

        main()
   # else:
    #    print "usage: python  whatever.py   path/master.csv  path/strength_links.csv"
 
     

##############################################
