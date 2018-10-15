#! /usr/bin/env python

from database import *
import networkx as nx
from copy import copy
import numpy
import os

class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class CKGraph(object):
    
    def __init__(self):
        self.db = DBConnection()
        
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
            #print len(result)
            for r in result:
                #get the source id
                src_id_result = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["src"]+"'")
                
                #get the dest id
                dest_id_result = self.db.query("SELECT id FROM users WHERE ck_id = '"+r["dest"]+"'")
                if len(src_id_result) > 0 and len(dest_id_result) > 0:
                    src_id = int(src_id_result[0]['id'])
                    dest_id = int(dest_id_result[0]['id'])
                #if r["src"] not in self.count_hash:
                #    self.count_hash[r["src"]] = self.counter
                #    self.counter += 1
                #src = self.count_hash[r["src"]]
                #if r["dest"] not in self.count_hash:
                #    self.count_hash[r["dest"]] = self.counter
                #    self.counter += 1
                #dest = self.count_hash[r["dest"]]
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
        
            
    def build_undirected_graph(self, duration=None, uids=None):
        self.G = nx.Graph()
        if not duration: 
            g_tag = "_all"
        elif duration == "quarters":
            g_tag = "_quarter"
        elif duration == "months":
            g_tag = "_month"
        graphs = self._query_full_network_and_add_edges(duration, uids)
        for i in range(len(graphs)):
            nx.write_edgelist(graphs[i], "/home/staff/rmukogo/calorie_king_hg/data/new_networks/friends_undirected_all"+g_tag+str(i), data=False)
            nx.write_gml(graphs[i],"/home/staff/rmukogo/calorie_king_hg/data/new_networks/friends_undirected_all"+g_tag+str(i)+".gml")
        return graphs
            
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
