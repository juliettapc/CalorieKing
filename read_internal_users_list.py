#!/usr/bin/env python


'''
Create segments of the original weigh time series, only including the first
membership periods, defined as the membership_period form the database table
or if two are separated by less than 30days. These segments will be used 
to study the evolution of the weight in the "initiation" part of their stay in the system.

Created by Julia Poncela, June  2013

'''

import networkx as nx   # some packages i will probably need
import numpy
import random
import csv
import sys
import os
import itertools
from datetime import *
from database import *   #package to handle databases


def main():



    database = "CK_users2009_2012_collected_june2013"  
    server="tarraco.chem-eng.northwestern.edu"
    user="julia" 
    passwd="tiyp,julia"
    db= Connection(server, database, user, passwd) 



    file = open("./data_2009_2012_collected_june2013/CK_internal-accounts-list.dat", "r")
    list_data= file.readlines()

    list_ck_id=[]
    for data in list_data:
        ck_id=data.strip("\r\n")
        if ck_id not in list_ck_id:
            list_ck_id.append(ck_id)

    list_num_wi=[]
    for ck_id in list_ck_id:
        query1="""select * from weigh_in_history where ck_id='""" +str(ck_id) +"""'"""    
        result1 = db.query(query1) 
        print ck_id, len(result1)        
        list_num_wi.append(len(result1))

    print max(list_num_wi)


    query1="""select * from users"""    
    result1 = db.query(query1) 
    list_users=[]
    for r1 in result1:
        ck_id=r1['ck_id']
        list_users.append(ck_id)

    print  "intersection:",len(list(set(list_ck_id) & set(list_users))), len(list_ck_id),len(list_users)

##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    filename = sys.argv[1]
   
    main()
    #else:
     #   print "Usage: python script.py path/filename"
