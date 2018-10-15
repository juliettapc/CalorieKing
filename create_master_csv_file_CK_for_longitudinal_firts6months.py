#!/usr/bin/env python


'''
Code to read the CK database and the .gml file(s) to collect all info
on all users and create a csv master file for the longitudinal study.

Created by Julia Poncela, on April 22th, 2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from database import *   
from datetime import *
import dateutil

def main():
 


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 




    end_initiation=182 # days
    first_day=datetime(2009,01,01)  # to exclude users with prior act




    ########### output file to put all info in
    filename0="./analysis_time_bins_bmi_groups/master_users_file_for_longitudinal_first6months.txt"
    file0 = open(filename0,'wt')
    print >> file0, "ck_id label_id day weight at_least_2w_ins num_activity initial_BMI gender age height paying_info join_date join_time num_friends avg_w_change_friends betweenness num_R6_friends k_shell_index max_clique_size role percent_wins_14 percent_wins_28"
    ############




    ####### input network files to collect the info from
    graph_name="./network_all_users/GC_full_network_all_users_merged_small_comm_roles_diff_layers1_roles_diff_layers1.5.gml"

    graph_name_kshell_info_GC="./network_all_users/GC_full_network_all_users_no_selfloops_kshells.gml"

  # both networks are only the GC!!!

    csv_file="./network_all_users/master_csv_gender_pay_info.csv"
    #########




    ######### i build the networks  (remember label attribute matches id in users table)
    G = nx.read_gml(graph_name)
    GC_G = nx.connected_component_subgraphs(G)[0] 

   # print len(G.nodes()), len(GC_G.nodes())  #  1910   (they are both the GC)
    
    G_kshell_info_GC = nx.read_gml(graph_name_kshell_info_GC)
   # GC_G_kshell_info_GC = nx.connected_component_subgraphs(G_kshell_info_GC)[0] 

 
    #########


  

    print "getting users with activity prior 2009....."
    #########################                     
    query4="select  * from activity_combined order by activity_date asc"
    result4= db.query(query4)                

    list_users_prior2009=[]
    for r4 in result4:

        ck_id=r4['ck_id']
        act_date=r4['activity_date']
        act_date=datetime(act_date.year, act_date.month, act_date.day)    # convert date to datetime

        if act_date < first_day:
            if ck_id not in list_users_prior2009:
                list_users_prior2009.append(ck_id)



    print  "# users activity prior 2009:", len(list_users_prior2009)





   # print "network sizes","   tot:",len(G.nodes()),"   GC:",len(GC_G.nodes()), "  kshell:", len(G_kshell_info_GC.nodes()), "  kshell_GC:", len(GC_G_kshell_info_GC.nodes()), "  engaged:",len(G_kshell_info_engaged.nodes()), "  GC engaged:",len(GC_G_kshell_info_engaged.nodes())   # they are all GC!!!
   

    print "getting user's info from dB....."
    dict_ck_id_label={}
    dict_label_ck_id={}
    dict_master_user_info={}


    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict.   
    list_users=[] 

    cont_testing=0

    for r1 in result1:
        ck_id =str(r1['ck_id'])

     # if cont_testing <= 1500:    ############### # to test the code out!!

      #  cont_testing +=1

        if ck_id not in list_users_prior2009:

            list_users.append(ck_id)
            dict_master_user_info[ck_id]={}
            
            age=str(r1['age'])
            height=str(r1['height'])
            gender=str(r1['gender'])
            paying_info=str(r1['paying'])
            label=str(r1['id'])   # to match users from .gml and dB
            join_date=r1['join_date']  

            dict_label_ck_id[label]=ck_id
            dict_ck_id_label[ck_id]=label
            
            
            dict_master_user_info[ck_id]['label']=label
            dict_master_user_info[ck_id]['age']=age
            dict_master_user_info[ck_id]['height']=height
            dict_master_user_info[ck_id]['gender']=gender
            dict_master_user_info[ck_id]['paying_info']=paying_info
            dict_master_user_info[ck_id]['join_date']=join_date    

            
        # by default values:
            dict_master_user_info[ck_id]['friend_avg']="NA"
            dict_master_user_info[ck_id]['betweenness']="NA"
            dict_master_user_info[ck_id]['R6_overlap']=0   # no R6 friends
            dict_master_user_info[ck_id]['kshell_index']="NA"
            dict_master_user_info[ck_id]['max_clique_size'] ="NA"
            dict_master_user_info[ck_id]['role']="NA"
            dict_master_user_info[ck_id]['list_friends_wc']=[]   # to calculate the avg wc of a user's friends (restri cted to 6months)
            dict_master_user_info[ck_id]['weigh_in_history']=[]
            dict_master_user_info[ck_id]['percent_wins_14']=[]
            dict_master_user_info[ck_id]['percent_wins_28']=[]
            

    cont_users=0
    num_users_at_least2wins=0




    print "getting users' activity info..."
    #########################   
    cont=0
    for user in list_users:       
        cont+=1
        print cont,"/ 47000"
        join_date= dict_master_user_info[user]['join_date']
        last_date_6months_user=join_date + timedelta(days=end_initiation)               
        last_date_6months_user=datetime(last_date_6months_user.year, last_date_6months_user.month, last_date_6months_user.day)    # convert date to datetime
       # print user, join_date, last_date_6months_user,"act",last_date_6months_user-join_date

        query4="select  * from activity_combined where ck_id ='"+str(user)+"' order by activity_date asc" #and activity_flag != '"+str("WI")+"'  and activity_date <= '"+str(last_date_6months_user)+ "' order by activity_date asc"
        result4= db.query(query4)  

        cont_act=0
        for r4 in result4:
            activity_flag=r4['activity_flag']
            activity_date=r4['activity_date']
            activity_date=datetime(activity_date.year, activity_date.month, activity_date.day)    # convert date to datetime
            
            

            if activity_flag != "WI" and activity_date <= last_date_6months_user:
                cont_act +=1
        dict_master_user_info[user]['activity']=cont_act
        

    print "getting weigh-in info....."   
 ############### weigh_ins records
    for user in   list_users:

        dict_master_user_info[user]['weight_change_6months']="NA"

        cont_users += 1
        print cont_users
        join_date = dict_master_user_info[user]['join_date']       
        last_date_6months_user=join_date + timedelta(days=end_initiation)       

      


        query3="select  * from weigh_in_history where ck_id ='"+str(user)+"' and on_day <= '"+str(last_date_6months_user)+ "' order by on_day asc"
        result3= db.query(query3)   
         

        if len(result3) >0:  # some users dont have any w-in in the first 6months!!
         
          first_weigh_in_date=result3[0]['on_day']
          last_weigh_in_date_6months=result3[-1]['on_day']

       #   print user, join_date, last_date_6months_user,"wins",last_date_6months_user-join_date,last_weigh_in_date_6months-first_weigh_in_date
          

          dict_master_user_info[user]['weight_change_6months']=result3[-1]['weight'] - result3[0]['weight']

          for r3 in result3:    
            pair_weight_day=[]
         
            weigh_in_date=r3['on_day']          
            weight=r3['weight']

            delta_days=(weigh_in_date-first_weigh_in_date).days+1  
            
            if delta_days <= end_initiation:
                pair_weight_day.append(delta_days)
                pair_weight_day.append(weight)
                
                dict_master_user_info[user]['weigh_in_history'].append(pair_weight_day)
             

          dict_master_user_info[user]['weigh_ins']=len(dict_master_user_info[user]['weigh_in_history'])

          if len(dict_master_user_info[user]['weigh_in_history'])  >= 2:
            dict_master_user_info[user]['at_least_2w_ins']= 1
            num_users_at_least2wins +=1

          else:
            dict_master_user_info[user]['at_least_2w_ins']= 0


     #   print user,len(result3), len(dict_master_user_info[user]['weigh_in_history']), dict_master_user_info[user]['at_least_2w_ins']
       


    print "num users with at least 2-wins in the first 6months:",num_users_at_least2wins
   
 
    
    print "getting user's info from gml....."
    for node in G_kshell_info_GC.nodes():
        try:
            label_network=G_kshell_info_GC.node[node]['label']
            ck_id=dict_label_ck_id[label_network]        # do not get degree from the network, because it only includes the GC                        
        
            kshell_index=G_kshell_info_GC.node[node]["kshell_index"]
            dict_master_user_info[ck_id]['kshell_index']=kshell_index
        except: 
            print label_network, "not in the list of users"     #users with activity previous to Jan 2009



    for node in G.nodes():
        try:
            
            label_network=G.node[node]['label']
            ck_id=dict_label_ck_id[label_network]
            
            R6_overlap=G.node[node]['R6_overlap']
            dict_master_user_info[ck_id]['R6_overlap']=R6_overlap
            
            max_clique_size=G.node[node]['max_clique_size']
            dict_master_user_info[ck_id]['max_clique_size']=max_clique_size
            
            role=G.node[node]['role']
            dict_master_user_info[ck_id]['role']=role
            
            betweenness=G.node[node]['betweenness']
            dict_master_user_info[ck_id]['betweenness']=betweenness
        except: 
            print label_network, "not in the list of users"#users with activity previous to Jan 2009


    print "getting user's info from csv....."
    ################# getting info from csv
    list_users_from_csv=[]
    file_csv_info=open(csv_file,'r')
    list_lines_file_csv_info=file_csv_info.readlines()  
    cont=0           
    for line in list_lines_file_csv_info:
        if cont >0: 
            list_elements_line=line.strip("\r\n").split(" ")

            try:
            
                label=str(list_elements_line[0])
                ck_id=str(list_elements_line[1])      
                
                if ck_id in list_users:
                    
                    ibmi=str(list_elements_line[9])
                    degree=str(list_elements_line[21])
                    
                    dict_master_user_info[ck_id]['ibmi']=ibmi
                    dict_master_user_info[ck_id]['degree']=degree
                    
                    
                    if ck_id not in list_users_from_csv:
                        list_users_from_csv.append(ck_id)
            except:
                pass#     print label,ck_id, "not in the list of users"


        cont+=1
       
    print  "intersection list_users  vs users from csv",len(list(set(list_users) & set(list_users_from_csv)))   # the two list are identical!  intersection= 47094




    print "getting friendship's info from dB....."
    ################# friendship info
    list_people_with_friends=[]
    cont_discrepancies=0
    cont_users_friendship=0
    for user in   list_users:

       

        query2=" select  * from friends where (src ='"+str(user)+"')or (dest ='"+str(user)+"') "    # because there are friends that are not in the users table
        result2 = db.query(query2)  # is a list of dicts.   
  
        list_friends_in_users=[]   # there are DUPLICATE friendships

        for r2 in result2:
            src=str(r2['src'])
            dest=str(r2['dest'])

            if src != dest:   # ignore self-loops

                if (src in list_users) and (dest in list_users):

                    if (src != user) and (src not in list_friends_in_users): # the friend is the src
                        list_friends_in_users.append(src)
                    elif (dest != user) and (dest not in list_friends_in_users): # the friend is the dest
                        list_friends_in_users.append(dest)


                    if src not in list_people_with_friends:
                        list_people_with_friends.append(src)
                    if dest not in list_people_with_friends:
                        list_people_with_friends.append(dest)


    #    print  user, len(result2),len(list_friends_in_users), dict_master_user_info[user]['degree']    
        if len(list_friends_in_users) != int(dict_master_user_info[user]['degree']): # double check num_friends here and compare with degree from network (that is only GC)

            cont_discrepancies+=1
           
           
        dict_master_user_info[user]['degree']=len(list_friends_in_users)
        cont_users_friendship+=1
        print cont_users_friendship

        for friend in list_friends_in_users:
            if dict_master_user_info[friend]['weight_change_6months'] != "NA":  # if the friend at least had 2points to calculate it
                dict_master_user_info[user]['list_friends_wc'].append(dict_master_user_info[friend]['weight_change_6months'])

        if  len(dict_master_user_info[user]['list_friends_wc'])>0:  # the by default value is NA
            dict_master_user_info[user]['friend_avg']=numpy.mean(dict_master_user_info[user]['list_friends_wc'])






    print  "# discrepancies friends db vs GC",cont_discrepancies
    print "# people with friends", len(list_people_with_friends)



    ##### i generate the average percent of day a user weighs herself in over the first 14, 28, etc days
    list_28_periods=[]
    list_14_periods=[]
    for i in range(1,20):
        if i*14 <= end_initiation+14:
            list_14_periods.append((i*14))   #[14, 28, 42, 56, 70, 84, 98, 112, 126, 140, 154, 168, 182, 196]

        if i*28 <= end_initiation+28:
            list_28_periods.append((i*28))   #[28, 56, 84, 112, 140, 168, 196]



  

    for ck_id in dict_master_user_info:   # (for key in dict.)
                                           
        for i in range(len(dict_master_user_info[ck_id]['weigh_in_history'])):  # one line per weigh-in and per user
                
            day=dict_master_user_info[ck_id]['weigh_in_history'][i][0]                
            
            if day>1:   # i need to exclude the first weigh in for the averages                   
                
                if day <= list_14_periods[-1]:   # to avoid days after the 6month mark
                    value=takeClosest_smaller(list_14_periods, day)
                    avg_14=float(i)/ float(value) *100.               
                    
                    pair_day_14=[]
                    
                    pair_day_14.append(day)
                    pair_day_14.append(avg_14)                                                       
                    dict_master_user_info[ck_id]['percent_wins_14'].append(pair_day_14)  


                if day <= list_28_periods[-1]:
                    value=takeClosest_smaller(list_28_periods, day)
                    avg_28=float(i)/ float(value) *100.               
                    
                    pair_day_28=[]
                    
                    pair_day_28.append(day)
                    pair_day_28.append(avg_28)                                                       
                    dict_master_user_info[ck_id]['percent_wins_28'].append(pair_day_28)  

  
                
                                                
            else:       # the first weigh-in doesnt have an associated value for 14 or 28 day average                        
                dict_master_user_info[ck_id]['percent_wins_14'].append([day, "NA"])                   
                dict_master_user_info[ck_id]['percent_wins_28'].append([day, "NA"])                   

                
   #     print ck_id, dict_master_user_info[ck_id]['percent_wins_14'],len(dict_master_user_info[ck_id]['percent_wins_14']),len(dict_master_user_info[ck_id]['weigh_in_history'])
    #    print ck_id, dict_master_user_info[ck_id]['percent_wins_28'],len(dict_master_user_info[ck_id]['percent_wins_28']),len(dict_master_user_info[ck_id]['weigh_in_history'])
      







    print "printing out final file....."
    ############### i print out the final data file
    for ck_id in dict_master_user_info:   # (for key in dict.)
        for i in range(len(dict_master_user_info[ck_id]['weigh_in_history'])):  # one line per weigh-in and per user

            day=dict_master_user_info[ck_id]['weigh_in_history'][i][0]
            weight=dict_master_user_info[ck_id]['weigh_in_history'][i][1]

            try:
                print >> file0,ck_id,  dict_master_user_info[ck_id]['label'] , day, weight, dict_master_user_info[ck_id]['at_least_2w_ins'], dict_master_user_info[ck_id]['activity'],dict_master_user_info[ck_id]['ibmi'], dict_master_user_info[ck_id]['gender'], dict_master_user_info[ck_id]['age'], dict_master_user_info[ck_id]['height'], dict_master_user_info[ck_id]['paying_info'], dict_master_user_info[ck_id]['join_date'], dict_master_user_info[ck_id]['degree'], dict_master_user_info[ck_id]['friend_avg'], dict_master_user_info[ck_id]['betweenness'], dict_master_user_info[ck_id]['R6_overlap'], dict_master_user_info[ck_id]['kshell_index'], dict_master_user_info[ck_id]['max_clique_size'] ,dict_master_user_info[ck_id]['role'],dict_master_user_info[ck_id]['percent_wins_14'][i][1],dict_master_user_info[ck_id]['percent_wins_28'][i][1]

            except IndexError:
                print ck_id
                print dict_master_user_info[ck_id]['weigh_in_history']
                print dict_master_user_info[ck_id]['percent_wins_14']
                print dict_master_user_info[ck_id]['percent_wins_28']

    print "\n printed file:", filename0
        



#############################3

def takeClosest_smaller(lista, number):

    if number > lista[-1]:       
        print  "number larger than the upper limit!", number, lista[-1]
       # raw_input()


    closest=lista[0]
    minimo=0
    for i in range(len(lista)):
        if number <= lista[i] and number > minimo:
            closest=lista[i]
            minimo=lista[i]

    return closest
        



##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename_network1 = sys.argv[1]
    #    filename_network_for_kshell = sys.argv[2]
   
     #   main(filename_network1,filename_network_for_kshell)
    #else:
     #   print "Usage: python script.py path/filename.gml  path/filename_for_kshell.gml"

    
    main()
