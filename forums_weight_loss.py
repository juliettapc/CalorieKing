#! /usr/bin/env python

"""
Created by Julia Poncela of March 2011

It calculates the average weight changes for forum threads, as a function of its (arbitrary) index, the activity density and the lifespan of the threads.

It doesnt take any arguments.

"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import *
import math
from pylab import *
import numpy
from scipy import stats



def main ():



 
    database = "calorie_king_social_networking_2010"  #the old data was:  calorie_king_social_networking
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"


    db= Connection(server, database, user, passwd)  #abro la base de datos



    directory="5_points_network_2010/data/"  
    filename="Averge_weight_loss_forums_.dat" 
    file = open(directory+filename,'wt')
    file.close()



    query="""select  distinct thread_id from forum_posts"""   
    result1 = db.query(query) #list of dict: [{'thread_id':  },{'thread_id':  },{... },...]

    total_list_weight_changes=[]
    total_list_BMI_changes=[]
    total_list_weight_percentage_changes=[]
    list_life_span=[]
    list_dens_actividad=[]


    count=0
    for r1 in result1:  # loop over different threads 

        if count <=  9425:   # DELETE THIS CONDITION IN THE FINAL VERSION!!!!!!!!

            list_weight_changes_thead=[]
            list_BMI_changes_thead=[]
            list_weight_percentage_changes_thead=[]

            thread=r1['thread_id']
                       


            result2=db.query("select ck_id,at_time  from forum_posts  where (thread_id ='"+str(thread)+"') order by at_time asc")  #[{'ck_id': },{'ck_id':  },{... },...]
            num_posts=len(result2)


            last_first=result2[-1]['at_time']-result2[0]['at_time']# type: timedelta                    
            life_span=(last_first.seconds)/(60.0*60.0*24.0)+float(last_first.days)   # of the thread (in days)
           
           

           
            result3=db.query("select distinct ck_id  from forum_posts  where (thread_id ='"+str(thread)+"')") #[{'ck_id':  },{'ck_id':  } ,{}}
            num_posters=len(result3)


            if len(result3) >3:  #only consider threads with more than 3 distinct users!

                print "\n",count
                count=count+1

                for r3 in result3:  # loop over all users of a given thread
                    user=r3['ck_id']


                    result4=db.query("select ck_id, initial_weight, most_recent_weight, height  from users  where (ck_id ='"+str(user)+"')") 


                    if len(result4)>0:# this user HAS a weigh-in history, not GHOST user!!!

                        weight_change=float(result4[0]['most_recent_weight'])-float(result4[0]['initial_weight'])
                        BMI_change=weight_change*703.0/float(result4[0]['height']*result4[0]['height'])

                        weight_percentage_change=weight_change*100.0/float(result4[0]['initial_weight'])

                        


                        list_weight_changes_thead.append(weight_change)
                        list_BMI_changes_thead.append(BMI_change)
                        list_weight_percentage_changes_thead.append(weight_percentage_change)



                # end loop over all users of a given thread

                if len(list_weight_changes_thead)>0:
                    
                    average_weight=numpy.mean(list_weight_changes_thead)
                    std_deviation_weight=numpy.std(list_weight_changes_thead)
                #print "tread:",thread,"#posts:",num_posts,"#posters:",num_posters,"<weight_ch>",average,"+/-",std_deviation
                
                    average_BMI=numpy.mean(list_BMI_changes_thead)
                    std_deviation_BMI=numpy.std(list_BMI_changes_thead)


                    
                    average_weight_percentage=numpy.mean(list_weight_percentage_changes_thead)
                    std_deviation_weight_percentage=numpy.std(list_weight_percentage_changes_thead)                                            


                    dens_activity_posts=num_posts/(float(last_first.seconds) + float(last_first.days*60*60*24))#posts per second
                    dens_activity_posters=num_posters/(float(last_first.seconds) + float(last_first.days*60*60*24)) #posters per second

                    dens_activity_posts=dens_activity_posts*60*60*24 #posts per day 
                    dens_activity_posters=dens_activity_posters*60*60*24 #posts per day 




                    file = open(directory+filename,'at')
                    print >> file,count,average_weight,std_deviation_weight,average_BMI,std_deviation_BMI,average_weight_percentage,std_deviation_weight_percentage,num_posts,num_posters,life_span,dens_activity_posts,dens_activity_posters
                    file.close()

                    total_list_weight_changes.append(average_weight)
                    total_list_BMI_changes.append(average_BMI)
                    total_list_weight_percentage_changes.append(average_weight_percentage)

                    list_life_span.append(life_span)
                    list_dens_actividad.append(dens_activity_posters)


    # end loop over threads



    print "total average weight change:",numpy.mean(total_list_weight_changes),"+/-:",numpy.std(total_list_weight_changes)
    print "total average BMI change:",numpy.mean(total_list_BMI_changes),"+/-:",numpy.std(total_list_BMI_changes)

    print "total average weight change:",numpy.mean(total_list_weight_percentage_changes),"+/-:",numpy.std(total_list_weight_percentage_changes)







    # shapiro-wilks test for normal distributions:
    print "\n\nShapiro-Wilks for weight changes of the threads:"
    print stats.shapiro(total_list_weight_changes) # it returns  a tupla of floats, W : The test statistic, and p-value for the hypothesis test.
#IT IS NORMAL DISTRIBUTED DATA IF w CLOSE TO 1 AND p<0.05



    hist, bin_edges= numpy.histogram(total_list_weight_changes, bins=20)
    

  #  print list_weight_changes_thead

    print hist, bin_edges



    origin=float(bin_edges[0])
    file = open(directory+"histogram_weight_change_threads_",'wt')
    for b in range(len(bin_edges)-1):        
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0, hist[b]
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()










    print "\n\nShapiro-Wilks for lifespan of the threads but only for >20:"


    list_life_span20=[n for n in list_life_span if (n>20)]

    print stats.shapiro(list_life_span20) 

    hist, bin_edges= numpy.histogram(list_life_span20, bins=60)
    
    #print list_life_span
    print hist, bin_edges



    origin=float(bin_edges[0])
    file = open(directory+"histogram_life_span_threads20",'wt')
    for b in range(len(bin_edges)-1):        
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0, hist[b]
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()








    print "\n\nShapiro-Wilks for lifespan of the threads:"
    print stats.shapiro(list_life_span) 

    hist, bin_edges= numpy.histogram(list_life_span, bins=60)
    
    #print list_life_span
    print hist, bin_edges



    origin=float(bin_edges[0])
    file = open(directory+"histogram_life_span_threads_",'wt')
    for b in range(len(bin_edges)-1):        
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0, hist[b]
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()







    print "\n\nShapiro-Wilks for dens. of act. of the threads:"
    print stats.shapiro(list_dens_actividad) 


    hist, bin_edges= numpy.histogram(list_dens_actividad, bins=60)
    
   # print list_life_span
    print hist, bin_edges



    origin=float(bin_edges[0])
    file = open(directory+"histogram_dens_act_threads_",'wt')
    for b in range(len(bin_edges)-1):        
        print >> file,origin +(bin_edges[b+1]-bin_edges[b])/2.0, hist[b]
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()









    print "\n\nShapiro-Wilks for dens. of act. of the threads ( >20 & <100):"

    list_dens_actividad20=[n for n in list_dens_actividad if ((n>=20) and (n<=100)) ]

    print stats.shapiro(list_dens_actividad20) 


    hist, bin_edges= numpy.histogram(list_dens_actividad20, bins=60)
    
   # print list_life_span
    print hist, bin_edges



    origin=float(bin_edges[0])
    file = open(directory+"histogram_dens_act_threads20",'wt')
    for b in range(len(bin_edges)-1):        
        print >> file,origin +(bin_edges[b+1]-bin_edges[b])/2.0, hist[b]
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()


  
  

 


    print "\n\nKolmogorov-Smirnov test for (normal) weight changes of the threads:"
    print stats.kstest(total_list_weight_changes, 'norm') # it returns  a tupla of floats, D : The test statistic, and p-value for the hypothesis test.
#IT IS NORMAL DISTRIBUTED DATA IF D CLOSE TO 1 AND p<0.05


    print "\n\nKolmogorov-Smirnov test for (power-law) dens. activity of threads (>20 & <100):"
    print stats.kstest(list_dens_actividad20, 'powerlaw') # it returns  a tupla of floats, D : The test statistic, and p-value for the hypothesis test.
#IT IS NORMAL DISTRIBUTED DATA IF D CLOSE TO 1 AND p<0.05


#########################
      
        



if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass
