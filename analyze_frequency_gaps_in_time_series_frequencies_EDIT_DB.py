
#! /usr/bin/env python

"""
Created by Julia Poncela on February 2012.

Given a set of time series (in files), calculates the outliers in terms of times between events, to find statistically significant gaps.
Also, adds a new table to the original DB with the gap info.




"""


import sys
import os
from datetime import *
import math
import numpy as np
from scipy import stats
from database import *   #package to handle databases


def main ():


    top=8924    #max: 8924  for the files with filters (>=10 days, >=10weigh-ins >= 1/30 weigh-ins per day).    max:50 for the top50 longest time series (no filter)


    zscore_threshold=1.   # it is a statistically significant gap if zs>= X std

    min_freq=10.    # to consider something a gap

    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    db.execute ("DROP TABLE IF EXISTS gaps_by_frequency")  #i remove the old table 


    #i create a new table in an existing DB  
    db.execute ("""                      
       CREATE TABLE gaps_by_frequency
       (
         file_index     INT,
         ck_id          CHAR (36),           
         index_start_day      INT,
         index_end_day        INT,
         start_day      INT,
         end_day        INT,
         days_gap       INT,        
         zscore_gap     FLOAT,
         average_freq     FLOAT
       
        
       )
     """) # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 

    #query="""describe gaps_by_frequency""" 
    #db.execute ("DROP TABLE IF EXISTS animal")
    # query="""show tables""" 





    query="""select * from gaps_by_frequency""" 
   

   
   # db.execute ("INSERT INTO gaps_by_frequency (file_index, ck_id, start_date, end_date, start_day, end_day, days_gap, std_freq, zscore_gap) VALUES (1, 'reptile',7, 4,1,20,18, 2.,3.) ")

   # db.execute ("INSERT INTO gaps_by_frequency (file_index, ck_id, start_date, end_date, start_day, end_day, days_gap, std_freq, zscore_gap) VALUES ("+str(1)+", 'reptile',"+str(1)+", "+str(1)+","+str(1)+","+str(1)+","+str(1)+", "+str(1.)+","+str(1.)+") ")




    #query="""show tables""" 
   

 #   query="""select * from gaps_by_frequency""" 
  #  result1 = db.query(query)  # is a list of dict.
   # for r1 in result1:
    #    print r1
    




  
    for index_file in range(top):

       
        index_file+=1
        print "\n\n",index_file
       


#input file:      
        #file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50"    
        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_filters"
                                                 
    
# OJO!!!!!!!! EN ESTE ARCHIVO, EL DIA (RELATIVO AL PRIMERO) ES LA COLUNMA 4, NO LA 0 !!!!!!!!!!

    
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()


        list_dates=[]
        list_days=[]
        list_frequencies=[]
        cont=0
        for line in list_lines_file:
            if cont>0:   # i skip the first line,cos it doesnt have an associated freq. 
   
                list=line.split(" ")

                ck_id=list[8].strip("\n")
                               
                try:                               
                    list_frequencies.append(float(list[7]))  #frequency                                                    
                    list_days.append(float(list[4]))  #relative day  to the sign-up  date
                    list_dates.append(list[5])  #dates    
                                  

                except IndexError:                       
                    
                    list_frequencies.append(float(0.0)) #frequency                    
                    list_days.append(float(list[4]))  #day                                      
                    list_dates.append(list[5])  #dates    
                   
            cont+=1

        

        average_freq= np.mean(list_frequencies)

        list_zscores= stats.zs(list_frequencies)




# OJO!!!!!!!!! list_zscores[0] (o tb list_frequencies[0]) corresponde a la diff entre la primera y la segunda entrada de list_days, por lo que en realindad
#hay un desfase de una unidad entre los indices de las dos listas
        num_gaps=0
        for i in range(len(list_zscores)):

            if list_zscores[i] >=zscore_threshold:  # it is a statistically significant gap if zs>= zscore_threshold
                if list_frequencies[i] > min_freq:# dont consider it a gap if it is shorter than  x days
                    if  i>=1:  #because of the python thing about list[-1]=last_element_of_list)

                       
                        print "    between days:",list_days[i-1],"-",list_days[i], "there is a gap. freq:", list_frequencies[i],"zscore:",list_zscores[i],"average freq: ",average_freq, ck_id,"on file",index_file

                        time_gap=list_days[i]-list_days[i-1]
                      




                       # db.execute ("""
                       # INSERT INTO gaps_by_frequency (file_index, ck_id, start_date, end_date, start_day, end_day, days_gap, zscore_gap)
                        #VALUES (%s, %s, %s,%s, %s, %s,%s, %s,%s, %s)
                        #""", str(index_file), str(ck_id),str(list_dates[i-1]), str(list_dates[i]),str(list_days[i-1]),str(list_days[i]),str(time_gap), str(list_zscores[i]), str(np.asanyarray(list_frequencies).mean(axis=0)), str(np.asanyarray(list_frequencies).std(axis=0, ddof=0)))    NO FUNCIONA!!
                        
                       
                        db.execute ("""
                        INSERT INTO gaps_by_frequency (file_index, ck_id,  start_day, end_day, index_start_day, index_end_day, days_gap, zscore_gap, average_freq)
                        VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)
                        """, str(index_file), str(ck_id),str(list_days[i-1]),str(list_days[i]),i,i+1,str(time_gap), str(list_zscores[i]), str(average_freq))

# note: to get the index (of the point) for the days, it is i+1, because i corresponds to the serie of freq. (also, remember that it starts ato 0 index)




                                 
                        num_gaps+=1



                        if ck_id== "34214d9b-3fae-43d5-a961-bf7a94e22a3c" :
                            for ii in range(len(list_zscores)):
                                print list_days[ii],list_frequencies[ii],list_zscores[ii]
                
                            raw_input()

                        print  str(ck_id),str(list_days[i-1]),str(list_days[i]),i,i+1,str(time_gap), str(list_zscores[i]), str(average_freq)



                       # raw_input()

        print "on file",index_file,"mean freq:",np.asanyarray(list_frequencies).mean(axis=0),"std:",np.asanyarray(list_frequencies).std(axis=0, ddof=0)

       

       # if num_gaps>=8:  #only one time series (file_index=2040) have more than 8  zs=3 gaps
        #    print index_file, "file has",num_gaps,"or more gaps! in ", len(list_days),"measurements"
         #   raw_input()

       

 
       


##################################
       
def zscore(a, axis=0, ddof=0):
	    """
	    Calculates the z score of each value in the sample, relative to the sample
	    mean and standard deviation. 
	 
	    Parameters
	    ----------
	    a: array_like
	       An array like object containing the sample data
	    axis: int or None, optional
	         If axis is equal to None, the array is first ravel'd. If axis is an
	         integer, this is the axis over which to operate. Defaults to 0.
	   

            ddof : int, optional
                 Degrees of freedom correction in the calculation 
                 of the standard deviation. Default is 0.

	    Returns
	    -------
	    zscore: array_like
	        the z-scores, standardized by mean and standard deviation of input
	        array
	
	    Notes
	    -----
	    This function does not convert array classes, and works also with
	    matrices and masked arrays.
	
	    """
	    a = np.asanyarray(a)
	    mns = a.mean(axis=axis)
	    sstd = a.std(axis=axis, ddof=ddof)
	    if axis and mns.ndim < a.ndim:
	        return ((a - np.expand_dims(mns, axis=axis) /
	                 np.expand_dims(sstd,axis=axis)))
	    else:
	        return (a - mns) / sstd
	   


#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
