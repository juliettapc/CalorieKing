#!/usr/bin/env python


'''
Explain here what does this code do.

Created by Julia Poncela, on April 8th, 2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from database import *   #package to handle databases
from datetime import *
import dateutil
import operator

def main():
 
    
    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 

    

    starting_date=datetime(2009,1,1)   #datetime(yy,mm,ddt)
    last_day_of_database=datetime(2010,12,31)   #datetime(yy,mm,ddt)   



    filename0="./analysis_time_bins_bmi_groups/weekly_list_friends.dat"
    file0 = open(filename0,'wt')
    print >> file0, "ck_id  label week_start_date - week_stop_date    tot_num_friends_that_week  tot_num_friends  list_friends_that_week "


    filename1="./analysis_time_bins_bmi_groups/weekly_list_friends_simplified.dat"
    file1 = open(filename1,'wt')
    print >> file1, "label  week_index  tot_num_friends_that_week  tot_num_friends "


    filename3="./analysis_time_bins_bmi_groups/weekly_list_members.dat"
    file3 = open(filename3,'wt')
   



    ############# i create an empty dictionary of dictionaries that will save the weekly list of friends of each user
    dict_date_week_index={}
    dict_dict_weeks_list_friends_each_user={}   
    current_week_date=starting_date
    cont=1
    for i in range(104):   # two years worth of weeks 
        dict_dict_weeks_list_friends_each_user[current_week_date]={}       
        dict_date_week_index[current_week_date]=cont

        current_week_date += timedelta(days=7)
        cont+=1
   

    ###############  i preselect onlye the users with friends, so the rest of the queries run faster
    query1="""SELECT * FROM users order by join_date asc"""    
    result1 = db.query(query1)  # is a list of dict.   
    list_users=[] 
    for r1 in result1:
        ck_id =str(r1['ck_id'])     
        if ck_id not in list_users:
            list_users.append(ck_id)



    query0="""SELECT * FROM friends"""    
    result0 = db.query(query0)  
  
    print "\ndoing preselection of users with friends..."
    list_users_with_friends=[]
    for r0 in result0:
        src=str(r0['src'])
        dest=str(r0['dest'])
       
        if src not in list_users_with_friends:
            if src in list_users:
                list_users_with_friends.append(src)   # because some friends are not users from the user_table

        if dest not in list_users_with_friends:
            if dest in list_users:
                list_users_with_friends.append(dest)

  
    print "   done!\n"

    ################ i create and populate the dict of users_tot_list_friends
    dict_users_list_friends={}    
    dict_ck_id_label={}
    print "creating empty dict users_list_friends..."

    
    for r1 in result1:    #loop over users
        ck_id =str(r1['ck_id'])     
        label= str(r1['id'])              
        dict_ck_id_label[ck_id]=label

        if ck_id in list_users_with_friends:
            dict_users_list_friends[ck_id]=[]

       

        
    print "   done!"

    print "# users",len(list_users)
    print "# users with friends (that are also in the users_table)", len(list_users_with_friends)
   
    

#    print "\nnumber users from friends_table:",len(list_users_with_friends), "number users:",len(list_users), "\nintersection (from users_table who have friends)" ,len(list_users_with_friends_from _users_table)

    print "\ncreating dict of users' list of friends..."

    for r0 in result0:   # loop over friendships
        src=str(r0['src'])
        dest=str(r0['dest'])
        if (src in list_users_with_friends)  and (dest in list_users_with_friends): # because there are some friendships among some users that are NOt in the users table!!!  (those friendships, i ignore)

            if src not in dict_users_list_friends[dest]:
                dict_users_list_friends[dest].append(src)
            if dest not in dict_users_list_friends[src]:
                dict_users_list_friends[src].append(dest)

    print "   done!"

    print "size of dict for users with friends", len(dict_users_list_friends)

   
   
    print "getting users' membership periods..."
    ###############  i study each user (but only if they have friends)

   
    dict_users_membership_periods={}
    cont_num_friendships=0
    for r1 in result1:   # loop over users
        
        cont_num_friendships+=1
        ck_id =str(r1['ck_id'])               
        join_date=r1['join_date']

        if ck_id in list_users_with_friends:
            
            dict_users_membership_periods[ck_id]={}
            cont_pairs=0  # membership start/stop pairs 


            ############## i obtain the membership periods for that user (and i put it in the dict of dicts.)
            query2="select  * from membership_periods where ck_id ='"+str(ck_id)+"' order by on_day,type"  
            result2= db.query(query2)    

           
            for r2 in result2:                                       
               
                if r2['type']=="START":
                    
                    pair_start_end=[]
                    membership_start=r2['on_day']
                    membership_start=datetime.combine(membership_start, time())   # need to convert from date to datetime (because weigh in are datetime) 
                    flag_start=1                                        
                    
                    pair_start_end.append(membership_start)  # everyone has a START, not everyone has a STOP
                    flag_end=0
                    
                    
        
                elif r2['type']=="END":
                    cont_pairs+=1
                    
                    membership_stop=r2['on_day']
                    membership_stop=datetime.combine(membership_stop, time())   # need to convert from date to datetime (because weigh in are datetime)                                         
                    
                    pair_start_end.append(membership_stop)                    
                    dict_users_membership_periods[ck_id][cont_pairs]=pair_start_end                    
                    flag_end=1
        
        
            if flag_end==0:   # user without a final STOP date
                    cont_pairs+=1
                    pair_start_end.append(last_day_of_database)  # if it is an open_account, i add the last day of the db as ending membership date for the user
                    dict_users_membership_periods[ck_id][cont_pairs]=pair_start_end
                                        
        #print dict_users_membership_periods[ck_id]

    print "   done!"     

    print "number users with membership period info:",len(dict_users_membership_periods)


    #############   i find out what active friends each user has each week  (active== in the middle of a membership period)



    sorted_dict_dict_weeks_list_friends_each_user=sorted(dict_dict_weeks_list_friends_each_user.iteritems(), key=operator.itemgetter(0))#, reverse=True)   # the index in itemgetter is to sort 0: by key, 1: by value  --->> sorted_dict is  a list of tuples: key, dict[key]



    for user in list_users_with_friends:
       
                    
        filename2="./analysis_time_bins_bmi_groups/indiv_users_lists/weekly_number_friends_user"+str(dict_ck_id_label[user])+"_tot_num_friends"+str(len(dict_users_list_friends[user]))+"_number_memebership_periods"+str(len(dict_users_membership_periods[user]))+".dat"   #dict_users_membership_periods[ck_id]
        file2 = open(filename2,'wt')


        
        for pair_key_value in sorted_dict_dict_weeks_list_friends_each_user:   #loop over weeks

            beginning_week=pair_key_value[0]
            end_week=beginning_week+timedelta(days=7)

              

          

            flag_user_is_member_that_week=is_user_active_that_week(dict_users_membership_periods, user,beginning_week,end_week)



            
            if  flag_user_is_member_that_week ==1:  
             #   print user, " was active during week:", beginning_week, "and ", end_week, "because his/her membership periods are:",dict_users_membership_periods[user]

                dict_dict_weeks_list_friends_each_user[beginning_week][user]=[]   # i initialize all active users' list of friends for that week



                print "\n\n"

            
                for friend in dict_users_list_friends[user]:

                    if friend in list_users_with_friends:

                        flag_friend_is_member_that_week=is_user_active_that_week(dict_users_membership_periods, friend,beginning_week,end_week)

                    
                        if  flag_friend_is_member_that_week ==1:                          
                            dict_dict_weeks_list_friends_each_user[beginning_week][user].append(friend)
                            print "during week:",beginning_week,"-",end_week,"  ",user, "  and  ", friend, " are friends"
                        
             



                print "during week:",beginning_week,"-",end_week," user ",user, "(whose membership periods are: ",dict_users_membership_periods[user],")   has",len(dict_dict_weeks_list_friends_each_user[beginning_week][user])," friend(s), out of a total of", len(dict_users_list_friends[user])


                print >> file0, user, dict_ck_id_label[user], beginning_week,"-",end_week, len(dict_dict_weeks_list_friends_each_user[beginning_week][user]), len(dict_users_list_friends[user]), dict_dict_weeks_list_friends_each_user[beginning_week][user]

                print >> file1, dict_ck_id_label[user], dict_date_week_index[beginning_week], len(dict_dict_weeks_list_friends_each_user[beginning_week][user]), len(dict_users_list_friends[user])

                print >> file2,  dict_date_week_index[beginning_week], len(dict_dict_weeks_list_friends_each_user[beginning_week][user]), len(dict_users_list_friends[user])



                print "  friends memberships:"
                for i in dict_users_list_friends[user]:
                    print "    ",i, dict_users_membership_periods[i]

               # if len(dict_dict_weeks_list_friends_each_user[beginning_week][user]) >0:
                #    raw_input()


   
           # else:
            #    print user, " was NOT active during week:", beginning_week, "and ", end_week, "because his/her membership periods are:",dict_users_membership_periods[user]
        file2.close()

    file0.close()
    file1.close()



    ############### i calculate the number of members for each week  (3 diff. methods)
   
    for pair_key_value in sorted_dict_dict_weeks_list_friends_each_user:
        beginning_week=pair_key_value[0]
        end_week=beginning_week+timedelta(days=7)
        week_index=dict_date_week_index[beginning_week]


        dict_users_list_friends_that_week=dict_dict_weeks_list_friends_each_user[beginning_week]

     
        num_members_this_week=0       
        for user in list_users_with_friends:
            num_members_this_week += is_user_active_that_week(dict_users_membership_periods, user,beginning_week,end_week)
            

        num_members_this_week_method2=len(dict_users_list_friends_that_week)
       

       
        list_unique_members_week=[]
        for  clave_user in dict_users_list_friends_that_week:
            if clave_user not in list_unique_members_week:
                list_unique_members_week.append(clave_user)
            for clave_friend in dict_users_list_friends_that_week[clave_user]:
                if clave_friend not in list_unique_members_week:
                    list_unique_members_week.append(clave_friend)

        print >> file3,week_index,num_members_this_week, num_members_this_week_method2, len(list_unique_members_week)   #(3 diff. methods)


    file3.close()



    ######### checking how many friendships exits between users that were NOT members together, ever
    print "\nchecking how many friendships exits between users that were NOT members together..."    
    list_users_friends_but_not_members_together=[]    
    for clave_user in dict_users_list_friends:

        
        for friend in dict_users_list_friends[clave_user]:

            flag_together=0

            for pair_key_value in sorted_dict_dict_weeks_list_friends_each_user:

                flag_user_member=0
                flag_friend_member=0

                beginning_week=pair_key_value[0]
                end_week=beginning_week+timedelta(days=7)
              
                flag_friend_member = is_user_active_that_week(dict_users_membership_periods,friend, beginning_week, end_week)
                flag_user_member = is_user_active_that_week(dict_users_membership_periods, clave_user, beginning_week, end_week)

                if flag_friend_member ==1 and flag_friend_member ==1 :
                    flag_together=1

            if flag_together ==0:
                if dict_ck_id_label[clave_user] not in list_users_friends_but_not_members_together:
                    list_users_friends_but_not_members_together.append(dict_ck_id_label[clave_user])



    print "   number of users with friends but apparently NOT members at the same time:", len(list_users_friends_but_not_members_together)
    raw_input()
    print  list_users_friends_but_not_members_together

##########################

def is_user_active_that_week(dict_users_membership_periods, user, beginning_week, end_week):

    flag_user_is_member_that_week=0
    for clave in dict_users_membership_periods[user]:
        
        
        start_membership = dict_users_membership_periods[user][clave][0]
        stop_membership = dict_users_membership_periods[user][clave][1]
      
        if (beginning_week >= start_membership )  and (beginning_week <= stop_membership )  :
            flag_user_is_member_that_week=1
            break
        
        if (end_week >= start_membership )  and (end_week <= stop_membership )  :
            flag_user_is_member_that_week=1
            break


   
    return flag_user_is_member_that_week
##################################################
######################################
      
if __name__ == '__main__':
#    if len(sys.argv) > 2:
 #       master_csv = sys.argv[1]
  #      strength_links_csv = sys.argv[2]
       

    main()
   # else:
    #    print "usage: python  whatever.py   path/master.csv  path/strength_links.csv"
 
    
