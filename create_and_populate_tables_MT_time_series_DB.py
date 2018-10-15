
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


    arbitrary_initial_date=datetime(2009, 1, 1, 0, 0)   # because the MT time series are generated starting at an arbitrary day=0
   



    database = "MT_time_series"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"

    db= Connection(server, database, user, passwd) 


    db.execute ("DROP TABLE IF EXISTS weigh_in_history")  #i remove the old table 
  

 

    #i create a new table in an existing DB  
    db.execute ("""                      
       CREATE TABLE weigh_in_history
       (
         ck_id INT,
         weight FLOAT,
         on_day DATETIME,
         id   INT,
         activity_flag  CHAR (2)
                   
       )
     """) # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 






    resultado_csv= csv.reader(open(csv_file, 'rb'), delimiter=',')#, quotechar='"')
    #weight_week0, weight_week_week1, weight_week2,... weight_week29

    cont=0
    for row in resultado_csv:
        ck_id=cont+1   # the fake ck_id (and the id) will both be the line count from the csv file
        id=cont+1
        activity_flag='WI'

        if cont>0:     # i skip the header line     

            print "line:",cont+1,row 
            list_weight_values=[]
            flag_skip_line=0
            list_values_days=[]
            cont_week=0

            for element in row:                 
                if len(element) >0:  # if it is  not an empty enty
                    try:
                        value=float(element)
                        if value >200.0 and value < 400.0:   # i remove bad data                    
                            list_weight_values.append(value)
                            list_values_days.append(cont_week*7)
                  #     else:
                  #        flag_skip_line=1
                    except  ValueError: pass   # in case the value is not a numberic character
                              
                cont_week+=1

            if len(list_weight_values)<10:   # if after removing bad data i still have a long enough time serie
                flag_skip_line=1
  
             
            if flag_skip_line==0:
                for i in range(len(list_weight_values)):                         
                    print list_values_days[i],timedelta(list_values_days[i])+arbitrary_initial_date,list_weight_values[i]  


                   
                    weight=list_weight_values[i]  
                    on_day=timedelta(list_values_days[i])+arbitrary_initial_date                                      
                    
                    db.execute ("""
                        INSERT INTO weigh_in_history (ck_id, weight, on_day, id, activity_flag)
                        VALUES (%s, %s, %s, %s,%s)
                        """, str(ck_id), str(weight),str(on_day),str(id), str(activity_flag))

                delta=(len(row)-1)*7
                print delta,timedelta(delta)+arbitrary_initial_date ,240.  # fixed final value
                weight=240.
                on_day=timedelta(delta)+arbitrary_initial_date                                              
                
                db.execute ("""
                        INSERT INTO weigh_in_history (ck_id, weight, on_day, id, activity_flag)
                        VALUES (%s, %s, %s, %s,%s)
                        """, str(ck_id), str(weight),str(on_day),str(id), str(activity_flag))





                #raw_input()
            else:
                print "bad data!"
        cont+=1









    #query="""describe weigh_in_history""" 
   









	   
     

##############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
       
       

        main(csv_file)
    else:
        print "usage: python  whatever.py   path/csv_file_all_MT_series.csv "
 
     
