
#! /usr/bin/env python

"""
Created by Julia Poncela of January 2013

Get some statistics on time series cutting from the database



"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import histograma_gral
import histograma_bines_gral

 
def main ():

    min_wi=20  #Filter1:  min number of weigh ins >=
    min_timespan=0       # Filter2: min lenght of the serie

   
   
    filename4="./Results/More_summary_statistics_cutting_time_series.dat"
    file4=open(filename4,'wt')
   



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



   
    query="""select * from users""" 

   
    result1 = db.query(query)  # is a list of dict.

    num_users=len(result1)

    cont=0
    for r1 in result1:   #loop over users to get their number_of_weigh-ins
                               
        ck_id=r1['ck_id']       ## the ck_id from the weigh_in_cut table is a shorter id than the one in the users table
        


#weigh_ins_query = db.query('''
 #      SELECT on_day, weight
  #     FROM weigh_in_history
   #    WHERE ck_id LIKE %s
    #   ORDER BY on_day
     #  ''', user_id + '%')


        
        result4 = db.query(''' SELECT on_day, weight FROM weigh_in_history WHERE ck_id LIKE %s  ORDER BY on_day''', ck_id + '%')#THIS QUERY IS JUST TO TEST IT OUT!!
  # is a list of dict.
        print result4
        for r4 in result4:
            print r4
        
        cont+=1 
        print cont
        
    exit()
        




    list_num_segments_per_user=[]
    list_num_gaps_per_user=[]


    num_segments=0
    num_lin_segments=0
    num_exp_segments=0
    num_isolated=0
    num_gaps=0
    num_valid_users=0

    list_lenghts=[]
    list_lin_lenghts=[]
    list_exp_lenghts=[]



    for r1 in result1:   #loop over users to get their number_of_weigh-ins

        
        ## r1 is a dict.:  {'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6', 'age': 52L, 'state': u'', 'height': 64L, 'join_date': datetime.datetime(2009, 11, 27, 10, 41, 5), 'is_staff': u'public', 'most_recent_weight': 142.0, 'initial_weight': 144.0, 'id': 1L}

        ck_id=r1['ck_id']
        

        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       
       


        r1['num_wi']=len(result2)  # i add another key-value to the dict. -->> with this i ALSO modify the list of dict. result!!!

       
        first=result2[0]['on_day']
        last=result2[-1]['on_day']
        time_span_days=(last-first).days+1
      

        if r1['num_wi']>=min_wi   :#and   int(time_span_days) >= min_timespan:                 
               
            num_valid_users=num_valid_users+1
           
            print num_valid_users
                   

            query3="select * from weigh_in_cuts  where (ck_id ='"+str(ck_id)+"') order by id, start_day"
            result3 = db.query(query3)  # is a list of dict.

            list_num_segments_per_user.append(len(result3))
    
    

            for r3 in result3:  # each line is a dict, each line is a segment
       
        
                fit_type=str(r3['fit_type'])
                start_day=int(r3['start_day'])
                stop_day=int(r3['stop_day'])
                start_weight=float(r3['start_weight'])
                stop_weight=float(r3['stop_weight'])
                
          
                list_lenghts.append(stop_day-start_day+1)
   

                if fit_type == "isolated":      
                    num_isolated+=1

                elif fit_type == "linear":  
                    num_lin_segments+=1
                    list_lin_lenghts.append(stop_day-start_day+1)

                elif fit_type == "exponential":  
                    num_exp_segments+=1
                    list_exp_lenghts.append(stop_day-start_day+1)

               

            query4="SELECT * FROM weigh_in_cuts where (ck_id ='"+str(ck_id)+"') order start_day"   #gap info  3THIS QUERY IS JUST TO TEST IT OUT!!
           # query4="select * from frequency_cuts where (ck_id ='"+str(ck_id)+"') order start_day"   #gap info
            result4 = db.query(query4)  # is a list of dict.

          
            for r4 in result4:
                if r4['param3']==Null:
                    
                    raw_input()



            list_num_gaps_per_user.append(len(result4))
            num_gaps+=len(result4)


                
      
 
    print >> file4, "Summary results cutting time series:\n\n"
    
    print >> file4,"Total number of users:",num_users,", Number users with at least 20 weigh-ins:",num_valid_users
    print >> file4,"Number of segments:", sum(list_num_segments_per_user)  #not including one-point segments   
    print >> file4,"Average number of segments per individual:",numpy.mean(list_num_segments_per_user)
    print >> file4,"Number of one-point segments:",num_isolated
    print >> file4, "Number segments by type:"
    print >> file4, "    Linear: ",num_lin_segments    
    print >> file4, "    Exponential: ",num_exp_segments,"\n"
    print >> file4, "Number of gaps:",num_gaps
    print >> file4,"Average number of segments per individual:",numpy.mean(list_num_gaps_per_user)

    file4.close()





    print "   printed out file: ",filename4


#########################
          
if __name__== "__main__":
   # if len(sys.argv) > 2:
       
        main()
#    else:
 #       print "usage: python whatever.py path/network_file1_R6s_info.gml  path/network_file2_kshell_info.gml "

   
    
     

##############################################
