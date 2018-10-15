#! /usr/bin/env python
"""
user_activity_timeseries.py

Created by Rufaro Mukogo on 2011-01-11.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

Produces timeseries data for user activity over time.

"""
from database import *
import networkx as nx
from copy import copy
import numpy
import os
import sys

class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class Users_activity(object):
    
    def __init__(self):
        self.db = DBConnection()
        self.year = "'2009-"
        self.quarters = [("'2009-01-01'", "'2009-03-31'"), ("'2009-04-01'", "'2009-06-30'"),\
                          ("'2009-07-01'", "'2009-09-30'"), ("'2009-10-01'", "'2009-12-31'")]
        self.months = [("01-01'", "01-31'"), ("02-01'","02-28'"), ("03-01'", "03-31'"),\
                       ("04-01'", "04-30'"), ("05-01'","05-31'"), ("06-01'","06-30'"), ("07-01'", "07-31'"),\
                       ("08-01'","08-31'"), ("09-01'", "09-30'"), ("10-01'", "10-31'"), ("11-01'", "11-30'"),\
                       ("12-01'","12-31'")]
        self.month_ends = (31,28,31,30,31,30,31,31,30,31,30,31)
        
    def _assemble_uids_query(self, duration=None):
        
        """ 
        query to extract the set of unique uids over the specified time period, 
        this corresponds to all active users in that window
            
        """ 
        queries = []
        
        master = self.master
        
        for q in duration:            
            
            if duration == self.months:
                v = (self.year+q[0], self.year+q[1])
            else:
                v = q
            
            q_string = master + """WHERE activity_date >= %s AND activity_date<= %s""" %(v[0],v[1])
            queries.append(q_string)
        print queries
        return queries
    
    def _assemble_data_query(self, uid_list):
        
        """ 
        query to extract information from the activity_time_log 
        
        """ 
        queries = []
        
        for uid in uid_list:
            for item in uid: 
                q_string ="""Select * from activity_time_log where ck_id ='%s'"""%item
                queries.append(q_string)
        #print "queries", queries 
        return queries
    
    def extract_active_uids(self, duration):
        
        self.master ="""Select distinct(ck_id) from activity_combined """
        master = self.master
        results_uids = []
        
        if not duration:
            queries_to_run = [self.master]  
        elif duration == "quarters":
            queries_to_run = self._assemble_uids_query(self.quarters)
        elif duration == "months":
            queries_to_run = self._assemble_uids_query(self.months)
       
        for query in queries_to_run:
            
            result = self.db.query(query)

            interim_results = [] 
            
            for r in result:
                interim_results.append(r['ck_id'])
        
            results_uids.append(map(str,interim_results))
        
        return results_uids
    
    
    def extract_data_from_table(self, uid_list):
        
        if not duration:
            queries_to_run = self._assemble_data_query(uid_list)
    
            for query in queries_to_run:
            
                result = self.db.query(query)

            print result
        
        return result
    
    
def main(duration=None):
    
    users= Users_activity()
    uids = users.extract_active_uids(duration)
    users.extract_data_from_table(uid_list = uids)
   

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        duration = str(sys.argv[1])
    else: 
        duration =None
   
    main()
        
    
    
       


        
    
