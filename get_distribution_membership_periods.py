#!/usr/bin/env python


'''
Code to get the distribution of lengths and number of membership periods for 
the CK users. Datase 2009-2012 collected in June 2013.

Created by Julia Poncela, on June, 2013

'''


import numpy
import csv
import sys
import os
from datetime import *
from database import *   #package to handle databases
import histograma_gral

def main():
 

    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 

    name1="./list_users_membership_way_into_future.dat"
    file1=open(name1, 'wt')



    last_day=datetime(2012,12,31)  # to close the open memberships



    query1="""select * from users"""    
    result1 = db.query(query1)       
    list_users=[]
    for r1 in result1:  # i create the empty dict
        ck_id=r1['ck_id']
        if r1['act_prior2009']=="NO":   # there are 158 users with act prior 2009          
            list_users.append(ck_id)





    list_membership_lengths=[]
    list_number_membership_per_user=[]
    list_membership_gaps=[]

    query1="""select * from membership_periods order by ck_id, start_date"""    
    result1 = db.query(query1)         
        
    previous_ck_id=None
    previous_end_date=None

    number_memberships_one_user=1
    list_memberships_per_user=[]
    num_users_starting_after2012=0
    list_crazy_end_dates=[]
    cont=1
    for r1 in result1:  # list of dicts
      ck_id=r1['ck_id']
      start_date=r1['start_date']
      end_date=r1['end_date']
      if ck_id in list_users:   # i exclude the 158 users with act. prior Jan 2009

        if start_date <=last_day  :  # i dont include memberships newer than that
            if end_date: # if the membership has an end
                number_days=(end_date-start_date).days                
            else:  # if the membership is still open
                end_date=last_day
                number_days=(end_date-start_date).days      

            print cont, ck_id, start_date, end_date, number_days
            list_membership_lengths.append(number_days)

            if number_days > 1461 :  # if more than 4years
                list_crazy_end_dates.append(number_days)
                print >> file1, ck_id, start_date, end_date , number_days
        else:
            num_users_starting_after2012 +=1
       


        if cont >1: # to exclude the first entry
                
            if ck_id  != previous_ck_id:
                list_memberships_per_user.append(number_memberships_one_user)
                number_memberships_one_user=1                   

            else:
                number_memberships_one_user +=1
                list_membership_gaps.append((start_date-previous_end_date).days)
                print "  gap!", start_date, end_date,"-->",(start_date-previous_end_date).days
              

        previous_end_date= end_date
        previous_ck_id=ck_id
       

        cont +=1

    print "building histogram membership lenghts..."
    histograma_gral.histograma(list_membership_lengths,"./histogram_lengths_membership_periods.dat")   

    print "building histogram # membership periods per user..."
    histograma_gral.histograma(list_memberships_per_user,"./histogram_number_membership_per_user.dat")    

    print "building histogram between-membership gap lenghts..."
    histograma_gral.histograma(list_membership_gaps,"./histogram_gap_lengths_between_memberships.dat") 



  
    file1.close()
    print "written:", name1

    print "\n# users starting after 2012:",num_users_starting_after2012
    print "tot # gaps in between memberhips:",len(list_membership_gaps)
##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py path/filename"

    
