#! /usr/bin/env python
"""
build_friend_graph.py

Created by Daniel McClary on 2010-12-21.
Copyright (c) 2010 __Northwestern University. All rights reserved.

The class DBConnection provides an interface to Facebook's MySQLDB wrapper.  The class CKGraph enables building undirected and directed
graphs (via NetworkX) from the CalorieKing database.
"""
from database import *
import networkx as nx
from copy import copy
import numpy
import os

class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking_2010"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class CKGraph(object):
    
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
        
    def _assemble_query(self, master, duration):
        queries = []
        for q in duration:
            if duration == self.months:
                v = (self.year+q[0], self.year+q[1])
            else:
                v = q
            q_string = master + " AND u.join_date >= " + v[0] + " AND u.join_date <= " + v[1] 
            queries.append(q_string)
        return queries
        
    def _assemble_trend_query(self, master, duration):
        queries = []
        for q in duration:
            if duration == self.months:
                v = (self.year+q[0], self.year+q[1])
            else:
                v = q
            q_string = master + "' AND on_day >= " + v[0] + " AND on_day <= " + v[1] + """ ORDER BY on_day ASC"""
            queries.append(q_string)
        return queries
        
    def _query_full_network_and_add_edges(self, duration=None, uids=None):    
        self.counter = 0
        self.count_hash = {}
        master_query = """SELECT f.* FROM friends AS f, users as u WHERE (f.src = u.ck_id)"""
        print master_query
        if not duration:
            queries_to_run = [master_query]  
        elif duration == "quarters":
            queries_to_run = self._assemble_query(master_query, self.quarters)
        elif duration == "months":
            queries_to_run = self._assemble_query(master_query, self.months)
        
        result_graphs = []
        for query in queries_to_run:
            tmp_graph = copy(self.G)
            #print query
            result = self.db.query(query)
            
            for r in result:
                #get the source id
                src_id_result = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["src"]+"'")
                
                #get the dest id
                dest_id_result = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["dest"]+"'")
                if len(src_id_result) > 0 and len(dest_id_result) > 0:
                    src_id = str(src_id_result[0]['id'])
                    dest_id = str(dest_id_result[0]['id'])
               
                    if uids:
                        if r["src"] in uids and r["dest"] in uids:
                            tmp_graph.add_edge(src_id, dest_id)
                    else:
                        tmp_graph.add_edge(src_id, dest_id)
            #print len(tmp_graph)
            result_graphs.append(tmp_graph)
            
        return result_graphs
    
    def _query_no_staff_network_and_add_edges(self, duration=None):
        self.counter = 0
        self.count_hash = {}
        master_query = """SELECT f.* FROM friends AS f, users as u WHERE (f.src = u.ck_id) AND (u.is_staff = 0)"""
        if not duration:
            queries_to_run = [master_query]  
        elif duration == "quarters":
            queries_to_run = self._assemble_query(master_query, self.quarters)
        elif duration == "months":
            queries_to_run = self._assemble_query(master_query, self.months)
        
        result_graphs = []
        for query in queries_to_run:
            #print query
            tmp_graph = copy(self.G)
            result = self.db.query(query)
            for r in result:
                if r["src"] not in self.count_hash:
                    self.count_hash[r["src"]] = self.counter
                    self.counter += 1
                src = self.count_hash[r["src"]]
                if r["dest"] not in self.count_hash:
                    self.count_hash[r["dest"]] = self.counter
                    self.counter += 1
                dest = self.count_hash[r["dest"]]
                tmp_graph.add_edge(src, dest)
            result_graphs.append(nx.connected_component_subgraphs(tmp_graph)[0])
            
        return result_graphs
        
            
    def build_undirected_graph(self, duration=None, uids=None, write=False):
        self.G = nx.Graph()
        if not duration: 
            g_tag = "_all"
        elif duration == "quarters":
            g_tag = "_quarter"
        elif duration == "months":
            g_tag = "_month"
        graphs = self._query_full_network_and_add_edges(duration, uids)
        if write:
            for i in range(len(graphs)):
                nx.write_edgelist(graphs[i], "calorie_king_friends_undirected_giant"+g_tag+str(i), data=False)
                nx.write_gml(graphs[i], "calorie_king_friends_undirected_giant"+g_tag+str(i)+".gml")
        return graphs
        
    def _get_weight_trend(self, uid, duration):
        master_query = """SELECT on_day, weight FROM `weigh_in_history` WHERE ck_id = """ +"'" + uid
        if not duration:
            queries_to_run = [master_query+ "' ORDER BY on_day ASC"]  
        elif duration == "quarters":
            queries_to_run = self._assemble_trend_query(master_query, self.quarters)
        elif duration == "months":
            queries_to_run = self._assemble_trend_query(master_query, self.months)
        
        trendsets = []
        for query in queries_to_run:
            #print query
            result = self.db.query(query)
            trendsets.append(result)
        return trendsets
             
    def get_weight_timeseries(self, duration=None):
        current_id_mapping = copy(self.count_hash)
        if not duration:
            g_tag = "_all"
            dirstring = "weights_all"
        elif duration == "quarters":
            g_tag = "_quarter"
            dirstring = "weights_quarters"
        elif duration == "months":
            g_tag = "_month"
            dirstring = "weights_months"
            
        os.system("mkdir "+dirstring)
            
        for key in current_id_mapping:
            trendsets = self._get_weight_trend(key, duration)
            for i in range(len(trendsets)):
                subject_filename = dirstring+"/"+str(current_id_mapping[key])+"_weight_history"+g_tag+"_"+str(i)
                f = open(subject_filename, "w")
                print >> f, '"on_day"\t"weight"'
                for t in trendsets[i]:
                    print >> f, "\t".join(map(str, [t["on_day"], t["weight"]]))
                f.close()
        
            
    def build_no_staff_graph(self, duration=None):
        self.G = nx.Graph()
        if not duration: 
            g_tag = "_all"
        elif duration == "quarters":
            g_tag = "_quarter"
        elif duration == "months":
            g_tag = "_month"
        graphs = self._query_no_staff_network_and_add_edges(duration)
        for i in range(len(graphs)):
            nx.write_edgelist(graphs[i], "calorie_king_friends_no_staff_undirected_giant"+g_tag+str(i), data=False)
            nx.write_gml(graphs[i], "calorie_king_friends_no_staff_undirected_giant"+g_tag+str(i)+".gml")
        return graphs
    
    def build_directed_graph(self, duration=None):
        self.G = nx.DiGraph()
        if not duration: 
            g_tag = "_all"
        elif duration == "quarters":
            g_tag = "_quarter"
        elif duration == "months":
            g_tag = "_month"
        graphs = self._query_full_network_and_add_edges(duration)
        
        for i in range(len(graphs)):
            nx.write_edgelist(graphs[i], "calorie_king_friends_directed_giant"+g_tag+str(i))
            nx.write_gml(graphs[i], "calorie_king_friends_directed_giant"+g_tag+str(i)+".gml")
        return graphs
