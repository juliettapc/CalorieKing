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


    
    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 





    query="""select * from users""" 

   
    result1 = db.query(query)  # is a list of dict.

    
    num_user=0
    for r1 in result1:   #loop over users
        
        ## r1 is a dict.:  {'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6', 'age': 52L, 'state': u'', 'height': 64L, 'join_date': datetime.datetime(2009, 11, 27, 10, 41, 5), 'is_staff': u'public', 'most_recent_weight': 142.0, 'initial_weight': 144.0, 'id': 1L}

        ck_id=r1['ck_id']
        id=r1['id']
        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       
        # result2 is a list of dict.: [{'id': 163978L, 'activity_flag': u'WI', 'weight': 144.0, 'on_day': datetime.datetime(2009, 11, 27, 0, 0), 'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6'}, {'id': 163979L, 'activity_flag': u'WI', 'weight': 143.09999999999999, 'on_day': datetime.datetime(2009, 12, 15, 0, 0), 'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6'}, ...,]
       

        cont=0   #number of users
        if len(result2)>=100: # only consider users with at least 100 weigh-ins                       
            num_user=num_user+1
            print num_user

         
            initial_BMI=float(r1['initial_weight'])*703.0/(float(r1['height'])*float(r1['height']))


            if (initial_BMI >30): #obese
                name1="temporal_series/most_weigh_ins/single_file_weigh_in_time_serie_days_obese.dat" 
                
            elif (initial_BMI >25) and(initial_BMI <30): #overweighted
                name1="temporal_series/most_weigh_ins/single_file_weigh_in_time_serie_days_overweighted.dat"
                                                            
            elif (initial_BMI  < 25) and (initial_BMI  > 18.5): #normal   
                name1="temporal_series/most_weigh_ins/single_file_weigh_in_time_serie_days_normal.dat" 
            
            elif (initial_BMI < 18.5): #underweighted group 
                name1="temporal_series/most_weigh_ins/single_file_weigh_in_time_serie_days_underweighted.dat" 





            file = open(name1,'at')
            contador=0 # number of weigh-ins
            for row in result2:   

                if contador==0 :
                    first_day=row['on_day']


               
                if (float(row['weight'])>10.0):  # to eliminate some error in the data
                    print >> file, contador,row['weight'],float(row['weight'])*703.0/(float(r1['height'])*float(r1['height'])),row['on_day']-first_day                        
                    contador=contador+1

                print >> file,"\n"    #to separate users                      
            file.close()
                






# one file per each user's weight time serie:

            name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(num_user)+".dat"
            file = open(name,'wt')
            

            contador2=0
            for row in result2: 

                if contador2==0 :
                    first_day=row['on_day']
                

               
                if (float(row['weight'])>10.0): # to eliminate some error data   
                   
                    print >> file, contador2,row['weight'],float(row['weight'])*703.0/(float(r1['height'])*float(r1['height'])),row['on_day']-first_day 


                    contador2=contador2+1
                    cont=cont+1                                
         
            file.close()






#########################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

