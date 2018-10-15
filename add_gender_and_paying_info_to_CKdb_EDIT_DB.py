
#! /usr/bin/env python

"""
Created by Julia Poncela on March 2013.

Code to add the gender, and paying info to the existing Users table 
of the CK db, reading from a datafile.



"""


import sys
import os
from datetime import *
import math
import numpy as np
from scipy import stats
from database import *   #package to handle databases


def main ():



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd)   # connect to the db





    file_name="data_2009_2010_generated_in2013_includes_sex_paying/paid.txt"
    file=open(file_name,'r')
    list_lines_file=file.readlines()        
        

    dict_user_paying={}
            
    for line in list_lines_file:     # read paying info from file
        
        list_one_line=line.split(",")   

      #  print list_one_line

        ck_id=  str(list_one_line[0])
      
        paying_info=list_one_line[1].strip("\r\n")  # \r\n  (both together) are the return for Mac op system!
      
        dict_user_paying[ck_id]=paying_info

      



       

    file_name2="data_2009_2010_generated_in2013_includes_sex_paying/users.txt"
    file2=open(file_name2,'r')
    list_lines_file2=file2.readlines()                    

    dict_user_gender={}
            
    for line in list_lines_file2:      # read gender info from file
        
        list_one_line=line.split(",")   

        ck_id= str(list_one_line[0])
        gender=list_one_line[8].strip("\r\n")  # \r\n  (both together) are the return for Mac op system!

        dict_user_gender[ck_id]=gender

     #   print ck_id, gender




    print "paying dict:",len(dict_user_paying),"gender dict:",len(dict_user_gender)

#/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_all_users/master_csv.csv




 

  #  query1="""ALTER TABLE users ADD gender CHAR(10)"""     # i just need to do this once
   # db.execute (query1) 

    #query2="""ALTER TABLE users ADD paying CHAR(10)""" 
    #db.execute (query2) 

    cont=1
    for clave in dict_user_gender:
        ck_id=clave
        gender=dict_user_gender[clave]
        paying_info=dict_user_paying[ck_id]

        print cont
      #  print ck_id,gender, type(gender), len(gender), paying_info, type(paying_info), len(paying_info)


        query3=""" UPDATE users SET gender='%s'  WHERE ck_id='%s'  """   %   (gender, ck_id)
        try:
            db.execute (query3) 
        except KeyError : 
            print ck_id,"doenst exist (gender dict)"



        query4=""" UPDATE users SET paying='%s'  WHERE ck_id='%s'  """  % (paying_info, ck_id)
        try:
            db.execute (query4) 
        except KeyError : 
            print ck_id,"doenst exist (gender dict)"

    


        cont+=1





    


#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
