
#! /usr/bin/env python

"""
Created by Julia Poncela of October 2011

Given a file for a non-stationary time serie, it calculates the optimum points to cut it, that mark different trends.

More info: It follows the method proposed by Fukuda, Stanley and Amaral PRL 69, 2004.



"""


import sys
import os
from datetime import *
import math
import numpy as np
from scipy import stats
from database import *   #codigo para manejar bases de datos


def main ():


    top=50   #max: 8921  with filters  
  


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    db.execute ("DROP TABLE IF EXISTS gaps_by_frequency")  #i remove the (old) table 

      
    db.execute ("""                      
       CREATE TABLE gaps_by_frequency
       (
         file_index     INT,
         ck_id          CHAR (20),
         start_date     INT,
         end_date       INT,
         start_day      INT,
         end_day        INT,
         days_gap       INT,        
         zscore_gap     FLOAT
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
    




    list_all_average_frequencies=[]
    histogram_all_freq_no_averaged=[0]*1000
    num_events_all_freq_no_averaged=0.

  
    for index_file in range(top):
        index_file+=1

        list_average_frequencies_one_user=[]
        histogram_idiv=[0]*1000
        num_events_indiv=0.


#input file:      
        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50"    
        #file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_filters"
                                                 
    
    
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()


        list_dates=[]
        list_days=[]
        list_frequencies=[]
        cont=0
        for line in list_lines_file:
            if cont>0:   # i skip the first line,cos it doesnt have an associated freq. 
   
                list=line.split(" ")

                ck_id=list[10]
                
                print line
                try:                               
                    list_frequencies.append(float(list[9]))  #frequency                                                    
                    list_days.append(float(list[4]))  #relative day    
                    list_dates.append(list[7])  #dates    
                                  

                except IndexError:                       
                    
                    list_frequencies.append(float(0.0)) #frequency                    
                    list_days.append(float(list[4]))  #day                                      
                    list_dates.append(list[7])  #dates    
                   
            cont+=1

        print list_dates

        print "\n\n"

        list_zscores= stats.zs(list_frequencies)

        for i in range(len(list_zscores)):

            if list_zscores[i] >=3.0:  # statistically significant gap if zs>=3 std
                if list_frequencies[i] >15.:# dont consider it a gap if it is shorter than 2weeks
                    if  i>2:  #or happens for the very second measurement

                        print "on file",index_file,"between days:",list_days[i-1],"-",list_days[i], "there is a gap. freq:", list_frequencies[i],"zscore:",list_zscores[i]

                        time_gap=list_days[i]-list_days[i-1]

                        db.execute ("INSERT INTO gaps_by_frequency (file_index, ck_id, start_date, end_date, start_day, end_day, days_gap, zscore_gap) VALUES ("+str(index_file)+", "+str(ck_id)+","+str(list_dates[i-1])+", "+str(list_dates[i])+","+str(list_days[i-1])+","+str(list_days[i])+","+str(time_gap)+", "+str(list_zscores[i])+" ")



            print "\n","on file",index_file,"mean freq:",np.asanyarray(list_frequencies).mean(axis=0),"std:",np.asanyarray(list_frequencies).std(axis=0, ddof=0)







 
        raw_input()


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
