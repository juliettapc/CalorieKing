#!/usr/bin/env python



"""
Created by Julia Poncela on November 2011.

Given a network and the corresponding csv file for networked & non-networked people,
it caluculates the average pwc  and standard deviation for different sets: all, non-networked, networked, GC, SmallClusters
and also the fraction of people in each set that reaches the -5% wc

"""

import sys
import os
import networkx as nx
import numpy
import csv
from matplotlib import mlab

def main():
   


    input_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_all_users/master_csv.csv"  
    resultado= csv.reader(open(input_name, 'rb'), delimiter=',')#, quotechar='"')

#id,ck_id,join_date,initial_weight,most_recent_weight,height,age,weighins,initial_bmi,final_bmi,percentage_weight_change,weight_change,time_in_system,outcome20,outcome50,p_50,act_20,wi_20,p_friend,R6_overlap,degree,friend_avg,activity
    
   
    

# REMEMBER THAT THE RESULT FROM A CSV.READER ARE TYPE STRINGS!!!!!!

    list_age_all=[]
    list_age_all_2points=[]
    list_age_all_2points_50days=[]
    list_age_all_2points_50days_networked=[]


    list_activity_all=[]
    list_activity_all_2points=[]
    list_activity_all_2points_50days=[]
    list_activity_all_2points_50days_networked=[]


    list_wi_all=[]
    list_wi_all_2points=[]
    list_wi_all_2points_50days=[]
    list_wi_all_2points_50days_networked=[]


    list_ibmi_all=[]
    list_ibmi_all_2points=[]
    list_ibmi_all_2points_50days=[]
    list_ibmi_all_2points_50days_networked=[]


    list_time_all=[]
    list_time_all_2points=[]
    list_time_all_2points_50days=[]
    list_time_all_2points_50days_networked=[]
  
  
    list_pwc_all_2points=[]
    list_pwc_all_2points_50days=[]
    list_pwc_all_2points_50days_networked=[]


    cont_lines=0
    for row in resultado:        
        if cont_lines>0:

            if float(row[9])>15 and float(row[9])<80 :     # filtering out outlayers               
                if float(row[8])>15 and float(row[8])<80 :
                    if float(row[10])>-100 and float(row[10])<100 :  
                        
                        age=float(row[6])
                        if float(row[12])>0:
                            activity=float(row[22])/float(row[12])*7
                        else:
                            activity=float(row[22])

                        wi=float(row[7])
                        ibmi=float(row[8])
                        time=float(row[12])


                        if age >= 18 and age <=100:# filtering out outlayers   
                            list_age_all.append(age)

                        list_activity_all.append(activity)
                        list_wi_all.append(wi)
                        list_ibmi_all.append(ibmi)
                        list_time_all.append(time)
                        
                          

                        if float(row[7])>=2:  #at least two points  
                            pwc= float(row[10])

                            if age >= 18 and age <=100:# filtering out outlayers   
                                list_age_all_2points.append(age)

                            list_activity_all_2points.append(activity)
                            list_wi_all_2points.append(wi)
                            list_ibmi_all_2points.append(ibmi)
                            list_time_all_2points.append(time)
                            list_pwc_all_2points.append(pwc)

                            if float(row[12])>=50:  #at least 50 days      
                            
                                if age >= 18 and age <=100:# filtering out outlayers   
                                    list_age_all_2points_50days.append(age)

                                list_activity_all_2points_50days.append(activity)
                                list_wi_all_2points_50days.append(wi)
                                list_ibmi_all_2points_50days.append(ibmi)
                                list_time_all_2points_50days.append(time)
                                list_pwc_all_2points_50days.append(pwc)
                                
                           
                                if  float(row[20])>=1:  # at least one friend

                                    if age >= 18 and age <=100:# filtering out outlayers   
                                        list_age_all_2points_50days_networked.append(age)

                                    list_activity_all_2points_50days_networked.append(activity)
                                    list_wi_all_2points_50days_networked.append(wi)
                                    list_ibmi_all_2points_50days_networked.append(ibmi)
                                    list_time_all_2points_50days_networked.append(time)
                                    list_pwc_all_2points_50days_networked.append(pwc)
                            
        cont_lines+=1   





    file=open("network_all_users/summary_statistics_different_sets.dat",'wt')

    print >> file, "ALL: # members, Age (mean, SD, 10th p, 90th p, 99th p) || Activity (mean, SD, 10th p, 90th p, 99th p) || #w-ins (mean, SD, 10th p, 90th p, 99th p) || IBMI (mean, SD, 10th p, 90th p, 99th p) || Time (mean, SD, 10th p, 90th p, 99th p) "

    print >> file,  len(list_age_all),numpy.mean(list_age_all),numpy.std(list_age_all),mlab.prctile(list_age_all,p=(10,90,99)),"||",numpy.mean(list_activity_all),numpy.std(list_activity_all),mlab.prctile(list_activity_all,p=(10,90,99)),"||",numpy.mean(list_wi_all),numpy.std(list_wi_all),mlab.prctile(list_wi_all,p=(10,90,99)),"||",numpy.mean(list_ibmi_all),numpy.std(list_ibmi_all),mlab.prctile(list_ibmi_all,p=(10,90,99)),"||",numpy.mean(list_time_all),numpy.std(list_time_all),mlab.prctile(list_time_all,p=(10,90,99)),"\n\n"


    print "max age (All users)",max(list_age_all),"min age (All users)",min(list_age_all)

    print >> file,  "2points: # members, Age (mean, SD, 10th p, 90th p) || Activity (mean, SD, 10th p, 90th p) || #w-ins (mean, SD, 10th p, 90th p) || IBMI (mean, SD, 10th p, 90th p) || Time (mean, SD, 10th p, 90th p) || pwc (mean, SD, 10th p, 90th p)"

    print >> file,  len(list_age_all_2points),numpy.mean(list_age_all_2points),numpy.std(list_age_all_2points),mlab.prctile(list_age_all_2points,p=(10,90,99)),"||",numpy.mean(list_activity_all_2points),numpy.std(list_activity_all_2points),mlab.prctile(list_activity_all_2points,p=(10,90,99)),"||",numpy.mean(list_wi_all_2points),numpy.std(list_wi_all_2points),mlab.prctile(list_wi_all_2points,p=(10,90,99)),"||",numpy.mean(list_ibmi_all_2points),numpy.std(list_ibmi_all_2points),mlab.prctile(list_ibmi_all_2points,p=(10,90,99)),"||",numpy.mean(list_time_all_2points),numpy.std(list_time_all_2points),mlab.prctile(list_time_all_2points,p=(10,90,99)),"||",numpy.mean(list_pwc_all_2points),numpy.std(list_pwc_all_2points),mlab.prctile(list_pwc_all_2points,p=(10,90,99)),"\n\n"





    print >> file,  "2points & 50days: # members, Age (mean, SD, 10th p, 90th p) || Activity (mean, SD, 10th p, 90th p) || #w-ins (mean, SD, 10th p, 90th p) || IBMI (mean, SD, 10th p, 90th p) || Time (mean, SD, 10th p, 90th p) || pwc (mean, SD, 10th p, 90th p)"

    print >> file, len(list_age_all_2points_50days),numpy.mean(list_age_all_2points_50days),numpy.std(list_age_all_2points_50days),mlab.prctile(list_age_all_2points_50days,p=(10,90,99)),"||",numpy.mean(list_activity_all_2points_50days),numpy.std(list_activity_all_2points_50days),mlab.prctile(list_activity_all_2points_50days,p=(10,90,99)),"||",numpy.mean(list_wi_all_2points_50days),numpy.std(list_wi_all_2points_50days),mlab.prctile(list_wi_all_2points_50days,p=(10,90,99)),"||",numpy.mean(list_ibmi_all_2points_50days),numpy.std(list_ibmi_all_2points_50days),mlab.prctile(list_ibmi_all_2points_50days,p=(10,90,99)),"||",numpy.mean(list_time_all_2points_50days),numpy.std(list_time_all_2points_50days),mlab.prctile(list_time_all_2points_50days,p=(10,90,99)),"||",numpy.mean(list_pwc_all_2points_50days),numpy.std(list_pwc_all_2points_50days),mlab.prctile(list_pwc_all_2points_50days,p=(10,90,99)),"\n\n"






    print >> file,  "2points & 50days & networked: # members, Age (mean, SD, 10th p, 90th p) || Activity (mean, SD, 10th p, 90th p) || #w-ins (mean, SD, 10th p, 90th p) || IBMI (mean, SD, 10th p, 90th p) || Time (mean, SD, 10th p, 90th p) || pwc (mean, SD, 10th p, 90th p)"

    print >> file,  len(list_age_all_2points_50days_networked),numpy.mean(list_age_all_2points_50days_networked),numpy.std(list_age_all_2points_50days_networked),mlab.prctile(list_age_all_2points_50days_networked,p=(10,90,99)),"||",numpy.mean(list_activity_all_2points_50days_networked),numpy.std(list_activity_all_2points_50days_networked),mlab.prctile(list_activity_all_2points_50days_networked,p=(10,90,99)),"||",numpy.mean(list_wi_all_2points_50days_networked),numpy.std(list_wi_all_2points_50days_networked),mlab.prctile(list_wi_all_2points_50days_networked,p=(10,90,99)),"||",numpy.mean(list_ibmi_all_2points_50days_networked),numpy.std(list_ibmi_all_2points_50days_networked),mlab.prctile(list_ibmi_all_2points_50days_networked,p=(10,90,99)),"||",numpy.mean(list_time_all_2points_50days_networked),numpy.std(list_time_all_2points_50days_networked),mlab.prctile(list_time_all_2points_50days_networked,p=(10,90,99)),"||",numpy.mean(list_pwc_all_2points_50days_networked),numpy.std(list_pwc_all_2points_50days_networked),mlab.prctile(list_pwc_all_2points_50days_networked,p=(10,90,99)),"\n\n"


    file.close()





    exit()

#############################




####################################
######################################
if __name__ == '__main__':
   
    main()
   
