#! /usr/bin/env python

import csv
import networkx as nx
import numpy


def main():


    H = nx.read_gml("network_no_bias/full_network_all_users_no_selfloops_kshells.gml")
    

    input_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_no_bias/master_csv.csv"  
    resultado= csv.reader(open(input_name, 'rb'), delimiter=',')#, quotechar='"')

    output_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_no_bias/master_csv_Prob_2point_kshell.csv"  
    file=open(output_name, 'wt')
    print >> file,"id ck_id join_date join_time initial_weight most_recent_weight height age weighins initial_bmi final_bmi percentage_weight_change weight_change time_in_system outcome20 outcome50 p_50 act_20 wi_20 p_friend R6_overlap degree friend_avg activity P_2points kshell"

#id,ck_id,join_date,initial_weight,most_recent_weight,height,age,weighins,initial_bmi,final_bmi,percentage_weight_change,weight_change,time_in_system,outcome20,outcome50,p_50,act_20,wi_20,p_friend,R6_overlap,degree,friend_avg,activity

    num_time_0=0
    cont_lines=0
    for row in resultado:        
        if cont_lines>0:

            label=int(row[0])
           
            node_exists=0   #flag
            for i in H.nodes():
                if int(H.node[i]["label"])==label:
                    node=i
                    node_exists=1
           
               
            if node_exists==1:
                
                if str(row[14])=="NA":                
                    for i in range(len(row)):
                        print >> file,row[i],
                    print >> file,0,H.node[node]["kshell_index"]                   
                    
                else:               
                    for i in range(len(row)):
                        print >> file,row[i],
                    print >> file,1,H.node[node]["kshell_index"] 




            else:  #not network people
                if str(row[14])=="NA":                
                    for i in range(len(row)):
                        print >> file,row[i],
                    print >> file,0,0                  
                        
                else:               
                    for i in range(len(row)):
                        print >> file,row[i],
                    print >> file,1,0


            if int(row[12]) <=0:                            
                num_time_0+=1
                  
           
           
      
        cont_lines+=1   

   
    file.close()

    print "number of users with 'time in the system<=0'",num_time_0
########################################
if __name__== "__main__":   
    
    main()
######################################
