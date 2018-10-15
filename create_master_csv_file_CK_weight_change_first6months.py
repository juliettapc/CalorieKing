#!/usr/bin/env python


'''
Code to read the CK database and the .gml file(s) to collect all info
on all users and create a csv master file for weight change and activity until 6months

Created by Julia Poncela, on September, 2013

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




    months6=182 # days
    months4=122 # days
    interval=20  # days  (to the left and right to calculate activity during final interval)
    first_day=datetime(2009,01,01)  # to exclude users with prior act




    ########### output file to put all info in
    filename0="./analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_p180_p120_within.txt"
    file0 = open(filename0,'wt')
    print >> file0, "ck_id label_id weight_change_4months weight_change_6months pwc_4months pwc_6months num_wins_4months num_wins_6months num_activity_4months num_activity_6months initial_BMI gender age height paying_info join_date join_time time_in_system p_120 p_180 p_friends p_120_friends p_180_friends outcome20 act20 wi_20 num_friends avg_w_change_friends betweenness num_R6_friends k_shell_index max_clique_size role "
    ############




    ####### input network files to collect the info from
    graph_name="./network_all_users/GC_full_network_all_users_merged_small_comm_roles_diff_layers1_roles_diff_layers1.5.gml"

    graph_name_kshell_info_GC="./network_all_users/GC_full_network_all_users_no_selfloops_kshells.gml"

  # both networks are only the GC!!!
  
    #########



    print "\nreading network file..."

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

#     if cont_testing <= 170:    ############### # to test the code out!!

        #cont_testing +=1

        if ck_id not in list_users_prior2009:

            list_users.append(ck_id)
            dict_master_user_info[ck_id]={}
            

#ck_id label_id weight_change percentage_weight_change number_weigh_ins num_activity initial_BMI gender age height paying_info join_date join_time time_in_system p_120 p_180  p_friends p_120_friends p_180_friends  outcome20 act20 wi_20 num_friends avg_w_change_friends betweenness num_R6_friends k_shell_index max_clique_size role 

            age=str(r1['age'])
            height=str(r1['height'])
            gender=str(r1['gender'])
            paying_info=str(r1['paying'])
            label=str(r1['id'])   # to match users from .gml and dB
            join_date=r1['join_date']  
            ibmi=r1['initial_weight'] *703./( float(height)*float(height) )


            dict_label_ck_id[label]=ck_id
            dict_ck_id_label[ck_id]=label
            
            
            dict_master_user_info[ck_id]['label']=label
            dict_master_user_info[ck_id]['age']=age
            dict_master_user_info[ck_id]['height']=height
            dict_master_user_info[ck_id]['gender']=gender
            dict_master_user_info[ck_id]['paying_info']=paying_info
            dict_master_user_info[ck_id]['join_date']=join_date    
            dict_master_user_info[ck_id]['ibmi']=ibmi
            
        # by default values:
            dict_master_user_info[ck_id]['friend_avg']="NA"
            dict_master_user_info[ck_id]['betweenness']=0
            dict_master_user_info[ck_id]['R6_overlap']=0   # no R6 friends
            dict_master_user_info[ck_id]['kshell_index']=0
            dict_master_user_info[ck_id]['max_clique_size'] =1
            dict_master_user_info[ck_id]['role']="NA"
            dict_master_user_info[ck_id]['list_friends_wc']=[]   # to calculate the avg wc of a user's friends (restri cted to 6months)
            dict_master_user_info[ck_id]['degree']=0

            dict_master_user_info[ck_id]['p_friends']=0


                   

    cont_users=0
    num_users_at_least2wins=0


    

    print "getting users' activity info..."
    #########################   
    cont=0
    for user in list_users:       
        cont+=1
        print cont,"/ 47000", user
        join_date= dict_master_user_info[user]['join_date']
        last_date_6months_user=join_date + timedelta(days=months6)               
        last_date_6months_user=datetime(last_date_6months_user.year, last_date_6months_user.month, last_date_6months_user.day)    # convert date to datetime

        last_date_4months_user=join_date + timedelta(days=months4)               
        last_date_4months_user=datetime(last_date_4months_user.year, last_date_4months_user.month, last_date_4months_user.day)    


        ###### to calculate p_120 
        interval_last_date_4months_left=last_date_4months_user - timedelta(days=interval) 
        interval_last_date_4months_left=datetime(interval_last_date_4months_left.year,interval_last_date_4months_left.month,interval_last_date_4months_left.day)

        interval_last_date_4months_right=last_date_4months_user + timedelta(days=interval) 
        interval_last_date_4months_right=datetime(interval_last_date_4months_right.year,interval_last_date_4months_right.month,interval_last_date_4months_right.day)

        ##### to calculate p_180 
        interval_last_date_6months_left=last_date_6months_user - timedelta(days=interval) 
        interval_last_date_6months_left=datetime(interval_last_date_6months_left.year,interval_last_date_6months_left.month,interval_last_date_6months_left.day)

        interval_last_date_6months_right=last_date_6months_user + timedelta(days=interval) 
        interval_last_date_6months_right=datetime(interval_last_date_6months_right.year,interval_last_date_6months_right.month,interval_last_date_6months_right.day)


      #  print "\n",user, "join:",join_date, " last6:",last_date_6months_user, " 4-:",interval_last_date_4months_left, " 4+:", interval_last_date_4months_right, " 6-:",interval_last_date_6months_left, " 6+:", interval_last_date_6months_right
      
        day20_mark_user =join_date + timedelta(days=20)       
        day20_mark_user=datetime(day20_mark_user.year, day20_mark_user.month, day20_mark_user.day) 

     

        query4="select  * from activity_combined where ck_id ='"+str(user)+"' order by activity_date asc"      #and activity_flag != '"+str("WI")+"'  and activity_date <= '"+str(last_date_6months_user)+ "' order by activity_date asc"
        result4= db.query(query4)  


        cont_act_4m=0
        cont_act_6m=0
        cont_act20=0
        
        lista_dates=[]
        for r4 in result4:
            lista_dates.append(datetime(r4['activity_date'].year,r4['activity_date'].month,r4['activity_date'].day))
      
        closest_date_within_4m= takeClosest_date(lista_dates, last_date_4months_user,interval)       
        closest_date_within_6m= takeClosest_date(lista_dates, last_date_6months_user,interval)


        dict_master_user_info[user]['p_120']=0
        dict_master_user_info[user]['p_180']=0

        for r4 in result4:
            activity_flag=r4['activity_flag']
            activity_date=r4['activity_date']
            activity_date=datetime(activity_date.year, activity_date.month, activity_date.day)    # convert date to datetime
            
            
            if activity_flag != "WI" and activity_date <= closest_date_within_6m:  # it is faster to filter with python than with mysql
                cont_act_6m +=1

                if activity_date <= closest_date_within_4m:
                    cont_act_4m +=1

               
                if activity_date <=day20_mark_user:  # for the act_20
                    cont_act20+=1



            if activity_date >=interval_last_date_4months_left and activity_date <=interval_last_date_4months_right :
                dict_master_user_info[user]['p_120']=1
            if activity_date >=interval_last_date_6months_left and activity_date <=interval_last_date_6months_right :
                dict_master_user_info[user]['p_180']=1


        #    print user, activity_flag, activity_date, dict_master_user_info[user]['p_120'],dict_master_user_info[user]['p_180']
       

        dict_master_user_info[user]['activity_4m']=cont_act_4m
        dict_master_user_info[user]['activity_6m']=cont_act_6m
        dict_master_user_info[user]['activity_20']=cont_act20


        dict_master_user_info[user]['time_in_system']=(result4[-1]['activity_date']- result4[0]['activity_date']).days #total time in system

      #  print user, "join:",join_date,"4m:",last_date_4months_user,dict_master_user_info[user]['activity_4m'],"6m:",last_date_6months_user,dict_master_user_info[user]['activity_6m']
       

   #     print user, "   ",dict_master_user_info[user]['p_120'],dict_master_user_info[user]['p_180']
      

  
    print "getting weigh-in info....."   
 ############### weigh_ins records
    for user in list_users:

        dict_master_user_info[user]['weight_change_4months']="NA"
        dict_master_user_info[user]['percentage_weight_change_4months']="NA"

        dict_master_user_info[user]['weight_change_6months']="NA"
        dict_master_user_info[user]['percentage_weight_change_6months']="NA"


        cont_users += 1
        print "\n\n",cont_users, user
        join_date = dict_master_user_info[user]['join_date']       
        last_date_4months_user=join_date + timedelta(days=months4)         
        last_date_6months_user=join_date + timedelta(days=months6)      
       
        day20_mark_user=join_date + timedelta(days=20)
      #  day20_mark_user=datetime(day20_mark_user.year, day20_mark_user.month, day20_mark_user.day) 



        query3="select  * from weigh_in_history where ck_id ='"+str(user)+"' and on_day <= '"+str(last_date_6months_user)+ "' order by on_day asc"
        result3= db.query(query3)   
        dict_master_user_info[user]['num_weigh_ins_6m']=len(result3)
    




        if len(result3) >0:  # some users dont have any w-in in the first 6months!!
         
            lista_dates=[]
            for r3 in result3:
                lista_dates.append(datetime(r3['on_day'].year,r3['on_day'].month,r3['on_day'].day))

      
            closest_date_within_4m= takeClosest_date(lista_dates, last_date_4months_user,interval)       
            closest_date_within_6m= takeClosest_date(lista_dates, last_date_6months_user,interval)


        #    print user, "   ",dict_master_user_info[user]['p_120'],dict_master_user_info[user]['p_180']




            first_weigh_in_date=result3[0]['on_day']
            last_weigh_in_date_6months=result3[-1]['on_day']
            
       
            dict_master_user_info[user]['outcome20']="NA"  # some users dont have weigh-ins within the first 20days
            list_weights_20=[]       
            list_weights_4m=[]        
            list_weights_6m=[]        
       

            for r3 in result3:
              weigh_in_date=r3['on_day']
              weight=r3['weight']

              if weigh_in_date <= day20_mark_user:  # for the outcome_20 and w_ins_20
                  list_weights_20.append(weight)
          
              if weigh_in_date <= closest_date_within_4m:
                  list_weights_4m.append(weight)

              if weigh_in_date <= closest_date_within_6m:
                  list_weights_6m.append(weight)




          

            if len(list_weights_20)>1:
              dict_master_user_info[user]['outcome20']=(list_weights_20[-1]-list_weights_20[0] )*100./list_weights_20[0]

            if len(list_weights_4m)>1:
              dict_master_user_info[user]['weight_change_4months']=list_weights_4m[-1]-list_weights_4m[0]          
              dict_master_user_info[user]['percentage_weight_change_4months']=(list_weights_4m[-1]-list_weights_4m[0])*100./ list_weights_4m[0]          


            if len(list_weights_6m)>1:
              dict_master_user_info[user]['weight_change_6months']=list_weights_6m[-1]-list_weights_6m[0]          
              dict_master_user_info[user]['percentage_weight_change_6months']=(list_weights_6m[-1]-list_weights_6m[0])*100./ list_weights_6m[0]          
            
              
            dict_master_user_info[user]['w_in20']=len(list_weights_20)
            dict_master_user_info[user]['num_weigh_ins_4m']=len(list_weights_4m)
            dict_master_user_info[user]['num_weigh_ins_6m']=len(list_weights_6m)
          


    #      print dict_master_user_info[user]['num_weigh_ins_4m'], dict_master_user_info[user]['num_weigh_ins_6m']
     #     print dict_master_user_info[user]['weight_change_4months'], dict_master_user_info[user]['weight_change_6months']
      #    print dict_master_user_info[user]['percentage_weight_change_4months'], dict_master_user_info[user]['percentage_weight_change_6months']
       #   print "act", dict_master_user_info[user]['activity_4m'], dict_master_user_info[user]['activity_6m']



         # print user, "join:",join_date,"4m:",last_date_4months_user,dict_master_user_info[user]['percentage_weight_change_4months'],dict_master_user_info[user]['num_weigh_ins_4m'],"  6m:",last_date_6months_user, dict_master_user_info[user]['percentage_weight_change_6months'],dict_master_user_info[user]['num_weigh_ins_6m']


#    raw_input()

    print "getting user's info from gml....."
    for node in G_kshell_info_GC.nodes():
        try:
            label_network=G_kshell_info_GC.node[node]['label']
            ck_id=dict_label_ck_id[label_network]        # do not get degree from the network, because it only includes the GC                        
        
            kshell_index=G_kshell_info_GC.node[node]["kshell_index"]
            dict_master_user_info[ck_id]['kshell_index']=kshell_index
        except: 
            print label_network, "not in the list of users"     #users with activity previous to Jan 2009



    for node in G.nodes():   # this is only the GC
        try:
            
            label_network=G.node[node]['label']
            ck_id=dict_label_ck_id[label_network]
            
            degree=G.node[node]['degree']
            dict_master_user_info[ck_id]['degree']=degree
            dict_master_user_info[ck_id]['p_friends']=1


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
                       # i remove duplicates and selfloops
                    if (src != user) and (src not in list_friends_in_users): # the friend is the src
                        list_friends_in_users.append(src)
                    elif (dest != user) and (dest not in list_friends_in_users): # the friend is the dest
                        list_friends_in_users.append(dest)


                    if src not in list_people_with_friends:
                        list_people_with_friends.append(src)
                    if dest not in list_people_with_friends:
                        list_people_with_friends.append(dest)

    
        if len(list_friends_in_users) != int(dict_master_user_info[user]['degree']): # double check num_friends here and compare with degree from network (that is only GC)
            if  int(dict_master_user_info[user]['degree']) >0:
                cont_discrepancies+=1
                print user, "discrepa en numero de amigos!"
       
           
        if len(list_friends_in_users) > 0 :
            dict_master_user_info[user]['p_friends']=1
            if dict_master_user_info[user]['degree']==0:   # cos the by default value is 0 but the GC already is been taken care of
                dict_master_user_info[user]['degree']=len(list_friends_in_users)                   
            


        cont_users_friendship+=1
        print cont_users_friendship

        for friend in list_friends_in_users:
            if dict_master_user_info[friend]['weight_change_6months'] != "NA":  # if the friend at least had 2points to calculate it
                dict_master_user_info[user]['list_friends_wc'].append(dict_master_user_info[friend]['weight_change_6months'])

        if  len(dict_master_user_info[user]['list_friends_wc'])>0:  # the by default value is NA
            dict_master_user_info[user]['friend_avg']=numpy.mean(dict_master_user_info[user]['list_friends_wc'])



        dict_master_user_info[user]['p_120_friends']=dict_master_user_info[user]['p_friends']*dict_master_user_info[user]['p_120']
        dict_master_user_info[user]['p_180_friends']=dict_master_user_info[user]['p_friends']*dict_master_user_info[user]['p_180']


    print  "# discrepancies friends db vs GC",cont_discrepancies
    print "# people with friends", len(list_people_with_friends)

   

    print "printing out final file....."
    ############### i print out the final data file
    for ck_id in list_users:   
        if dict_master_user_info[ck_id]['weight_change_6months'] != "NA":  # because some users dont have w-ins until more than 6months from their join date!
            print >> file0,ck_id,  dict_master_user_info[ck_id]['label'] , dict_master_user_info[ck_id]['weight_change_4months'], dict_master_user_info[ck_id]['weight_change_6months'], dict_master_user_info[ck_id]['percentage_weight_change_4months'], dict_master_user_info[ck_id]['percentage_weight_change_6months'], dict_master_user_info[ck_id]['num_weigh_ins_4m'], dict_master_user_info[ck_id]['num_weigh_ins_6m'],  dict_master_user_info[ck_id]['activity_4m'],  dict_master_user_info[ck_id]['activity_6m'],dict_master_user_info[ck_id]['ibmi'], dict_master_user_info[ck_id]['gender'], dict_master_user_info[ck_id]['age'], dict_master_user_info[ck_id]['height'], dict_master_user_info[ck_id]['paying_info'], dict_master_user_info[ck_id]['join_date'],dict_master_user_info[ck_id]['time_in_system'] ,dict_master_user_info[ck_id]['p_120'],dict_master_user_info[ck_id]['p_180'], dict_master_user_info[ck_id]['p_friends'], dict_master_user_info[ck_id]['p_120_friends'] , dict_master_user_info[ck_id]['p_180_friends'] ,dict_master_user_info[ck_id]['outcome20'] ,dict_master_user_info[ck_id]['activity_20'] , dict_master_user_info[ck_id]['w_in20'], dict_master_user_info[ck_id]['degree'], dict_master_user_info[ck_id]['friend_avg'], dict_master_user_info[ck_id]['betweenness'], dict_master_user_info[ck_id]['R6_overlap'], dict_master_user_info[ck_id]['kshell_index'], dict_master_user_info[ck_id]['max_clique_size'] ,dict_master_user_info[ck_id]['role']

     #   except :
      #      print ck_id, "is missing some info in the dict"           


    print "\n printed master file:", filename0
        
        


#############################

def takeClosest_date(lista, mark_date,interval):  # lista de fechas de weigh-ins y fecha de los 4m o 6m

  
    #print "list events:",lista
    #print "mark day:",mark_date


    closest=lista[-1]
    delta_min=10000
    for i in range(len(lista)):
        date_win=lista[i]
        delta=abs((date_win-mark_date).days)
     #   if delta <= interval:   # if no points are within the interval, i just pick the closest one to the mark anyway  (doesnt matter, cos i wont use them for the analysis, for having p_120 or p_180 =0)
        if delta <= delta_min:
            closest = date_win
            delta_min=delta
    #        print "  ",date_win,mark_date,closest, delta

   # print  "closest:",closest
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
