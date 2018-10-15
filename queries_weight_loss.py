#! /usr/bin/env python

"""
Created by Julia Poncela of March 2011


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

   
    result1 = db.query(query) 

    
    num_user=0
    for r1 in result1:   #loop over users
        
        ck_id=r1['ck_id']
        id=r1['id']
        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       

        cont=0
        if len(result2)>=5: # only consider users with at least 5 weigh-ins                       
            num_user=num_user+1
            print num_user

         


            if len(result2)>=20:  # one sigle file per BMI category with all the user time series
               
                initial_BMI=float(r1['initial_weight'])*703.0/(float(r1['height'])*float(r1['height']))


                if (initial_BMI >30): #obese
                    name1="temporal_series/single_file_weigh_in_time_serie_obese.dat" 

                elif (initial_BMI >25) and(initial_BMI <30): #overweighted
                    name1="temporal_series/single_file_weigh_in_time_serie_overweighted.dat"
                                                            
                elif (initial_BMI  < 25) and (initial_BMI  > 18.5): #normal   
                    name1="temporal_series/single_file_weigh_in_time_serie_normal.dat" 
            
                elif (initial_BMI < 18.5): #underweighted group 
                    name1="temporal_series/single_file_weigh_in_time_serie_underweighted.dat" 


                contador=0
                for row in result2:                 
                    file = open(name1,'at')
                    if (float(row['weight'])>10.0):  # to eliminate some error in the data
                         print >> file, contador,row['weight'],float(row['weight'])*703.0/(float(r1['height'])*float(r1['height'])),row['on_day']                        
                        contador=contador+1

                print >> file,"\n"    #to separate users                      
                file.close()
                








# one file per each user's weight time serie:

            name="temporal_series/weigh_in_time_serie"+str(num_user)+".dat"
            file = open(name,'wt')
            file.close()

            for row in result2:                 
                file = open(name,'at')
                if (float(row['weight'])>10.0):  # to eliminate some error data
                     if (float(row['weight'])>0.0):
                         #print >> file, cont,row['weight'],float(row['weight'])*703.0/(float(r1['height'])*float(r1['height'])),row['on_day']  
                         print >> file,row['on_day'],",",row['weight'],",",float(row['weight'])*703.0/(float(r1['height'])*float(r1['height']))                  


                         cont=cont+1                                
         
            file.close()






#########################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

