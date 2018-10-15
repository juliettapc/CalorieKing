#! /usr/bin/env python

"""
Created by Julia Poncela of March 2011

It extractes the weight time series for all users (one file per each), plus
a block file for all obese, all overweighted etc.
It needs a pre-existing folder temporal_series/ to storage the files.


It doesnt take any arguments.

"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import *
import math
from pylab import *
import numpy



def main ():



   

    min_wi=10  #Filter1:  min number of weigh ins >=
    min_frequency=1./30.  #Filter2:  min frequency
    min_timespan=10       # Filter3: min lenght of the serie


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 





    query="""select * from users""" 

   
    result1 = db.query(query)  # is a list of dict.



    

    num_user=0
    for r1 in result1:   #loop over users to get their number_of_weigh-ins

        
        ## r1 is a dict.:  {'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6', 'age': 52L, 'state': u'', 'height': 64L, 'join_date': datetime.datetime(2009, 11, 27, 10, 41, 5), 'is_staff': u'public', 'most_recent_weight': 142.0, 'initial_weight': 144.0, 'id': 1L}

        ck_id=r1['ck_id']
        id=r1['id']
        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       
       

        # result2 is a list of dict.: [{'id': 163978L, 'activity_flag': u'WI', 'weight': 144.0, 'on_day': datetime.datetime(2009, 11, 27, 0, 0), 'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6'}, {'id': 163979L, 'activity_flag': u'WI', 'weight': 143.09999999999999, 'on_day': datetime.datetime(2009, 12, 15, 0, 0), 'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6'}, ...,]
       
        r1['num_wi']=len(result2)  # i add another key-value to the dict. -->> with this i ALSO modify the list of dict. result!!!

       
        first=result2[0]['on_day']
        last=result2[-1]['on_day']
        time_span_days=(last-first).days+1
        ratio=float(r1['num_wi'])/float(time_span_days)

        if r1['num_wi']>=min_wi   and   ratio >= min_frequency  and   int(time_span_days) >= min_timespan:                 
               
            num_user=num_user+1
            print num_user


            ck_id=r1['ck_id']
            id=r1['id']
            query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
            result2 = db.query(query2)

            initial_weight=float(r1['initial_weight'])



         
           
           # one file per each user's weight time serie:
            name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(num_user)+"_filters.dat" 
            file = open(name,'wt')
            

            contador2=0
            previous= result2[0]['on_day']
            for row in result2: 

               
                if contador2==0 :
                    first_day=row['on_day']
                

                interevent=row['on_day']-previous   # time between events
                if (float(row['weight'])>10.0): # to eliminate some error data   
                   
                    print >> file, contador2,row['weight'],(float(row['weight'])-initial_weight)*100.0/initial_weight,float(row['weight'])*703.0/(float(r1['height'])*float(r1['height'])),row['on_day']-first_day ,row['on_day'],interevent


                    contador2=contador2+1                   
                    previous=row['on_day']       
         
            file.close()






############################################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

