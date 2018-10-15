
#! /usr/bin/env python

"""
Created by Julia Poncela on July  2012.

Given a set of time series (in files), it creates a new table in the MT_time_series DB and populates it with the data
from the MT fake time series.




"""

import csv
import sys
import os
from datetime import *
import math
import numpy as np
from scipy import stats
from database import *   #package to handle databases


def main (csv_file):



    database = "MT_time_series"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 

    db.execute ("DROP TABLE IF EXISTS subjective_weigh_in_history")  #i remove the old table 
  

 

    #i create a new table in an existing DB  
    db.execute ("""                      
       CREATE TABLE subjective_weigh_in_history
       (
         ck_id INT,
         weight FLOAT,
         on_day DATETIME,
         id   INT,
         activity_flag  CHAR (2)
                   
       )
     """) # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 





    activity_flag='WI'

    resultado_csv= csv.reader(open(csv_file, 'rb'), delimiter=',')#, quotechar='"')
    #weight_week1, weight_week_week2, weight_week3,... weight_week8





    current_ck_id=str(51)   # first id in the file  THIS MAY CHANGE WITH OTHER FILES!!!!!!!!!!

    old_ck_id=str(51)

    list_weight_values=[]           
    list_percent_weight_changes=[]  
    list_dates=[]
    print "first id", current_ck_id

   
    cont=0  # for the tot number of lines of the one and only datafile
    for row in resultado_csv:       
        
        if cont>0:     # i skip the header line     
            ck_id=str(row[0])
          
            print ck_id          
            
            if ck_id== current_ck_id:
               

                weight=float(row[2])

                complete_date=row[1].split("-")
                year=int(complete_date[0].strip(" "))
                month=int(complete_date[1].strip(" "))
                day=int(complete_date[2].strip(" "))
             
                weight_date=datetime(year, month, day, 0, 0) 
 
                list_weight_values.append(float(weight))
                list_dates.append(weight_date)


              #  print len(list_weight_values)
                if len(list_percent_weight_changes)  ==0:
                    first_weight=float(weight)
                    first_date=weight_date
                    print "first_weight:",first_weight,"first enty"

                else:
                    first_weight =list_weight_values[0]
                    first_date=list_dates[0]

                    print " first_weight:",first_weight,"rest of them"

                  
                list_percent_weight_changes.append(100.*(weight-first_weight)/first_weight)

              #  print "  ",ck_id,weight_date, weight_date-first_date,weight,100.*(weight-first_weight)/first_weight 
               
           
            

            else :                               
                print "new id", ck_id
                cont_entries_one_user=1


                file_name="fake_time_series/Bonnies_study/subjective_weight_time_series_"+str(old_ck_id)+".dat" 
                file=open(file_name,'wt')

              
                for i in range(len(list_weight_values)):      # i print the series for the previous user        
                   
                    weight=list_weight_values[i]  
                    on_day=list_dates[i]                     
                    
                    db.execute ("""
                        INSERT INTO subjective_weigh_in_history (ck_id, weight, on_day, id, activity_flag)
                        VALUES (%s, %s, %s, %s,%s)
                        """, str(old_ck_id), str(weight),str(on_day),str(old_ck_id), str(activity_flag))

              

                    print >> file, (on_day-first_date).days,list_percent_weight_changes[i],list_weight_values[i],list_dates[i]
                    print  old_ck_id, (on_day-first_date).days,list_percent_weight_changes[i],list_weight_values[i],list_dates[i]

                   
                list_weight_values=[]           # i get ready for the next user, and i save this entry as the first one of the new time series
                list_dates=[]
                list_percent_weight_changes=[]  
                current_ck_id=ck_id
                old_ck_id=ck_id

                weight=float(row[2])
               
                
                complete_date=row[1].split("-")
                year=int(complete_date[0].strip(" "))
                month=int(complete_date[1].strip(" "))
                day=int(complete_date[2].strip(" "))
                weight_date=datetime(year, month, day, 0, 0)  
             

                list_weight_values.append(float(weight))
                list_dates.append(weight_date)     


                if len(list_percent_weight_changes)  ==0:
                    first_weight=float(weight)
                    first_date=weight_date
                   # print "first_weight:",first_weight,"first enty"

                else:
                    first_weight =list_weight_values[0]
                    first_date=list_dates[0]

                  #  print " first_weight:",first_weight,"rest of them"




                list_percent_weight_changes.append(100.*(weight-first_weight)/first_weight)
               # print "  ",ck_id,weight_date, (weight_date-first_date).days, weight, 100.*(weight-first_weight)/first_weight


        cont+=1









    #query="""describe weigh_in_history""" 
   









	   
     

##############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
       
       

        main(csv_file)
    else:
        print "usage: python  whatever.py   path/csv_file_subjective_weight_time_series.csv "
 
     
