
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
import numpy
from scipy import stats
from database import *   #package to handle databases




def main ():



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    
    db= Connection(server, database, user, passwd) 


    db.execute ("DROP TABLE IF EXISTS frequency_cuts")  #i remove the old table 


    #i create a new table in an existin DB  
    db.execute ("""                      
       CREATE TABLE frequency_cuts
       (
         file_index     INT,
         ck_id          CHAR (200),            
         start_day      INT,
         end_day        INT,
         mean_freq      FLOAT,        
         std_freq       FLOAT,
         tot_num_cuts   INT
       
        
       )
     """) # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 


 


    significance_threshold=0.95
    min_lenght=10  # to cut the series (in terms of num of points)

    top=8924      #max: 8924  with filters, 50 for the top50 longest series


    freq_threshold=0.2   # meaningful threshold for   (freq1-freq2)/Average(freq1,freq2)


    list_all_average_frequencies=[]   
    num_events_all_freq_no_averaged=0.



    
    file22=open("temporal_series/most_weigh_ins/number_segments_acording_to_frequencies.dat",'wt')
  


  
    for index_file in range(top):
        index_file+=1
       

        list_average_frequencies_one_user=[]      
        num_events_indiv=0.

        file33=open("temporal_series/most_weigh_ins/average_frequencies_segments_"+str(index_file)+".dat",'wt')




#input file:
        #file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50"    
        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_filters"
                                                 
    

       
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()



      
        file2=open(file_name+"_frequencies_t_points_segments"+str(min_lenght)+"_threshold.dat",'wt')



       
        list_vectors=[]
        list_series=[]
        list_values_for_average=[]  # to do the average if the whole serie is just one piece

        cont=0
        for line in list_lines_file:
            if cont>0:   # i skip the first line,cos it doesnt have an associated freq. 
   
                list=line.split(" ")
                
                ck_id=list[8]
                
                vector=[]
               
               # try:                               
              
                vector.append(float(list[4]))  #day
                vector.append(float(list[7]))  #frequency
                vector.append(float(list[2]))  #%weight change
                
                list_values_for_average.append(float(list[7]))
                
                index=int(round(float(list[7])))         #for the histogram of frequencies (not averaged)               
                num_events_all_freq_no_averaged+=1.
                                
                num_events_indiv+=1.
                    
               
                

                vector.append(0.0)  # here it will go the value for t
                list_vectors.append(vector)
            cont+=1
        end=list_vectors[-1][0] #last day

        num_lines=len(list_vectors)
                
        list_series.append(list_vectors)
        
        
        list_cut_times=[]

        for list_evolution in list_series:  # i analyze the current time serie (or fragment of it)
            

            num_points=len(list_evolution)
                

            if num_points>=min_lenght:  # if the serie is too short, i wont cut it any further

                t_max=0.0          
       
                for index in range(num_points):
           
                    if index>=1  and index < num_points-1:  # to cut the serie, at least need one point in each list

                        list1=[]  #first segment of the list
                        list2=[]  #second segment of the list
                   
                
                        for x1 in range(num_points):
                                              
                            if x1 <= index:
                                list1.append(list_evolution[x1][1]) #only the list of values (not times!)                           
                            else:
                                list2.append(list_evolution[x1][1])
                            

                   
                        mu1=numpy.mean(list1)
                        mu2=numpy.mean(list2)
                        
                        sd1=numpy.std(list1)
                        sd2=numpy.std(list2)
                        
                        N1=float(len(list1))
                        N2=float(len(list2))
                        
                        S_D=math.sqrt(((N1-1)*sd1*sd1 + (N2-1)*sd2*sd2)/(N1+N2-2))*math.sqrt(1.0/N1 + 1.0/N2)
                        t=math.fabs((mu1-mu2)/S_D)
                        


                                         
                        list_evolution[index][3]=t
                       
                       
                                                                 
                        if t >= t_max:
                            t_max=t
                            index_max_t=index
                            time_max=list_evolution[index][0]
                            
                            
                            segment1=[]
                            segment2=[]    
                            for x2 in range(num_points):   # i save the definitive two segments
                                              
                                if x2 <= index_max_t:                           
                                    segment1.append(list_evolution[x2])   #list of events (time, value,t)
                                else:                           
                                    segment2.append(list_evolution[x2])     

                   
           
           
            
                eta=4.19*math.log(float(num_points))-11.54
                delta=0.40
                nu=float(num_points)-2.0
                
                a=delta*nu  #for the Incomplete beta function
                b=delta
                x=nu/(nu+t_max*t_max)
                I=stats.mstats.betai(a,b,x)
                
                #print eta, nu, a, b,x,I
                try:
                    significance_t_max=math.pow((1.0-I),eta)     #Return x raised to the power y. 
                except ValueError:
                    significance_t_max=0.  #in case I=1.0
        
        
               # print "independently of the signif. and meaninfl",mu1, mu2, abs(mu1-mu2)/((mu1+mu2)/2.)

                if significance_t_max>significance_threshold   and  (abs(mu1-mu2)/((mu1+mu2)/2.) >= freq_threshold  or len(list_cut_times) ==0) :  #so i allow the first cut always
                    if  len(segment1)>min_lenght  and len(segment2)>min_lenght:
                        
                        #print "file:",index_file,"max_t:", t_max, "at time:",list_evolution[index_max_t][0],"significance:",significance_t_max,"     I:",I,"eta:",eta,"nu:",nu,"x:",x,"a:",a,"N:",num_points, "diff freq:",abs(mu1-mu2)/((mu1+mu2)/2.),mu1,mu2
                        
                        list_series.append(segment1)  # next i will analyze the two segments independently
                        list_series.append(segment2)
                        
                        #print "   ",len(segment1), len(segment2)


                        list_cut_times.append(time_max)
                    
                        if round(mu1) not in list_average_frequencies_one_user:   # for the histogram of frequencies
                            list_average_frequencies_one_user.append(round(mu1))
                        if round(mu2) not in list_average_frequencies_one_user:
                            list_average_frequencies_one_user.append(round(mu2))


                else:
                    pass
                  #   print "    file:",index_file,"max_t:", t_max, "at time:",list_evolution[index_max_t][0],"NON significant!:",significance_t_max,"           I:",I,"eta:",eta,"nu:",nu,"x:",x,"a:",a,"N:",num_points
                    





###########################################################
# print out the cut time series to files and add info to DB:
##########################################################
       
        start=0.
        list_cut_times=sorted(list_cut_times)
        #if len(list_cut_times)>0:
        print "\n\nfile:",index_file,"number of cutting points:",len(list_cut_times),"namely:",list_cut_times
           
        cut_inferior=0.0
        
        if len(list_cut_times)!=0:
            for cut in list_cut_times:
               
        
                list_freq_that_segment=[] #list of freq only of that segment
                for vector in list_vectors:
                               
                    if vector[0]>= cut_inferior and vector[0]<= cut:                       
                        print >> file2, vector[0],vector[1],vector[2]
                        list_freq_that_segment.append(vector[1])


                print >> file2, "\n"   # to separate segments of the same time series
                


                print str(index_file),str(start),str(cut),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times)),  len(list_freq_that_segment)
                   
                db.execute ("""
                        INSERT INTO frequency_cuts (file_index, ck_id,  start_day, end_day, mean_freq, std_freq, tot_num_cuts)
                        VALUES (%s, %s, %s,%s, %s, %s, %s)
                """, str(index_file), str(ck_id),str(start),str(cut),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times))  )
                                      





                if cut == list_cut_times[-1]:  #for the last segment   (also if there is just one cut)
                    list_freq_that_segment=[]
                    for vector in list_vectors:
                        if vector[0]> cut:                        
                            print >> file2, vector[0],vector[1],vector[2]
                            list_freq_that_segment.append(vector[1])
                   
               
                   #i write the freq. segments info into the DB

                    print str(index_file),str(cut),str(list_vectors[-1][0]),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times)),  len(list_freq_that_segment)
                   
                    db.execute ("""
                        INSERT INTO frequency_cuts (file_index, ck_id,  start_day, end_day, mean_freq, std_freq, tot_num_cuts)
                        VALUES (%s, %s, %s,%s, %s, %s, %s)
                """, str(index_file), str(ck_id),str(cut),str(list_vectors[-1][0]),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times))  )


                 
                print >> file2, "\n"
                
                cut_inferior=cut
           
                start=cut


        else:      # if only one frequency for the whole serie
            list_freq_that_segment=[] 
           
            for vector in list_vectors:            
                print >> file2, vector[0],vector[1],vector[2]
                list_freq_that_segment.append(vector[1])



            print str(index_file), str(list_vectors[0][0]),str(list_vectors[-1][0]),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times)),  len(list_freq_that_segment)

            db.execute ("""
                        INSERT INTO frequency_cuts (file_index, ck_id,  start_day, end_day, mean_freq, std_freq, tot_num_cuts)
                        VALUES (%s, %s, %s,%s, %s, %s, %s)
                """, str(index_file), str(ck_id),str(list_vectors[0][0]),str(list_vectors[-1][0]),str(numpy.mean(list_freq_that_segment)), str(numpy.std(list_freq_that_segment)) ,str(len(list_cut_times))  )






           #i calculate the average frequency of the whole serie           
            mu=round(numpy.mean(list_values_for_average))
            if mu not in list_average_frequencies_one_user:
                list_average_frequencies_one_user.append(mu)

        file2.close()







        for item in list_average_frequencies_one_user:
            list_all_average_frequencies.append(int(item))

       
 

       



       # i create a file with the number of segments for every time serie (i need that info so i can plot them automatically)

        print >> file22,index_file,len(list_cut_times)+1

        for i in list_average_frequencies_one_user:
            print >> file33, i



    file22.close()
    file33.close()


 #   print list_all_average_frequencies

  


#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
