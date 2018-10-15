#! /usr/bin/env python

import csv
import networkx as nx
import numpy
import sys

def main(master_csv,strength_links_csv):


    name1="network_all_users/master_with_GINI_coef_friendships_strenght_friendship_with_R6s.csv"           
    file=open(name1, 'wt')   
   
    print >> file,'id','ck_id','join_date','initial_weight','most_recent_weight','height','age','weighins','initial_bmi','final_bmi','percentage_weight_change','weight_change','time_in_system','outcome20','outcome50','p_50','act_20','wi_20','p_friend','R6_overlap','degree','friend_avg','activity','gini_friendships','gini_to_friends','gini_from_friends','sum_strength_with_R6s','sum_strength_to_R6s','sum_strength_from_R6s'

    dict_dict_strength_links={}

    cont1=0
    resultado_strength_links= csv.reader(open(strength_links_csv, 'rb'), delimiter=' ')#, quotechar='|')
#label ck_id gini_friendships gini_to_friends gini_from_friends sum_strength_with_R6s sum_strength_to_R6s sum_strength_from_R6s

    for row in resultado_strength_links:
        if cont1>0:           
          
            label=int(row[0]) 
            dict_one_user={}

            dict_one_user['label']=int(row[0])
            dict_one_user['ck_id']=str(row[1])
            dict_one_user['gini_friendships']=row[2]
            dict_one_user['gini_to_friends']=row[3]
            dict_one_user['gini_from_friends']=row[4]
            dict_one_user['sum_strength_with_R6s']=row[5]
            dict_one_user['sum_strength_to_R6s']=row[6]
            dict_one_user['sum_strength_from_R6s']=row[7]
           
            dict_dict_strength_links[label]=dict_one_user
        cont1+=1


  
   


    dict_dict_master={}

    cont2=0
    resultado_master= csv.reader(open(master_csv, 'rb'), delimiter=',')#, quotechar='|')
#id,ck_id,join_date,initial_weight,most_recent_weight,height,age,weighins,initial_bmi,final_bmi,percentage_weight_change,weight_change,time_in_system,outcome20,outcome50,p_50,act_20,wi_20,p_friend,R6_overlap,degree,friend_avg,activity

    for row in resultado_master:
       # print row
        if cont2>0:
            label=int(row[0]) 
            dict_one_user={}
            
            dict_one_user['id']=row[0]
            dict_one_user['ck_id']=row[1]
            dict_one_user['join_date']=row[2]
            dict_one_user['initial_weight']=row[3]
            dict_one_user['most_recent_weight']=row[4]
            dict_one_user['height']=row[5]
            dict_one_user['age']=row[6]
            dict_one_user['weighins']=row[7]
            dict_one_user['initial_bmi']=row[8]
            dict_one_user['final_bmi']=row[9]
            dict_one_user['percentage_weight_change']=row[10]
            dict_one_user['weight_change']=row[11]
            dict_one_user['time_in_system']=row[12]
            dict_one_user['outcome20']=row[13]
            dict_one_user['outcome50']=row[14]
            dict_one_user['p_50']=row[15]
            dict_one_user['act_20']=row[16]
            dict_one_user['wi_20']=row[17]
            dict_one_user['p_friend']=row[18]
            dict_one_user['R6_overlap']=row[19]
            dict_one_user['degree']=row[20]
            dict_one_user['friend_avg']=row[21]
            dict_one_user['activity']=row[22]
            
            dict_dict_master[label]=dict_one_user

        cont2+=1
    

    for item in dict_dict_master:   # loop over the KEYS of the dict   (== over the ck_ids)
      #  print item , dict_dict_master[item]['label']  # are the same thing!
       # print dict_dict_master[item]
        #print dict_dict_master[item]['label']

        print >> file, dict_dict_master[item]['id'],dict_dict_master[item]['ck_id'],dict_dict_master[item]['join_date'],dict_dict_master[item]['initial_weight'],dict_dict_master[item]['most_recent_weight'],dict_dict_master[item]['height'],dict_dict_master[item]['age'],dict_dict_master[item]['weighins'],dict_dict_master[item]['initial_bmi'],dict_dict_master[item]['final_bmi'],dict_dict_master[item]['percentage_weight_change'],dict_dict_master[item]['weight_change'],dict_dict_master[item]['time_in_system'],dict_dict_master[item]['outcome20'],dict_dict_master[item]['outcome50'],dict_dict_master[item]['p_50'],dict_dict_master[item]['act_20'],dict_dict_master[item]['wi_20'],dict_dict_master[item]['p_friend'],dict_dict_master[item]['R6_overlap'],dict_dict_master[item]['degree'],dict_dict_master[item]['friend_avg'],dict_dict_master[item]['activity'],

        print >> file,dict_dict_strength_links[item]['gini_friendships'],dict_dict_strength_links[item]['gini_to_friends'],dict_dict_strength_links[item]['gini_from_friends'],dict_dict_strength_links[item]['sum_strength_with_R6s'],dict_dict_strength_links[item]['sum_strength_to_R6s'],dict_dict_strength_links[item]['sum_strength_from_R6s']

  

        
       
        

################################################

          
if __name__ == '__main__':
    if len(sys.argv) > 2:
        master_csv = sys.argv[1]
        strength_links_csv = sys.argv[2]
       

        main(master_csv,strength_links_csv)
    else:
        print "usage: python  whatever.py   path/master.csv  path/strength_links.csv"
 
     

##############################################
