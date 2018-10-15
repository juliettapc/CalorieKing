#! /usr/bin/env python

import csv
import networkx as nx
import numpy

def main():

    input_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_no_bias/master_csv.csv"  
    resultado= csv.reader(open(input_name, 'rb'), delimiter=',')#, quotechar='"')

    output_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_no_bias/master_csv_Prob_2point.csv"  
    file=open(output_name, 'wt')
    print >> file,"id ck_id join_date join_time initial_weight most_recent_weight height age weighins initial_bmi final_bmi percentage_weight_change weight_change time_in_system outcome20 outcome50 p_50 act_20 wi_20 p_friend R6_overlap degree friend_avg activity P_2points"

#id,ck_id,join_date,initial_weight,most_recent_weight,height,age,weighins,initial_bmi,final_bmi,percentage_weight_change,weight_change,time_in_system,outcome20,outcome50,p_50,act_20,wi_20,p_friend,R6_overlap,degree,friend_avg,activity

    num_time_0=0
    cont_lines=0
    for row in resultado:        
        if cont_lines>0:
            if str(row[14])=="NA":                
                for i in range(len(row)):
                    print >> file,row[i],
                print >> file,0                   
                
            else:               
                for i in range(len(row)):
                    print >> file,row[i],
                print >> file,1

           # print type (row[12]),type (int(row[12]))
            if int(row[12]) <=0:   
                #print row[0],row[12]               
                num_time_0+=1
                  
           
           
      
        cont_lines+=1   

   
    file.close()

    print "number of users with 'time in the system<=0'",num_time_0
########################################
if __name__== "__main__":   
    
    main()
######################################
