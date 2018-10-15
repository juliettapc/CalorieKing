
#! /usr/bin/env python

"""
Created by Julia Poncela on March 2013.
Given the datafile from CK with the info for forums, messages, users, 
friendships etc, create the corresponding tables and fields, and populate it.

"""


import sys
import os
from datetime import *
import math
import numpy as np
from scipy import stats
from database import *   #package to handle databases
from histograma_gral_negv_posit import histograma

def main ():

    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 




    
    flag_weighin_history=0
    flag_blog_comments=0
    flag_daily_steps=0
    flag_favorite_blogs=0
    flag_forum_posts=0
    flag_forums=0
    flag_friends=0
    flag_ignore=0
    flag_membership_periods=0
    flag_private_messages=0
    flag_lesson_comments=0
    flag_public_diary=0
    flag_public_group_memberships=0
    flag_homepage_comments=0
    flag_activity_combined=0
    flag_users=1
    flag_get_users_act_prior2009=1
    



    ################  weigh-in history table

    if flag_weighin_history==1:


        db.execute ("DROP TABLE IF EXISTS weigh_in_history")
        db.execute ("""                      
            CREATE TABLE  weigh_in_history  
            (        
             on_day           DATETIME,
             ck_id            CHAR(36),     
             weight           FLOAT,                        
             id               INT(11),
             activity_flag    CHAR(3)                 
            )
          """) 

        file_name3="data_2009_2012_collected_june2013/weighin_history.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
        empty_cases=0
        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            yy=int(list_one_line[0].split("-")[0])
            mm=int(list_one_line[0].split("-")[1])
            dd=int(list_one_line[0].split("-")[2])         
            on_day=datetime(yy,mm,dd)

            ck_id= str(list_one_line[1])   
   
            if list_one_line[2]:  # to check that the string is not empty
                weight=float(list_one_line[2].strip("\n\r").strip())
                           
                activity_flag="WI"

        
                db.execute ("""
                INSERT INTO weigh_in_history (on_day , ck_id, weight, id, activity_flag)
                VALUES (%s, %s, %s, %s, %s)
                """, str(on_day),str(ck_id),str(weight), str(contador),str(activity_flag) )

                print contador, on_day, ck_id, weight,type(weight),len(str(weight)),activity_flag

                contador +=1

            
                

   

    ################  blog comments table

    if flag_blog_comments==1:


        db.execute ("DROP TABLE IF EXISTS blog_comments")
        db.execute ("""                      
            CREATE TABLE  blog_comments  
            (        
               at_time        DATETIME,
               post_date      DATETIME,           
               poster         CHAR(36),
               owner          CHAR(36),
               activity_flag  CHAR(3),
               id             INT(11) 
            )
          """) 

        file_name3="data_2009_2012_collected_june2013/blog_comments.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            yy=int(list_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_one_line[0].split("T")[1].split(":")[2])

            at_time=datetime(yy,mm,dd,hh,mts,ss)


            yy=int(list_one_line[1].split("-")[0])
            mm=int(list_one_line[1].split("-")[1])
            dd=int(list_one_line[1].split("-")[2])

            post_date=datetime(yy,mm,dd)


            poster= str(list_one_line[2])   
            owner= str(list_one_line[3])   
   
            activity_flag="BC"
        
            db.execute ("""
                INSERT INTO blog_comments (at_time , post_date, poster, owner, activity_flag, id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, str(at_time),str(post_date),str(poster), str(owner),str(activity_flag),str(contador) )

            print contador, str(at_time),str(post_date),str(poster), str(owner),str(activity_flag),str(contador)         
            contador +=1






    ################  daily steps table

    if flag_daily_steps==1:


        db.execute ("DROP TABLE IF EXISTS daily_steps")
        db.execute ("""                      
       CREATE TABLE daily_steps
       (
         on_day        DATETIME,
         ck_id         CHAR(36),           
         steps         CHAR(36),        
         id             INT(11)
        
       )
     """) 
       
        file_name3="data_2009_2012_collected_june2013/daily_steps.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            yy=int(list_one_line[0].split("-")[0])
            mm=int(list_one_line[0].split("-")[1])
            dd=int(list_one_line[0].split("-")[2])
         
            on_day=datetime(yy,mm,dd)


            ck_id= str(list_one_line[1])   
            steps= str(list_one_line[2])   
   
        
        
            db.execute ("""
                INSERT INTO daily_steps (on_day , ck_id, steps, id)
                VALUES (%s, %s, %s, %s)
                """, str(on_day),str(ck_id),str(steps),str(contador) )

            print contador,  str(on_day),str(ck_id),str(steps),str(contador)         
            contador +=1





    ################  favorite blogs table

    if flag_favorite_blogs==1:

        db.execute ("DROP TABLE IF EXISTS favorite_blogs")
        db.execute ("""                      
            CREATE TABLE favorite_blogs
            (
             ck_id             CHAR(36),     
             num_blogs         INT(11),
             num_favorites     INT(11),      
             id                INT(11)
        
            )
          """) 
       
        file_name3="data_2009_2012_collected_june2013/favourite_blogs_threads.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file

            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            ck_id= str(list_one_line[0])   
            num_blogs= str(list_one_line[1])   
            num_favorites= str(list_one_line[2])   
        
        
            db.execute ("""
                INSERT INTO favorite_blogs (ck_id , num_blogs, num_favorites, id)
                VALUES (%s, %s, %s, %s)
                """, str(ck_id),str(num_blogs),str(num_favorites),str(contador) )

            print contador,  str(ck_id),str(num_blogs),str(num_favorites),str(contador)         
            contador +=1




    ################  forum posts table

    if flag_forum_posts==1:

        db.execute ("DROP TABLE IF EXISTS forum_posts")  
        db.execute ("""                      
            CREATE TABLE forum_posts
            (
             at_time           DATETIME,
             thread_id         CHAR(36),     
             forum_id          CHAR(36),     
             ck_id             CHAR(36),             
             activity_flag     CHAR(3),        
             id                INT(11)        
            )
          """)

       

        file_name3="data_2009_2012_collected_june2013/forum_posts.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            yy=int(list_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_one_line[0].split("T")[1].split(":")[2])

            at_time=datetime(yy,mm,dd,hh,mts,ss)

          
            thread_id= str(list_one_line[1])   
            forum_id= str(list_one_line[2])   
            ck_id= str(list_one_line[3])   
   
            activity_flag="FP"
        
            db.execute ("""
                INSERT INTO forum_posts (at_time , thread_id, forum_id, ck_id, activity_flag, id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, str(at_time),str(thread_id),str(forum_id), str(ck_id),str(activity_flag),str(contador) )

            print contador, str(at_time),str(thread_id),str(forum_id), str(ck_id),str(activity_flag),str(contador)          
            contador +=1





    ################  forums table

    if flag_forums==1:


        db.execute ("DROP TABLE IF EXISTS forums")
        db.execute ("""                      
            CREATE TABLE forums
            (        
             forum_id          CHAR(36),     
             user_created      CHAR(36),                        
             id                INT(11)        
            )
          """) 

       
        file_name3="data_2009_2012_collected_june2013/forums.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file

            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            forum_id= str(list_one_line[0])   
            user_created= str(list_one_line[1])   
          
        
            db.execute ("""
                INSERT INTO forums (forum_id, user_created, id)
                VALUES (%s, %s, %s)
                """, str(forum_id),str(user_created),str(contador) )

            print contador,  str(forum_id),str(user_created) 
            contador +=1





    ################  friends table

    if flag_friends==1:


        db.execute ("DROP TABLE IF EXISTS friends")
        db.execute ("""                      
            CREATE TABLE friends
            (        
             src          CHAR(36),     
             dest         CHAR(36),                        
             id           INT(11)
        
            )
          """)

       
        file_name3="data_2009_2012_collected_june2013/friends_list.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file

            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            src= str(list_one_line[0])   
            dest= str(list_one_line[1])   
          
        
            db.execute ("""
                INSERT INTO friends (src, dest, id)
                VALUES (%s, %s, %s)
                """, str(src),str(dest),str(contador) )

            print contador,  str(src),str(dest) 
            contador +=1






    ################  ignore table

    if flag_ignore==1:

        db.execute ("DROP TABLE IF EXISTS ignores")
        db.execute ("""                      
            CREATE TABLE ignores
            (        
             src          CHAR(36),     
             dest         CHAR(36),                        
             id           INT(11)        
            )
          """) 
        
       
        file_name3="data_2009_2012_collected_june2013/ignore_list.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file

            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            src= str(list_one_line[0])   
            dest= str(list_one_line[1])   
          
        
            db.execute ("""
                INSERT INTO ignores (src, dest, id)
                VALUES (%s, %s, %s)
                """, str(src),str(dest),str(contador) )

            print contador,  str(src),str(dest) 
            contador +=1




     ################  membership period table

    if flag_membership_periods==1:


        db.execute ("DROP TABLE IF EXISTS membership_periods")
        db.execute ("""                      
            CREATE TABLE membership_periods   
            (
             ck_id         CHAR(36),   
             start_date    DATETIME,          
             end_date      DATETIME, 
             free          CHAR(3),
             payment       CHAR(3),
             voucher       CHAR(3),
             system        CHAR(3),
             plan          CHAR(10),
             free_days     CHAR(10),  
             id            INT(11)

            )
          """) 
       
       

        file_name3="data_2009_2012_collected_june2013/membership_periods.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                

            ck_id= str(list_one_line[0])  

                       
            yy=int(list_one_line[1].split("T")[0].split("-")[0])
            mm=int(list_one_line[1].split("T")[0].split("-")[1])
            dd=int(list_one_line[1].split("T")[0].split("-")[2])

            hh=int(list_one_line[1].split("T")[1].split(":")[0])
            mts=int(list_one_line[1].split("T")[1].split(":")[1])
            ss=int(list_one_line[1].split("T")[1].split(":")[2])

            start_date=datetime(yy,mm,dd,hh,mts,ss)

            free  = str(list_one_line[3])   
            payment = str(list_one_line[4])    
            voucher= str(list_one_line[5])       
            system = str(list_one_line[6])      
            plan = str(list_one_line[7])          
            free_days= str(list_one_line[8])                      

            if list_one_line[2]:  # if there is an ending date
                
                yy=int(list_one_line[2].split("T")[0].split("-")[0])
                mm=int(list_one_line[2].split("T")[0].split("-")[1])
                dd=int(list_one_line[2].split("T")[0].split("-")[2])
                
                hh=int(list_one_line[2].split("T")[1].split(":")[0])
                mts=int(list_one_line[2].split("T")[1].split(":")[1])
                ss=int(list_one_line[2].split("T")[1].split(":")[2])
                
                end_date=datetime(yy,mm,dd,hh,mts,ss)
            

   
        
                db.execute ("""
                INSERT INTO membership_periods (ck_id, start_date, end_date, free, payment, voucher, system,  plan, free_days, id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, str(ck_id), str(start_date), str(end_date), str(free), str(payment), str(voucher), str(system),  str(plan), str(free_days), str(contador)  )

                print contador,  str(ck_id), str(start_date), str(end_date), str(free), str(payment), str(voucher), str(system),  str(plan), str(free_days)          



            else: # if there is no ending date for the period

                db.execute ("""
                INSERT INTO membership_periods (ck_id, start_date,  free, payment, voucher, system,  plan, free_days, id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, str(ck_id), str(start_date),  str(free), str(payment), str(voucher), str(system),  str(plan), str(free_days), str(contador)  )
               

                print contador,  str(ck_id), str(start_date), str(free), str(payment), str(voucher), str(system),  str(plan), str(free_days)  
                

        

            contador +=1




    ################  private messages table

    if flag_private_messages==1:


        db.execute ("DROP TABLE IF EXISTS private_messages")
        db.execute ("""                      
            CREATE TABLE private_messages 
            (        
             at_time           DATETIME,
             src_id            CHAR(36),     
             dest_id           CHAR(36),                        
             activity_flag     CHAR(3),
             id                INT(11)        
            )
         """) 

       
        file_name3="data_2009_2012_collected_june2013/private_messages.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
               



            yy=int(list_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_one_line[0].split("T")[1].split(":")[2])

            at_time=datetime(yy,mm,dd,hh,mts,ss)



            src_id= str(list_one_line[1])   
            dest_id= str(list_one_line[2])   
   
            activity_flag="PM"
        
            db.execute ("""
                INSERT INTO private_messages  (at_time , src_id, dest_id, activity_flag, id)
                VALUES (%s, %s, %s, %s, %s)
                """, str(at_time),str(src_id),str(dest_id),str(activity_flag),str(contador) )

            print contador,  str(at_time),str(src_id),str(dest_id),str(activity_flag)  
            contador +=1





    ################  lesson_comments table

    if flag_lesson_comments==1:

        db.execute ("DROP TABLE IF EXISTS lesson_comments")
        db.execute ("""                      
        CREATE TABLE lesson_comments  
        (
         at_time           DATETIME,
         content_id        CHAR(36),     
         poster_id         CHAR(36),                        
         activity_flag     CHAR(3),
         id                INT(11)

        )
      """) 

   
       
        file_name3="data_2009_2012_collected_june2013/program_lesson_comments.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
               

            yy=int(list_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_one_line[0].split("T")[1].split(":")[2])

            at_time=datetime(yy,mm,dd,hh,mts,ss)



            content_id= str(list_one_line[1])   
            poster_id= str(list_one_line[2])   
   
            activity_flag="LC"
        
            db.execute ("""
                INSERT INTO lesson_comments  (at_time , content_id, poster_id, activity_flag, id)
                VALUES (%s, %s, %s, %s, %s)
                """, str(at_time),str(content_id),str(poster_id),str(activity_flag),str(contador) )

            print contador,  str(at_time),str(content_id),str(poster_id),str(activity_flag)  
            contador +=1




    ################ public_diary table

    if flag_public_diary==1:


        db.execute ("DROP TABLE IF EXISTS public_diary")
        db.execute ("""                      
        CREATE TABLE  public_diary  
        (                
         ck_id            CHAR(36),     
         visibility       CHAR(36),                               
         id               INT(11)
        
        )
      """) 
       
        file_name3="data_2009_2012_collected_june2013/public_diary.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                                  
            ck_id= str(list_one_line[0])   
            visibility= str(list_one_line[1])           
        
            db.execute ("""
                INSERT INTO public_diary (ck_id, visibility, id)
                VALUES (%s, %s,  %s)
                """, str(ck_id),str(visibility),str(contador) )

            print contador,  str(ck_id),str(visibility)         
            contador +=1




    ################  group_membership table

    if flag_public_group_memberships==1:

        
        db.execute ("DROP TABLE IF EXISTS public_group_memberships")

        db.execute ("""                      
        CREATE TABLE public_group_memberships 
        (                 
         forum_id        CHAR(36),     
         ck_id           CHAR(36),                                
         id              INT(11)
        
        )
      """) 


        file_name3="data_2009_2012_collected_june2013/public_group_memberships.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
      

        contador=1
        for line in list_lines_file3:      # read gender info from file

            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
                                       
            forum_id= str(list_one_line[0])   
            ck_id= str(list_one_line[1])   
          
        
            db.execute ("""
                INSERT INTO public_group_memberships (forum_id, ck_id, id)
                VALUES (%s, %s, %s)
                """, str(forum_id),str(ck_id),str(contador) )

            print contador,  str(forum_id),str(ck_id) 
            contador +=1


    ################  homepage_comments table

    if flag_homepage_comments==1:

      
        db.execute ("DROP TABLE IF EXISTS homepage_comments")
        db.execute ("""                      
        CREATE TABLE homepage_comments 
        (
         at_time           DATETIME,
         poster_id         CHAR(36),     
         owner_id          CHAR(36),                 
         id                INT(11),
         activity_flag     CHAR(3)
        
        )
      """) 
       

        file_name3="data_2009_2012_collected_june2013/user_homepage_comments.txt"
        file3=open(file_name3,'r')
        list_lines_file3=file3.readlines()                    
        
        empty_cases=0
        contador=1
        for line in list_lines_file3:      # read gender info from file


            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
             
            yy=int(list_one_line[0].split("T")[0].split("-")[0])
            mm=int(list_one_line[0].split("T")[0].split("-")[1])
            dd=int(list_one_line[0].split("T")[0].split("-")[2])

            hh=int(list_one_line[0].split("T")[1].split(":")[0])
            mts=int(list_one_line[0].split("T")[1].split(":")[1])
            ss=int(list_one_line[0].split("T")[1].split(":")[2])

            at_time=datetime(yy,mm,dd,hh,mts,ss)
           

            poster_id= str(list_one_line[1])   
            owner_id= str(list_one_line[2])   
            activity_flag="HC"

   
           
        
            db.execute ("""
                INSERT INTO homepage_comments (at_time , poster_id, owner_id, id, activity_flag)
                VALUES (%s, %s, %s, %s, %s)
                """, str(at_time),str(poster_id),str(owner_id), str(contador),str(activity_flag) )
            
            print contador, str(at_time),str(poster_id),str(owner_id),str(activity_flag)
            
            contador +=1

            
                

   

    ################  activity_combined table

    if flag_activity_combined==1:
            

        list_dict_total_act=[]

        ### blog comments
        query1="""select * from blog_comments"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}

            dict_user['ck_id']=r1['poster']
            dict_user['activity_date']=r1['at_time']
            dict_user['activity_flag']="BC"
            
            list_dict_total_act.append(dict_user)
            
            print "blog",cont_act
            cont_act+=1




        ### forum posts
        query1="""select * from forum_posts"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}
            
            dict_user['ck_id']=r1['ck_id']
            dict_user['activity_date']=r1['at_time']
            dict_user['activity_flag']="FP"
            
            list_dict_total_act.append(dict_user)
            
            print "forum",cont_act
            cont_act+=1



        ### hompage comments
        query1="""select * from homepage_comments"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}
            
            dict_user['ck_id']=r1['poster_id']
            dict_user['activity_date']=r1['at_time']
            dict_user['activity_flag']="HC"
            
            list_dict_total_act.append(dict_user)
            
            print "hompage",cont_act
            cont_act+=1




        ###  lesson  comments
        query1="""select * from lesson_comments"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}
            
            dict_user['ck_id']=r1['poster_id']
            dict_user['activity_date']=r1['at_time']
            dict_user['activity_flag']="LC"
            
            list_dict_total_act.append(dict_user)
            
            print "lesson",cont_act
            cont_act+=1



        ### private_messages
        query1="""select * from private_messages"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}
            
            dict_user['ck_id']=r1['src_id']
            dict_user['activity_date']=r1['at_time']
            dict_user['activity_flag']="PM"
            
            list_dict_total_act.append(dict_user)
            
            print "message",cont_act
            cont_act+=1



        ### weigh in
        query1="""select * from weigh_in_history"""    
        result1 = db.query(query1) 

        cont_act=1
        for r1 in result1:  #list of dict.
            dict_user={}
            
            dict_user['ck_id']=r1['ck_id']
            dict_user['activity_date']=r1['on_day']
            dict_user['activity_flag']="WI"
            
            list_dict_total_act.append(dict_user)
            
            print "wi",cont_act
            cont_act+=1

        print  "tot activity combined:", len(list_dict_total_act)

       

        db.execute ("DROP TABLE IF EXISTS activity_combined")
        db.execute ("""                      
        CREATE TABLE activity_combined 
        (
         activity_date     DATETIME,
         ck_id             CHAR(36),                                
         activity_flag     CHAR(3),
         id                INT(11)        
        )
         """) 
       

        contador=1
        for dicc in list_dict_total_act:   # list of dicts
           
            activity_date= dicc['activity_date']
            ck_id= dicc['ck_id']
            activity_flag= dicc['activity_flag']


            db.execute ("""
                INSERT INTO activity_combined (activity_date , ck_id, activity_flag, id)
                VALUES (%s, %s, %s, %s)
                """, str(activity_date),str(ck_id),str(activity_flag), str(contador) )
            
            print contador, str(activity_date),str(ck_id),str(activity_flag)
            
            contador+=1

            



   ############# find the list of users with activity prior to 2009
    if  flag_get_users_act_prior2009==1:

        list_day_diff=[]        
        list_users_act_prior2009=[]
        first_day=datetime(2009,01,01)
        
        print "querying the db..."
        query1="""select * from activity_combined order by activity_date"""    
        result1 = db.query(query1) 
        
        
        for r1 in result1:  # list of dicts
            ck_id=r1['ck_id']
            date_act=r1['activity_date']
            
            
            if date_act < first_day:
                if ck_id not in list_users_act_prior2009:
                    list_users_act_prior2009.append(ck_id)
                    list_day_diff.append((date_act - first_day).days)
                print date_act, first_day, ck_id
           
       
        print "# users with activity prior to 2009:", len(list_users_act_prior2009)

        histograma(list_day_diff,"./histogr_diff_days_prior2009.dat")
      


    ################## users table
    if flag_users==1:

        db.execute ("DROP TABLE IF EXISTS users")
        db.execute ("""                      
           CREATE TABLE  users
           (        
            ck_id                   CHAR(36), 
            join_date               DATETIME,
            initial_weight          FLOAT,         
            most_recent_weight      FLOAT,                        
            height                  INT(11),       
            age                     INT(11),
            state                   CHAR(36), 
            is_staff                CHAR(36), 
            internal_CK_account     CHAR(36), 
            id                      INT(11),
            total_balance           CHAR(10),  
            gender                  CHAR(10),                     
            act_prior2009       CHAR(36)                     
        
           )
         """) # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




        file_name2="data_2009_2012_collected_june2013/users.txt"
        file2=open(file_name2,'r')
        list_lines_file2=file2.readlines()                    
        
        contador=0
        dict_of_dicts={}
        dict_id_ckid={}
        dict_user_internal_account={}
        for line in list_lines_file2:      # read gender info from file
            contador+=1
            dict_one_user={}
            
            list_one_line=line.strip("\n\r").split(",")  #remove \n\r together! (this is how the jump is coded in certain op. systems)
            

            ck_id= str(list_one_line[0])                       

            yy=int(list_one_line[1].split("T")[0].split("-")[0])
            mm=int(list_one_line[1].split("T")[0].split("-")[1])
            dd=int(list_one_line[1].split("T")[0].split("-")[2])

            hh=int(list_one_line[1].split("T")[1].split(":")[0])
            mts=int(list_one_line[1].split("T")[1].split(":")[1])
            ss=int(list_one_line[1].split("T")[1].split(":")[2])

            join_date=datetime(yy,mm,dd,hh,mts,ss)


            initial_weight=float(list_one_line[2])
            most_recent_weight=float(list_one_line[3])
            height=float(list_one_line[4])
            try:
                age=int(list_one_line[5])
            except ValueError:
                age=0
               
            state=str(list_one_line[6])                
            is_staff=str(list_one_line[7])
            gender=str(list_one_line[8])  # this is how some op. sys. code the jump of line!
            

            total_balance=str(list_one_line[9])  # either the user paid something or was totally free... 
            
            dict_one_user['ck_id']=ck_id
            dict_one_user['join_date']=join_date
            dict_one_user['initial_weight']=initial_weight
            dict_one_user['most_recent_weight']=most_recent_weight
            dict_one_user['height']=height
            dict_one_user['age']=age
            dict_one_user['state']=state
            dict_one_user['is_staff']=is_staff
            dict_one_user['gender']=gender
            dict_one_user['total_balance']=total_balance
            dict_one_user['id']=contador

            dict_one_user['act_prior2009']="NO"
            if ck_id in list_users_act_prior2009:
                dict_one_user['act_prior2009']="YES"
           

            dict_user_internal_account[ck_id]="NO"

            dict_id_ckid[contador]=ck_id

            dict_of_dicts[ck_id]=dict_one_user


        print  "number of users in the user.txt file:",len(dict_of_dicts), "\n"
        print "  populating the users table..."
   



        #### i get the info about users that actually correspond to an internal CK account

        file = open("./data_2009_2012_collected_june2013/CK_internal_accounts_list.dat", "r")
        list_data= file.readlines()
        
        for data in list_data:
            ck_id=data.strip("\r\n")           
            dict_user_internal_account[ck_id]="YES"  # the by-default value isbeen set to NO
       


        #### i populate the users table

        for user_id in range(len(dict_of_dicts)):
            user_id+=1

            ck_id=dict_id_ckid[user_id]
           
            join_date=dict_of_dicts[ck_id]['join_date']
            initial_weight=dict_of_dicts[ck_id]['initial_weight']
            most_recent_weight=dict_of_dicts[ck_id]['most_recent_weight']
            height=dict_of_dicts[ck_id]['height']
            age=dict_of_dicts[ck_id]['age']
            state=dict_of_dicts[ck_id]['state']
            is_staff=dict_of_dicts[ck_id]['is_staff']
            gender=dict_of_dicts[ck_id]['gender']
            total_balance=dict_of_dicts[ck_id]['total_balance']
            act_prior2009=dict_of_dicts[ck_id]['act_prior2009']
            internal_account=dict_user_internal_account[ck_id]
   
            db.execute ("""
                INSERT INTO users (ck_id,  join_date, initial_weight, most_recent_weight, height, age, state, is_staff, internal_CK_account, id, gender, total_balance, act_prior2009)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, str(ck_id),str(join_date),str(initial_weight), str(most_recent_weight),str(height),str(age), str(state),str(is_staff),str(internal_account), str(user_id), str(gender),str(total_balance), str(act_prior2009) )


      
            print user_id,ck_id, join_date,initial_weight,most_recent_weight, height,age,state, is_staff, internal_account, gender,total_balance

           



###########################################
          
if __name__== "__main__":

    main()
         
##############################################
