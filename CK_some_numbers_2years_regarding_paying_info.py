#! /usr/bin/env python

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


def main():




    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



    filename3="./analysis_time_bins_bmi_groups/users_multiple_periods_vs_paying.dat"
    file3 = open(filename3,'wt')
 #   print >> file3, " "




                
    

    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict.       
    
    initial_date_table_users=result1[0]['join_date']
    final_date_table_users=result1[-1]['join_date']
    
   
    cont_num_users=0
    cont_num_users_with_wins=0
     
    num_users_with_start=0   # for membership periods
    num_users_with_stop=0
    num_users_same_join_start=0
    num_users_multiple_start=0
    num_users_multiple_stop=0

     
    num_users_pay=0
    num_users_free=0

    num_users_pay_mult_start=0
    num_users_pay_mult_stop=0
    num_users_free_mult_start=0
    num_users_free_mult_stop=0

    num_users_pay_NO_mult_start=0
    num_users_pay_NO_mult_stop=0
    num_users_free_NO_mult_start=0
    num_users_free_NO_mult_stop=0

    num_users_pay_with_start=0   
    num_users_pay_with_stop=0
    num_users_free_with_start=0   
    num_users_free_with_stop=0


    for r1 in result1:   
            cont_num_users+=1


       

      #  if cont_num_users<1000:  ########################### just to test the code out






            print cont_num_users

            ck_id =r1['ck_id']
            join_date=r1['join_date'] 
            paying_info=r1['paying']
                        #if join_date >=  initial_date_table_users:   # everybody fullfils this condition    


            if paying_info =='paid':
                num_users_pay+=1
            elif paying_info =='free':
                num_users_free+=1
           



            ############# membership periods
            query5="select  * from membership_periods where ck_id ='"+str(ck_id)+"' order by on_day desc"  # just in case i have multiple starts, i pick always the oldest
            result5= db.query(query5)            

            query5_stop="select  * from membership_periods where ck_id ='"+str(ck_id)+"' order by on_day asc"  # just in case i have multiple stops, i pick always the oldest
            result5_stop= db.query(query5_stop)            


            flag_start=0
            flag_stop=0
            multiple_start=0
            multiple_stop=0

            membership_start=None
            membership_stop=None
           
            for r5 in result5:            
                
                if r5['type']=="START":

                    membership_start=r5['on_day']
                    membership_start=datetime.combine(membership_start, time())   # need to convert from date to datetime (because weigh in are datetime) 
                    flag_start=1
                    multiple_start+=1
                   
            for r5 in result5_stop:     
                if r5['type']=="END":
                    membership_stop=r5['on_day']
                    membership_stop=datetime.combine(membership_stop, time())   
                    flag_stop=1
                    multiple_stop+=1

            num_users_with_start+=flag_start
            num_users_with_stop+=flag_stop
          
  

          #  print  >> file3, ck_id,  multiple_start, multiple_stop, paying_info
           
            if multiple_start>1:
                num_users_multiple_start+=1

                if paying_info =='paid':
                    num_users_pay_mult_start +=1
                elif paying_info =='free':
                    num_users_free_mult_start+=1

            else:
                if paying_info =='paid':
                    num_users_pay_NO_mult_start+=1
                elif paying_info =='free':
                    num_users_free_NO_mult_start+=1
               


            if multiple_stop>1:
                num_users_multiple_stop+=1

                if paying_info =='paid':
                    num_users_pay_mult_stop +=1
                elif paying_info =='free':
                    num_users_free_mult_stop+=1

            else:
                if paying_info =='paid':
                    num_users_pay_NO_mult_stop+=1
                elif paying_info =='free':
                    num_users_free_NO_mult_stop+=1

 

            if flag_start==1:
                if paying_info =='paid':
                    num_users_pay_with_start+=1
                elif paying_info =='free':
                    num_users_free_with_start+=1
            if flag_stop==1:
                if paying_info =='paid':
                    num_users_pay_with_stop+=1
                elif paying_info =='free':
                    num_users_free_with_stop+=1




            if  calculate_proper_delta_times(membership_start , join_date) == 0  : 
                num_users_same_join_start+=1


          
    print >> file3, "\n# users paid:",num_users_pay
    print >> file3, "   and have multiple starts:",num_users_pay_mult_start, "  dont:",num_users_pay_NO_mult_start
    print >> file3, "   and have multiple stops:",num_users_pay_mult_stop, "  dont:",num_users_pay_NO_mult_stop

    print >> file3, "# users free:",num_users_free
    print >> file3, "   and have multiple starts:",num_users_free_mult_start, "  dont:",num_users_free_NO_mult_start
    print >> file3, "   and have multiple stops:",num_users_free_mult_stop, "  dont:",num_users_free_NO_mult_stop



    print >> file3, "\n# users with start:",num_users_with_start
    print >> file3, "   and have paid:",num_users_pay_with_start," free:",num_users_free_with_start
    
    print >> file3, "# users with stop:",num_users_with_stop
    print >> file3, "   and have paid:",num_users_pay_with_stop," free:",num_users_free_with_stop
  



    file3.close()
    print  "written:", filename3

###################################################
def calculate_proper_delta_times(date_ini, date_fin):   # 27 20     # 20  26

   # print date_ini, date_fin,
    if date_fin >=date_ini :
        dif= (date_fin-date_ini ).days
     
    elif date_fin < date_ini:
        dif = -(date_ini-date_fin).days   # REMEMBER!  2009-01-01 12:18:01 - 2009-01-01 00:00:00 = -1  !!!!

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
