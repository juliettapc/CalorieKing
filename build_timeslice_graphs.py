#! /usr/bin/env python
from database import *
import networkx as nx
from copy import copy
import numpy
import os,sys

"""

build_timeslice_graphs.py

Created by Rufaro Mukogo on 2011-03-27.
Copyright (c) 2010 __Northwestern University. All rights reserved

This script can be used to extract the networks for different time slices of the 2 year data that is
available for CalorieKing. At each time period, for example quarters, only users who were active in that
period are included. Furthermore, of this initial set of users, only users that joined after 1
January 2009 are included in building out the friendship network at each time point.

"""

class DBConnection(object):

    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking_2010"
        self.db = Connection(server, self.database, user, passwd)
 
    def query(self, q_string):
        return self.db.query(q_string)

class CKGraph(object):

    def __init__(self):
        self.db = DBConnection()
        
        self.year = ['2009-','2010-']
        
        self.quarters = [("2009-01-01", "2009-03-31"), ("2009-04-01", "2009-06-30"),\
        ("2009-07-01", "2009-09-30"), ("2009-10-01", "2009-12-31"),("2010-01-01", "2010-03-31"), ("2010-04-01", "2010-06-30"),\
        ("2010-07-01", "2010-09-30"), ("2010-10-01", "2010-12-31")]
        
        
        self.sixmonths = [("2009-01-01", "2009-05-31"), ("2009-06-01", "2009-12-31"),\
        ("2010-01-01", "2010-05-31"), ("2010-06-01", "2010-12-31")] 

        self.months = [("01-01", "01-31"), ("02-01","02-28"), ("03-01", "03-31"),\
        ("04-01", "04-30"), ("05-01","05-31"), ("06-01","06-30"), ("07-01", "07-31"),\
        ("08-01","08-31"), ("09-01", "09-30"), ("10-01", "10-31"), ("11-01", "11-30"),\
        ("12-01","12-31")]
       
        self.month_ends = (31,28,31,30,31,30,31,31,30,31,30,31)
    
    def _ck_ids_by_period(self,duration):
        ck_ids = []

        for q in duration:
            if duration == self.months:
                v = (self.year+q[0], self.year+q[1])
            else:
                v = q
            # sub-query to get the uses active in a particular quarter
            result = self.db.query("SELECT distinct ck_id from activity_combined WHERE activity_date >= '"+str(v[0])+"' AND activity_date <= '"+str(v[1])+"'")
            print len(result)

            #selected for activity in the time period
            active_users = [r['ck_id'] for r in result]
            adj_for_join_date = []
            
            for a in active_users:
                try:
                    result2 = self.db.query("SELECT u.ck_id from users as u where u.ck_id ='"+str(a)+"'") 
                    #print "results", result 

                    adj_for_join_date.append(result2[0]['ck_id'])
                
                except IndexError:
                    pass

            ck_ids.append(adj_for_join_date)
  
        return ck_ids
        
    def _query_full_network_and_add_edges(self, duration=None, uids=None):    
        
        result_graphs = []

        if not duration:
            print "Must enter sixmonths or quarters as duration"
            sys.exit()
        elif duration == "sixmonths":
            list_of_period_ck_ids = self._ck_ids_by_period(self.sixmonths)
            self.gtag = "sixmonths"
        elif duration =="quarters":
            list_of_period_ck_ids = self._ck_ids_by_period(self.quarters)
            self.gtag = "quarter"
        
        i = 0
        for period in list_of_period_ck_ids:
            
            tmp_graph = copy(self.G)
            
            print "period length", len(period)
            for ck_id in period:
                result = self.db.query("SELECT f.* FROM friends AS f WHERE f.src ='"+str(ck_id)+"'")
                
                for r in result:
                    
                    try:
                        src_id_result  = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["src"]+"'")
                        dest_id_result = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["dest"]+"'")
        
                    
                        tmp_graph.add_edge(int(src_id_result[0]['id']), int(dest_id_result[0]['id']))
                
                    except IndexError:
                        pass

            print "period length sanity check", len(tmp_graph)
           

            #write the gml files and the edgelists
            nx.write_gml(tmp_graph,"./5_points_network_2010/data/new_networks/friends_undirected_all_"+str(self.gtag)+str(i)+".gml")
            nx.write_edgelist(tmp_graph,"./5_points_network_2010/data/new_networks/friends_undirected_all_"+str(self.gtag)+str(i))
            
            result_graphs.append(tmp_graph)
        
            print "nodes in results as tmp_files are added", map(len, result_graphs)
            i=i+1

        return 
             
    def build_undirected_graph(self, duration=None, uids=None):
        
        self.G = nx.Graph()
       
        graphs = self._query_full_network_and_add_edges(duration, uids)
        
       

if __name__=="__main__":

    try: 
        import psycho
        psycho.full()
    except ImportError:
       pass
    
    if len(sys.argv)>1:
        duration = sys.argv[1]
    else:
        duration = "quarters"

    if len(sys.argv)>2:
        path = sys.argv[2]
    else:
        path = os.getcwd()+"/"

    g = CKGraph()
    g.build_undirected_graph(duration=str(duration))
