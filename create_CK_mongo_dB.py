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
import datetime
from database import *   #package to handle databases
import pymongo
from pymongo import MongoClient
from datetime import *


def main():


    client = MongoClient() 
    db = client['CalorieKing_mongo_db']    # or:  db = client.CalorieKing_mongo_db
    db.users.ensure_index('ck_id')  # i index the field "ck_id"  of the collection users so the queries will run faster
   



    flag_run_users=1
    flag_run_paying_info=0
    flag_run_daily_steps=0
    flag_run_blog_comments=0
    flag_run_forum_post=0
    flag_run_friends=0
    flag_run_private_messages=0
    flag_run_lesson_comments=0
    flag_run_public_diary=0   # run again!!! (to change field name)
    flag_run_homepage_comments=0
    flag_run_weigh_in_history=1
    flag_run_ignores=0
    flag_run_group_memberships=0
    flag_run_memberhip_periods=0
    flag_run_forums=0
    flag_run_favorites=0





    ############## i add a new collection: users
    if flag_run_users==1:

        db.drop_collection("users")   # if i dont and it already exists, then it will just add extra documents for the same users!
        users = db.users   # i create a collection (eq. to a table in mysql)

        file_name1="./data_2009_2010_generated_in2013_includes_gender_paying/users.txt"
        file1=open(file_name1,'r')
        list_lines_file=file1.readlines()    # if i want to exclude the first line, [1:]
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
            
            dict_one_user={}
            
            ck_id=list_elements_one_line[0]
          
            yy=int(list_elements_one_line[1].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[1].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[1].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[1].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[1].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[1].split("T")[1].split(":")[2])

            join_date=datetime(yy,mm,dd,hh,mts,ss)


            initial_w=list_elements_one_line[2]
            final_w=list_elements_one_line[3]
            height=list_elements_one_line[4]
            age=list_elements_one_line[5]
            state=list_elements_one_line[6]
            is_staff=list_elements_one_line[7]
            gender=list_elements_one_line[8]
            
            print ck_id,join_date,initial_w,final_w,height,age,state,is_staff,gender
            
            dict_one_user["ck_id"]=ck_id
            dict_one_user["join_date"]=join_date
            dict_one_user["initial_w"]=initial_w
            dict_one_user["final_w"]=final_w
            dict_one_user["height"]=height
            dict_one_user["age"]=age
            dict_one_user["state"]=state
            dict_one_user["is_staff"]=is_staff
            dict_one_user["gender"]=gender
            dict_one_user["i_bmi"]=float(initial_w)*703./(float(height)*float(height))
            
            
            users.insert(dict_one_user)    # insert document into mongodb


    ############# i add the paying info to the existing users collection
    if  flag_run_paying_info==1:
        file_name2="./data_2009_2010_generated_in2013_includes_gender_paying/paid.txt"
        file2=open(file_name2,'r')
        list_lines_file=file2.readlines()    # if i want to exclude the first line, i would add [1:]

        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
            
            ck_id=list_elements_one_line[0]
            paying_info=list_elements_one_line[1]
            print cont, ck_id, paying_info
            
            
            for doc in db.users.find({"ck_id": ck_id}) :  # i find the correct document
                doc['paying_info'] = paying_info   # i modify the document
                db.users.save(doc)    # then i save the document

        
       
       #or: db.users.update({"ck_id": ck_id}, {"$set": {"paying_info": paying_info}})  (no for loop needed)

            cont += 1




    ############## i add a new collection: daily_steps
    if  flag_run_daily_steps==1:

        db.drop_collection("daily_steps")   # if i dont and it already exists, then it will just add extra documents for the same users!
        daily_steps = db.daily_steps


        file_name3="./data_2009_2010_generated_in2013_includes_gender_paying/daily_steps.txt"
        file3=open(file_name3,'r')
        list_lines_file=file3.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  

            print cont , "daily steps"
            dict_steps={}

            on_day_list_str=list_elements_one_line[0].split("-")
 
            yy=int(on_day_list_str[0])
            mm=int(on_day_list_str[1])
            dd=int(on_day_list_str[2])
            on_day=datetime(yy,mm,dd)


            ck_id=list_elements_one_line[1]
            steps=list_elements_one_line[2]

            dict_steps['ck_id']= ck_id
            dict_steps['on_day']= on_day
            dict_steps['steps']= steps

            daily_steps.insert(dict_steps)    
            cont +=1



    ############## i add a new collection: blog_comments
    if  flag_run_blog_comments==1:

        db.drop_collection("blog_comments")  
        blog_comments = db.blog_comments


        file_name4="./data_2009_2010_generated_in2013_includes_gender_paying/blog_comments.txt"
        file4=open(file_name4,'r')
        list_lines_file=file4.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  


          

            yy=int(list_elements_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[0].split("T")[1].split(":")[2])

            comment_date=datetime(yy,mm,dd,hh,mts,ss)


            yy=int(list_elements_one_line[1].split("-")[0])
            mm=int(list_elements_one_line[1].split("-")[1])
            dd=int(list_elements_one_line[1].split("-")[2])
        
            blog_entry_date=datetime(yy,mm,dd)   # this is typically earlier



            poster=list_elements_one_line[2]
            owner=list_elements_one_line[3]

            dict_blog_comment={}
            dict_blog_comment['comment_date']=comment_date
            dict_blog_comment['blog_entry_date']=blog_entry_date
            dict_blog_comment['poster']=poster
            dict_blog_comment['owner']=owner

            print cont , "blog comment"
            blog_comments.insert(dict_blog_comment)
            cont +=1





    ############## i add a new collection: forum_posts
    if flag_run_forum_post==1:

        db.drop_collection("forum_posts")   
        forum_posts = db.forum_posts


        file_name5="./data_2009_2010_generated_in2013_includes_gender_paying/forum_posts.txt"
        file5=open(file_name5,'r')
        list_lines_file=file5.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  

          
            yy=int(list_elements_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[0].split("T")[1].split(":")[2])           


            at_time=datetime(yy,mm,dd,hh,mts,ss)



            thread_id=list_elements_one_line[1]
            forum_id=list_elements_one_line[2]
            ck_id=list_elements_one_line[3]

            dict_forum_posts={}
            dict_forum_posts['at_time']=at_time
            dict_forum_posts['thread_id']=thread_id
            dict_forum_posts['forum_id']=forum_id
            dict_forum_posts['ck_id']=ck_id

            print cont , "forum post"
            forum_posts.insert(dict_forum_posts)
            cont +=1

            



    ############## i add a new collection: friends
    if flag_run_friends==1:

        db.drop_collection("friends")   
        friends = db.friends


        file_name6="./data_2009_2010_generated_in2013_includes_gender_paying/friends_list.txt"
        file6=open(file_name6,'r')
        list_lines_file=file6.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
            src=list_elements_one_line[0]
            dest=list_elements_one_line[1]

            dict_friends={}
            dict_friends['src']=src
            dict_friends['dest']=dest


            print cont , "friendships"


           # if src == dest:   ### remember that there are many cases like this!!!!
            #    raw_input()
            friends.insert(dict_friends)
            cont +=1




    ############## i add a new collection: private_messages
    if flag_run_private_messages==1:

        db.drop_collection("private_messages")   
        private_messages = db.private_messages


        file_name7="./data_2009_2010_generated_in2013_includes_gender_paying/private_messages.txt"
        file7=open(file_name7,'r')
        list_lines_file=file7.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
           
            yy=int(list_elements_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[0].split("T")[1].split(":")[2])           


            at_time=datetime(yy,mm,dd,hh,mts,ss)



            src_id=list_elements_one_line[1]
            dest_id=list_elements_one_line[2]

            dict_private_messages={}
            dict_private_messages['at_time']= at_time
            dict_private_messages['src_id']=src_id
            dict_private_messages['dest_id']=dest_id


            print cont , "private messages"


          
            private_messages.insert(dict_private_messages)
            cont +=1




    ############## i add a new collection: lesson_comments
    if flag_run_lesson_comments==1:

        db.drop_collection("lesson_comments")   
        lesson_comments = db.lesson_comments


        file_name8="./data_2009_2010_generated_in2013_includes_gender_paying/program_lesson_comments.txt"
        file8=open(file_name8,'r')
        list_lines_file=file8.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  

            yy=int(list_elements_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[0].split("T")[1].split(":")[2])           


            at_time=datetime(yy,mm,dd,hh,mts,ss)

            
            content_id=list_elements_one_line[1]
            poster_id=list_elements_one_line[2]

            dict_lesson_comments={}
            dict_lesson_comments['at_time']= at_time
            dict_lesson_comments['content_id']=content_id
            dict_lesson_comments['poster_id']=poster_id


            print cont , "lesson comments"


           
            lesson_comments.insert(dict_lesson_comments)
            cont +=1



    ############# i add the diary info to the existing users collection
    if  flag_run_public_diary==1:
        file_name9="./data_2009_2010_generated_in2013_includes_gender_paying/public_diary.txt"
        file9=open(file_name9,'r')
        list_lines_file=file9.readlines()    # if i want to exclude the first line, i would add [1:]

        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
            
            ck_id=list_elements_one_line[0]
            visibility=list_elements_one_line[1]
           
            print cont, "public diary"
            
            for doc in db.users.find({"ck_id": ck_id}) :  # i find the correct document
                doc['diary_visibility'] = visibility   # i modify the document
                db.users.save(doc)    # then i save the document

        
       
       #or: db.users.update({"ck_id": ck_id}, {"$set": {"paying_info": paying_info}})  (no for loop needed)

            cont += 1





    ############## i add a new collection: homepage_comments
    if flag_run_homepage_comments==1:

        db.drop_collection("homepage_comments")   
        homepage_comments = db.homepage_comments


        file_name10="./data_2009_2010_generated_in2013_includes_gender_paying/user_homepage_comments.txt"
        file10=open(file_name10,'r')
        list_lines_file=file10.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  

            yy=int(list_elements_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_elements_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_elements_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_elements_one_line[0].split("T")[1].split(":")[2])           


            at_time=datetime(yy,mm,dd,hh,mts,ss)



            poster_id=list_elements_one_line[1]
            owner_id=list_elements_one_line[2]

            dict_homepage_comments={}
            dict_homepage_comments['at_time']= at_time
            dict_homepage_comments['poster_id']=poster_id
            dict_homepage_comments['owner_id']=owner_id


            print cont , "homepage_comments"

           
            homepage_comments.insert(dict_homepage_comments)
            cont +=1






    ############## i add a new collection: weigh_in_history  (and i also add a field to the users collection!)
    if  flag_run_weigh_in_history==1:

        db.drop_collection("weigh_in_history")   
        weigh_in_history = db.weigh_in_history


        file_name11="./data_2009_2010_generated_in2013_includes_gender_paying/weighin_history.txt"
        file11=open(file_name11,'r')
        list_lines_file=file11.readlines()    # if i want to exclude the first line, [1:]
        list_ck_id=[]
        dict_user_time_series={}
        cont=1
        for line in list_lines_file:  #the entries of this file are not always chronological nor order by user!! 
            list_elements_one_line=line.strip("\n\r").split(",")  
  
          

            yy=int(list_elements_one_line[0].split("-")[0])
            mm=int(list_elements_one_line[0].split("-")[1])
            dd=int(list_elements_one_line[0].split("-")[2])

           
            on_day=datetime(yy,mm,dd)



            ck_id, weight =list_elements_one_line   # unpacking, bitch!
           


            if ck_id not in list_ck_id:
                list_ck_id.append(ck_id)
                dict_user_time_series[ck_id]=[]
          
            dict_user_time_series[ck_id].append( (on_day,weight) )  #list of tuples  NOT SORTED chronologically!!!
          

            dict_weigh_in_history={}
            dict_weigh_in_history['on_day']= on_day
            dict_weigh_in_history['ck_id']=ck_id
            dict_weigh_in_history['weight']=weight


            print cont , "weigh_in_history", type(on_day)

           
            weigh_in_history.insert(dict_weigh_in_history)
            cont +=1


        for ck_key in dict_user_time_series:
            print ck_key, dict_user_time_series[ck_key]
            
            dict_user_time_series[ck_key].sort(key=lambda tupla: tupla[0])   #to sort by the first element of each tuple   # or sorted(unsorted, key = lambda element : element[1])
            
            print dict_user_time_series[ck_key]
            if ck_id =="6bdb078b-5f64-48a7-966f-ea2dd948f581":
                    raw_input()
            
            
            
            
            for doc in db.users.find({"ck_id": ck_id}) :  # i find the correct document
                doc['weigh_in_time_series'] = dict_user_time_series[ck_key]   # i modify the document
                db.users.save(doc)    # then i save the document
                


   



    ############## i add a new collection: ignores
    if flag_run_ignores==1:

        db.drop_collection("ignores")   
        ignores = db.ignores


        file_name12="./data_2009_2010_generated_in2013_includes_gender_paying/ignore_list.txt"
        file12=open(file_name12,'r')
        list_lines_file=file12.readlines()    # if i want to exclude the first line, [1:]
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
            src=list_elements_one_line[0]
            dest=list_elements_one_line[1]

            dict_ignore={}
            dict_ignore['src']=src
            dict_ignore['dest']=dest


            print cont , "ignores"

          
            ignores.insert(dict_ignore)
            cont +=1



    ############## i add a new collection: group_memberships
    if flag_run_group_memberships==1:
        db.drop_collection("group_memberships")   
        group_memberships = db.group_memberships


        file_name13="./data_2009_2010_generated_in2013_includes_gender_paying/public_group_memberships.txt"
        file13=open(file_name13,'r')
        list_lines_file=file13.readlines()    
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
            forum_id=list_elements_one_line[0]
            ck_id=list_elements_one_line[1]

            dict_group_memberships={}
            dict_group_memberships['forum_id']=forum_id
            dict_group_memberships['ck_id']=ck_id


            print cont , "group_memberships"
          
            group_memberships.insert(dict_group_memberships)
            cont +=1



    ############## i add a new collection: forums
    if  flag_run_forums==1:

        db.drop_collection("forums")   
        forums = db.forums


        file_name15="./data_2009_2010_generated_in2013_includes_gender_paying/forums.txt"
        file15=open(file_name15,'r')
        list_lines_file=file15.readlines()    
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
           
            forum_id=list_elements_one_line[0]
            type_forum=list_elements_one_line[1]

            dict_forums={}
            dict_forums['forum_id']= forum_id
            dict_forums['type_forum']=type_forum
           

            print cont , "forums"


          
            forums.insert(dict_forums)
            cont +=1


  



    ############## i add a new collection: favorites
    if  flag_run_favorites==1:


        list_ck_id=[]
        db.drop_collection("favorites")   
        favorites = db.favorites


        file_name16="./data_2009_2010_generated_in2013_includes_gender_paying/favourite_blogs_threads.txt"
        file16=open(file_name16,'r')
        list_lines_file=file16.readlines()    
        cont=1
        for line in list_lines_file:     
            list_elements_one_line=line.strip("\n\r").split(",")  
  
           
            ck_id=list_elements_one_line[0]
            num_favorite_blogs=list_elements_one_line[1]
            num_favorite_forum_threads=list_elements_one_line[2]
           
            dict_favorites={}
            dict_favorites['ck_id']= ck_id
            dict_favorites['num_favorite_blogs']=num_favorite_blogs
            dict_favorites['num_favorite_forum_threads']=num_favorite_forum_threads
           

            print cont , "favorite"

     #       if ck_id not in list_ck_id:
      #          list_ck_id.append(ck_id)
          
            favorites.insert(dict_favorites)
            cont +=1





 
  #  for ck_id in list_ck_id:
   #     for doc in db.users.find({"ck_id": ck_id}) :  # i find the correct document
    #        print ck_id

##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename = sys.argv[1]
   
        main()#filename)
    #else:
     #   print "Usage: python script.py path/filename"
