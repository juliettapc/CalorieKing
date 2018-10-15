#! /usr/bin/env python

"""
Created by Julia Poncela of February 2011

Calculates the distribution of: number of posters, number of posts, time intervals between posts, total time elapsed from first to last post in each thread, and also cumulative distributions for times.


It doesnt take arguments.

"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import *
import math
from pylab import *
import numpy



def main ():


    
    database = "calorie_king_social_networking"
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"


    db= Connection(server, database, user, passwd)  #abro la base de datos






    query="""select  distinct thread_id from forum_posts""" # there are 10511 of them: select count( distinct thread_id) from forum_posts

   
   
    result1 = db.query(query) #[{'thread_id':  },{'thread_id':  },{... },...]


    num_threads=len(result1)
    distr_posts=[0.0]*num_threads
    distr_posters=[0.0]*num_threads
    norm_posts=0.0
    norm_posters=0.0


   


    last_first_average=timedelta(0) #because this variable is going to store time!!   
    list_last_first=[]
    list_delta_times_posts=[]


    count=0

    num_eff_threads=0 # number of threads with more than one post
    norm_delta_times=0
    max_num_posts=0
    max_num_posters=0

    for r1 in result1:  # loop over different threads
       

        if count <= 100000:   # DELETE THIS CONDITION IN THE FINAL VERSION!!!!!!!!

            thread=r1['thread_id']
            
            print count
            count=count+1

       
       
            result3=db.query("select ck_id,at_time  from forum_posts  where (thread_id ='"+str(thread)+"') order by at_time asc")  #[{'ck_id': ,'at_time':  },{'ck_id': ,'at_time':   },{... },...]

            num_posts=len(result3)

            
            if num_posts>max_num_posts:
                max_num_posts=num_posts




            if num_posts >1:  # exclude the threads with only one post
            
                num_eff_threads=num_eff_threads+1



                result2=db.query("select distinct ck_id  from forum_posts  where (thread_id ='"+str(thread)+"')") #[{'ck_id':  },{'ck_id':  } ,{}}

                num_posters=len(result2)
            

                if num_posters>max_num_posters:
                    max_num_posters=num_posters



                distr_posters[num_posters]=distr_posters[num_posters]+1        
                norm_posters=norm_posters+1
 

               
        
                last_first=result3[-1]['at_time']-result3[0]['at_time']# type: timedelta
           


               
                list_last_first.append(last_first)
                last_first_average=last_first_average+last_first              
               
            

                distr_posts[num_posts]=distr_posts[num_posts]+1
                norm_posts=norm_posts+1



               

                for i in range(len(result3)): # create a list of delta_times between 
                    if i>0:             # sucesive posts (cummulative for all threads)
                        
                        time_elapsed=(result3[i]['at_time']-result3[i-1]['at_time']).seconds + (result3[i]['at_time']-result3[i-1]['at_time']).days*60*60*24
                        list_delta_times_posts.append(time_elapsed) # list of seconds (integers)
                        norm_delta_times=norm_delta_times+1
       

   


    # end loop over threads


    cum_distr_posts=[0.0]*num_threads    # cumulative distribution <=
    cum_distr_posters=[0.0]*num_threads
    

   

#larger of equal to
    for number in range(1,max_num_posts+1):
        for index in range(number, max_num_posts+1):            
            cum_distr_posts[number]=cum_distr_posts[number]+distr_posts[index]
            
            #print "number:", number,"index:", index, "cum:",cum_distr_posts[number],distr_posts[index]
            #raw_input()

    for number in range(1,max_num_posters+1):
        for index in range(number, max_num_posters+1):             
            cum_distr_posters[number]=cum_distr_posters[number]+distr_posters[index]
            
    


       
   


#average and standard deviation of time intervals between two posts
  
    average_delta_times=0.0
    for i in list_delta_times_posts:
        average_delta_times=average_delta_times+i
       
    average_delta_times=average_delta_times/norm_delta_times


    deviation_delta=0.0 
    for i in list_delta_times_posts:        #list of integers                         
        deviation_delta=deviation_delta +(i - average_delta_times)**2
       
        
    deviation_delta=deviation_delta/norm_delta_times
    deviation_delta=sqrt(deviation_delta)
    deviation_delta_time=timedelta(seconds=deviation_delta) #transform back to timedelta type
    

    average_delta_times=timedelta(seconds=average_delta_times) #transform to timedelta type




   
#average time of last-to-first-post
    last_first_average=last_first_average/num_eff_threads

#standard deviation of the (last-first) times:
#I NEED TO TRANSFORM EVERYTHING TO SECONDS BY HAND, BECAUSE MULTIPLY TO TIMEDELTA OBJECTS IS NOT SUPPORTED!!
    
    aux2_seg=float(last_first_average.seconds) + float(last_first_average.days*60*60*24)   


    deviation=0.0 
    for i in list_last_first:       
        aux1_seg=float(i.seconds) + float(i.days*60*60*24)#were integers                      
        deviation=deviation +(aux1_seg - aux2_seg)**2
       
        
    deviation=deviation/num_eff_threads
    deviation=sqrt(deviation)
    deviation_time=timedelta(seconds=deviation) #transform back to timedelta type
    



   

# print out the average and standard deviation of last-first times & consecutive-post times:
    file2 = open("Last_First_average_deviation_CK_forums.dat",'wt')   
    print >> file2, "average_last-first:",last_first_average,"(",deviation_time,  "seg.)"
    print >> file2,"average_delta_time:",average_delta_times,"(", deviation_delta_time, "seg.)"
    file2.close()








# print out the distribution of # post and posters:
    file1 = open("Post-poster_distributions_CK_forums.dat",'wt')
    for i in range (num_threads):
        print >> file1, i,"\t", distr_posts[i]/norm_posts,"\t", distr_posters[i]/norm_posters,"\t", cum_distr_posts[i]/norm_posts,"\t", cum_distr_posters[i]/norm_posters
        
    file1.close()










#bins for the delta_times between final and initial posts in a given thread:




    list_last_first_seconds=[] #list_last_first was a list of data of type: 'datetime.timedelta'

    for i in list_last_first:
        list_last_first_seconds.append(i.seconds + i.days*60*60*24)

   
  


    max_boundary= max(list_last_first_seconds)
    min_boundary= 1   # measured in seconds

  
#bins according to the natural way of measuring time  (in seconds):



    bin1=timedelta(minutes=1).seconds   
    bin2=timedelta(hours=1).seconds
    bin3=timedelta(days=1).days*60*60*24
    bin4=timedelta(days=1).days*60*60*24*2    
    bin5=timedelta(weeks=1).days*60*60*24
    bin6=timedelta(weeks=1).days*60*60*24*4
    bin7=timedelta(weeks=1).days*60*60*24*52

   
    Nbins=7  # i decide this number
    boundaries=[]
   

    
   
      
    boundaries.append(bin1)
    boundaries.append(bin2)   
    boundaries.append(bin3)
    boundaries.append(bin4)
    boundaries.append(bin5)
    boundaries.append(bin6)
    boundaries.append(bin7)




       

    print boundaries

    number_events_box=[0]*(Nbins+1)  # histogram
    

    for i in list_last_first_seconds:   # list of integers    
        b_index=0         
        for b in boundaries:  
            if i < b:                
                number_events_box[b_index]=number_events_box[b_index]+1              
                b_index=b_index+1               
                break
            else:
                b_index=b_index+1
           
   

    



     # print out the distribution of final-initial post times:
    file4 = open("Final_initial_time_boxes_CK_forums_natural.dat",'wt')
    for i in range(len(number_events_box)):
        print >> file4 ,i, number_events_box[i]
    print  >> file4 ,"max & min for last-first:",max_boundary, min_boundary, 
       
    file4.close()

   



    
# bins for the delta_times between consecutive post (cummulative for all threads)

    
#bins according to the natural way of measuring time  (in seconds):
############################################################  




    bin1=timedelta(minutes=1).seconds   
    bin2=timedelta(hours=1).seconds
    bin3=timedelta(days=1).days*60*60*24
    bin4=timedelta(days=1).days*60*60*24*2    
    bin5=timedelta(weeks=1).days*60*60*24
    bin6=timedelta(weeks=1).days*60*60*24*4
    bin7=timedelta(weeks=1).days*60*60*24*52
    



    Nbins=7  # i decide this number
    boundaries=[]
   

    
   
      
    boundaries.append(bin1)
    boundaries.append(bin2)   
    boundaries.append(bin3)
    boundaries.append(bin4)
    boundaries.append(bin5)
    boundaries.append(bin6)
    boundaries.append(bin7)


    print boundaries    

    number_events_box=[0]*(Nbins+1)  # histogram
    


    print boundaries
    
    for i in list_delta_times_posts:       
        b_index=0  
        for b in boundaries:     
           
            if i < b: 
                number_events_box[b_index]=number_events_box[b_index]+1             
                b_index=b_index+1
                break
            else:
                b_index=b_index+1

    



   
     # print out the distribution of final-initial post times:
    file5 = open("Delta_times_between_posts_boxes_CK_forums_natural.dat",'wt')
    for i in range(len(number_events_box)):
        print >> file5 ,i, number_events_box[i]
    print  >> file5 ,"max & min for delta_times:",max_boundary, min_boundary
      
    file5.close()

   





#########################
      
        



if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 
