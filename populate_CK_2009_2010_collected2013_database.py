
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


def main ():

    database = "CK_users2009_2010_collected2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"

    db= Connection(server, database, user, passwd) 




    file_name="data_2009_2010_generated_in2013_includes_gender_paying/paid.txt"
    file=open(file_name,'r')
    list_lines_file=file.readlines()        
        
    dict_user_paying={}
            
    for line in list_lines_file:     # read paying info from file
        
        list_one_line=line.split(",")   

        ck_id=  str(list_one_line[0])
        paying_info=list_one_line[1].strip("\r\n")  # this is how some op. sys. code the jump of line!

        dict_user_paying[ck_id]=paying_info
   

    print  len(dict_user_paying)


    file_name2="data_2009_2010_generated_in2013_includes_gender_paying/users.txt"
    file2=open(file_name2,'r')
    list_lines_file2=file2.readlines()                    

    dict_of_dicts={}
            
    for line in list_lines_file2:      # read gender info from file

        dict_one_user={}
        
        list_one_line=line.split(",")   

        ck_id= str(list_one_line[0])                       
        join_date=list_one_line[1]
        initial_weight=float(list_one_line[2])
        most_recent_weight=float(list_one_line[3])
        height=float(list_one_line[4])
        try:
            age=int(list_one_line[5])
        except ValueError:
            age="0"
        state=str(list_one_line[6])                
        is_staff=str(list_one_line[7])
        gender=str(list_one_line[8].strip("\r\n"))  # this is how some op. sys. code the jump of line!
        

        dict_one_user['ck_id']=ck_id
        dict_one_user['join_date']=join_date
        dict_one_user['initial_weight']=initial_weight
        dict_one_user['most_recent_weight']=most_recent_weight
        dict_one_user['height']=height
        dict_one_user['age']=age
        dict_one_user['state']=state
        dict_one_user['is_staff']=is_staff
        dict_one_user['gender']=gender
        dict_one_user['paying']=dict_user_paying[ck_id]



        dict_of_dicts[ck_id]=dict_one_user


    print  len(dict_of_dicts)

    num_outside_users=0
    for llave in dict_user_paying:
        try:
            a=dict_of_dicts[llave]
        except KeyError:
         #   print llave
            num_outside_users+=1


    print  num_outside_users   # i have 51007 entries in the pay file, 47110 match the users table, 3897 dont
    
   
    contador=1
    for clave in dict_of_dicts:
        ck_id=clave
        
        join_date=dict_of_dicts[clave]['join_date']
        initial_weight=dict_of_dicts[clave]['initial_weight']
        most_recent_weight=dict_of_dicts[clave]['most_recent_weight']
        height=dict_of_dicts[clave]['height']
        age=dict_of_dicts[clave]['age']
        state=dict_of_dicts[clave]['state']
        is_staff=dict_of_dicts[clave]['is_staff']
        gender=dict_of_dicts[clave]['gender']
        paying=dict_of_dicts[clave]['paying']

   
        db.execute ("""
        INSERT INTO users (ck_id,  join_date, initial_weight, most_recent_weight, height, age, state, is_staff, id, gender, paying)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, str(ck_id),str(join_date),str(initial_weight), str(most_recent_weight),str(height),str(age), str(state),str(is_staff),str(contador), str(gender),str(paying) )

## note: to get the index (of the point) for the days, it is i+1, because i corresponds to the serie of freq. (also, remember that it starts ato 0 index)


      
        print ck_id, join_date,initial_weight,most_recent_weight, height,age,state, is_staff, gender,paying

















    exit()

# I  create all tables



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
         id                      INT(11),
         gender                  CHAR(10), 
         paying                  CHAR(10)                   
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 

    db.execute ("""                      
        CREATE TABLE  weigh_in_history  
        (        
         on_day           DATETIME,
         ck_id            CHAR(36),     
         weight           FLOAT,                        
         id               INT(11),
         activity_flag    CHAR(3)
         
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE public_groups  
        (               
         forum_id            CHAR(36),     
         ck_id               CHAR(36),                                
         id                  INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 

    db.execute ("""                      
        CREATE TABLE  public_diary  
        (                
         ck_id            CHAR(36),     
         visibility       CHAR(36),                               
         id               INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE private_messages 
        (        
         at_time           DATETIME,
         src_id            CHAR(36),     
         dest_id           CHAR(36),                        
         activity_flag     CHAR(3),
         id                INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE membership_periods   
        (
         ck_id         CHAR(36),   
         on_day        DATETIME,          
         type          CHAR(36),                                
         id                INT(11)

        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE lesson_comments  
        (
         at_time           DATETIME,
         content_id         CHAR(36),     
         poster_id          CHAR(36),                        
         activity_flag     CHAR(3),
         id                INT(11)

        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE ignores
        (        
         src          CHAR(36),     
         dest         CHAR(36),                        
         id                INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 


    db.execute ("""                      
        CREATE TABLE homepage_comment 
        (
         at_time           DATETIME,
         poster_id         CHAR(36),     
         owner_id          CHAR(36),                 
         id                INT(11),
         activity_flag     CHAR(3)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




   



    db.execute ("""                      
        CREATE TABLE friends
        (        
         src          CHAR(36),     
         dest         CHAR(36),                        
         id                INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 




    db.execute ("""                      
        CREATE TABLE forums
        (        
         forum_id          CHAR(36),     
         user_created      CHAR(36),                        
         id                INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 



        
#    i create a new table in an existing DB  
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
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 





    db.execute ("""                      
        CREATE TABLE favorite_blogs
        (
         ck_id             CHAR(36),     
         num_blogs         INT(11),
         num_favorites     INT(11),      
         id                INT(11)
        
        )
      #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 





   # db.execute ("DROP TABLE IF EXISTS daily_steps")
  #  db.execute ("""                      
   #    CREATE TABLE daily_steps
    #   (
     #    on_day        DATETIME,
      #   ck_id         CHAR(36),           
       #  steps         CHAR(36),        
        # id             INT(11)
        
       #)
     #""") 

# falta ACTIVITY_COMBINED  !!!



   # try:
    #    db.execute ("DROP TABLE IF EXISTS blog_comments")  #i remove the old table 
        
    #i create a new table in an existing DB  
     #   db.execute ("""                      
      #  CREATE TABLE blog_comments
       # (
        # at_time        DATETIME,
         #post_date      DATE,           
         #poster         CHAR(36),
         #owner          CHAR(36),
         #activity_flag  CHAR(3),
         #id             INT(11)
        
        #)
        #""") # if i use triple quotation marks, i can have jumps of line no problem, but not with single ones 



 


#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
