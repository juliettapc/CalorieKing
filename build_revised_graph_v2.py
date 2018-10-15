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
from datetime import date
import networkx as nx

def write_row(f,row, header):
    row_to_write = []
    for key in header:
        try:
            row_to_write.append(row[key])
        except KeyError:pass
    
    print >> f, ",".join(map(str,row_to_write))
    
def format_user(row, header,types):
    formatted_row = {}
    for key_count in range(len(header)):
        key = header[key_count]
        if key in row:
            if types[key_count] == "s":
                formatted_row[key] = row[key]
            elif types[key_count] == "n":
                formatted_row[key] = float(row[key])
        else:
            formatted_row[key] = compute_metric(key,row,types[key_count])
            
    return formatted_row

def compute_metric(metric, row, metric_type):
    result_metric = None
    if metric == "initial_bmi":
        result_metric = compute_initial_bmi(row)
    elif metric == "final_bmi":
        result_metric = compute_final_bmi(row)
    elif metric == "percentage_weight_change":
        result_metric = compute_weight_change_per(row)
    elif metric == "weight_change":
        result_metric = compute_weight_change(row)
    elif metric == "time_in_system":
        result_metric = compute_time_in_system(row)
    elif metric == "days":
        result_metric = compute_days(row)
    elif metric == "weighins":
        result_metric = compute_weighins(row)
        
    return result_metric

def compute_weighins(row):
        db = DBConnection()
        ck_id = row['ck_id']
        join_date = str(row['join_date'].date())
        count_query ="SELECT COUNT(*) FROM weigh_in_history WHERE ck_id = '"+ck_id+"' AND on_day >= '"+join_date+"'"
        count = int(db.query(count_query)[0]['COUNT(*)'])
        return count
  
def compute_initial_bmi(row):
    return float(float(row['initial_weight'])*703.0)/float(row['height'])**2

def compute_final_bmi(row):
    return float(float(row['most_recent_weight'])*703.0)/float(row['height'])**2
    
def compute_weight_change_per(row):
    start_weight = float(row['initial_weight'])
    end_weight = float(row['most_recent_weight'])
    return ((end_weight - start_weight)/start_weight)*100.0
    
def compute_weight_change(row):
    start_weight = float(row['initial_weight'])
    end_weight = float(row['most_recent_weight'])
    return end_weight - start_weight

def compute_time_in_system(row):
    #get the difference between the join date and the last known activity
    db = DBConnection()
    ck_id = row['ck_id']
    join_date = row['join_date']
    last_activity_query = "SELECT activity_date FROM activity_combined WHERE ck_id = '" + ck_id+ "' ORDER BY activity_date DESC LIMIT 1"
    last_activity = db.query(last_activity_query)[0]
    last_activity = last_activity['activity_date']
    delta = last_activity - join_date.date()
    return delta.days
    
def compute_days(row):
    days = 0
    db = DBConnection()
    ck_id = row['ck_id']
    join_date = row['join_date']
    days_query = "SELECT on_day FROM weigh_in_history WHERE ck_id = '"+ck_id+"' AND on_day >= '" + str(join_date) + "'"
    first_day_query = days_query + "ORDER BY on_day ASC LIMIT 1"
    last_day_query = days_query + "ORDER BY on_day DESC LIMIT 1"
    first_day = db.query(first_day_query)
    last_day = db.query(last_day_query)
    if len(first_day) > 1 and len(last_day) > 1:
        first_day = first_day[0]
        last_day = last_day[0]
        delta = last_day['on_day'] - first_day['on_day']
        days = delta.days
    return days
    
class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking_2010"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class Everyone(object):
        def __init__(self):
            self.connection = DBConnection()
            self.header = ["id","ck_id","join_date","initial_weight", "most_recent_weight", "height", "age",\
             "weighins", "initial_bmi", "final_bmi", "percentage_weight_change", "weight_change", "time_in_system", "days"]
            self.header_types = ["s","s","s","n", "n", "n", "n",\
             "n","n", "n", "n", "n", "n", "n"]
            self.table = []

        def build(self):
            build_query = """SELECT id,ck_id, join_date, initial_weight, most_recent_weight, height, age FROM users"""
            result = self.connection.query(build_query)
            for r in result:
                self.table.append(format_user(r,self.header,self.header_types))

        def write(self, filename):
            f = open(filename, "w")
            print >> f, ",".join(self.header)
            for row in self.table:
                write_row(f,row, self.header)
            f.close()

class Newcomers(Everyone):  
    def build(self):
        build_query = """SELECT id,ck_id, join_date, initial_weight, most_recent_weight, height, age FROM users WHERE join_date >= '2010-10-1'"""
        result = self.connection.query(build_query)
        for r in result:
            self.table.append(format_user(r,self.header,self.header_types))
            
class Engaged(Everyone):
    def __init__(self):
        self.connection = DBConnection()
        self.header = ["id","ck_id","join_date","initial_weight", "most_recent_weight", "height", "age",\
         "weighins","initial_bmi", "final_bmi", "percentage_weight_change", "weight_change", "time_in_system", "days"]
        self.header_types = ["s","s","s","n", "n", "n", "n",\
         "n","n", "n", "n", "n", "n", "n"]
        self.engaged_table = []
        self.unengaged_table = []
        
    def build(self):
        build_query = """SELECT id,ck_id, join_date, initial_weight, most_recent_weight, height, age FROM users WHERE join_date < '2010-10-1'"""
        result = self.connection.query(build_query)
        self.engaged_table, self.unengaged_table = self.filter_for_engagement(result)
    
    def filter_for_engagement(self,result):
        #take only those users who are greater than 100 days time in system
        filtered_result = []
        remainder = []
        for r in result:
            time_in_system = compute_time_in_system(r)
            if time_in_system > 50:
                filtered_result.append(format_user(r, self.header, self.header_types))
            else:
                remainder.append(format_user(r, self.header, self.header_types))
                
        return filtered_result, remainder
        
    def write(self, engaged_filename, unengaged_filename):
        f = open(engaged_filename, "w")
        print >> f, ",".join(self.header)
        for row in self.engaged_table:
            write_row(f,row, self.header)
        f.close()
        
        f = open(unengaged_filename, "w")
        print >> f, ",".join(self.header)
        for row in self.unengaged_table:
            write_row(f,row, self.header)
        f.close()
        
class Adherent(Everyone):
    def __init__(self):
        self.connection = DBConnection()
        self.header = ["id","ck_id","join_date","initial_weight", "most_recent_weight", "height", "age",\
         "weighins","initial_bmi", "final_bmi", "percentage_weight_change", "weight_change", "time_in_system", "days"]
        self.header_types = ["s","s","s","n", "n", "n", "n",\
         "n","n", "n", "n", "n", "n", "n"]
        self.adherent_table = []
        self.nonadherent_table = []
        self.adherent_graph = None
        self.adherent_nonnetworked = []
        self.nonadherent_graph = None
        self.nonadherent_nonnetworked = []
        
    def filter_for_engagement(self,result):
        #take only those users who are greater than 100 days time in system
        filtered_result = []
        remainder = []
        for r in result:
            time_in_system = compute_time_in_system(r)
            if time_in_system > 50:
                filtered_result.append(format_user(r, self.header, self.header_types))
            else:
                remainder.append(format_user(r, self.header, self.header_types))
                
        return filtered_result, remainder
        
    def write(self, adherent_filename, nonadherent_filename):
        
        self.adherent_filename, self.nonadherent_filename = adherent_filename,nonadherent_filename
        
        f = open(self.adherent_filename+".csv", "w")
        print >> f, ",".join(self.header)
        for row in self.adherent_table:
            write_row(f,row, self.header)
            print row
        f.close()

        f = open(self.nonadherent_filename+".csv", "w")
        print >> f, ",".join(self.header)
        for row in self.nonadherent_table:
            write_row(f,row, self.header)
        f.close()
        
        nx.write_gml(self.adherent_graph,self.adherent_filename+".gml")
        nx.write_gml(self.nonadherent_graph,self.nonadherent_filename+".gml")
        
        nx.write_edgelist(self.adherent_graph,self.adherent_filename)
        nx.write_edgelist(self.nonadherent_graph,self.non_adherent_filename)
         
    def build(self):
        build_query = """SELECT id,ck_id, join_date, initial_weight, most_recent_weight, height, age FROM users WHERE join_date < '2010-10-1'"""
        result = self.connection.query(build_query)
        engaged, unengaged = self.filter_for_engagement(result)
        self.adherent_table, self.nonadherent_table = self.filter_for_adherence(engaged)
        print "check the size of the adherent table", len(self.adherent_table)
        print "check the size of the nonadherent table", len(self.nonadherent_table)
        
        #build graphs for both tables
        self.adherent_graph, self.adherent_nonnetworked = self.build_graph(self.adherent_table)
        self.nonadherent_graph, self.nonadherent_nonnetworked = self.build_graph(self.nonadherent_table)
    
        

    def get_id(self, ck_id):
        id_query = "SELECT id FROM users where ck_id='"+ck_id+"'"
        idresult =  self.connection.query(id_query)
        id_return = None
        if len(idresult)> 0:
            try:
                id_return = idresult[0]['id']
            except IndexError:pass
        return id_return

    def get_friends(self,node):
        friends = []
        ck_id = node['ck_id']
        #get this node's label
        label = node['id']
        friend_query = "SELECT src, dest FROM friends where src='"+ck_id+"' OR dest='"+ck_id+"'"
        friend_result = self.connection.query(friend_query)
        
        for f in friend_result:
            ckids = f.values()
            
            try:
                friend = filter(lambda x:x!=ck_id, ckids)[0]
                friend_label = self.get_id(friend)
                       
                if friend_label:
                    if friend_label != label:
                        friends.append(friend_label)
            except IndexError:
                pass
        
        return friends
            
    def build_graph(self, candidates):
        G = nx.Graph()
        remainder = []
        for c in candidates:
            #get all the friends for this candiate
            edges = self.get_friends(c)
            label = c['id']
            if len(edges) >= 1:
                for e in edges:
                    G.add_edge(label,e)
            else:
                remainder.append(format_user(c,self.header, self.header_types))
        return G, remainder

    def count_weigh_ins(self, row):
        ck_id = row['ck_id']
        join_date = str(row['join_date'].date())
        count_query ="SELECT COUNT(*) FROM weigh_in_history WHERE ck_id = '"+ck_id+"' AND on_day >= '"+join_date+"'"
        count = int(self.connection.query(count_query)[0]['COUNT(*)'])
        return count
        
    def filter_for_adherence(self,result):
        filtered_result = []
        remainder = []
        for r in result:
            weigh_in_count = self.count_weigh_ins(r)
            if weigh_in_count >= 5:
                filtered_result.append(r)
            else:
                remainder.append(r)
        return filtered_result, remainder
        
    def filter_for_engagement(self,result):
        #take only those users who are greater than 100 days time in system
        filtered_result = []
        remainder = []
        for r in result:
            time_in_system = compute_time_in_system(r)
            if time_in_system > 50:
                filtered_result.append(format_user(r, self.header, self.header_types))
            else:
                remainder.append(format_user(r, self.header, self.header_types))
                
        return filtered_result, remainder
        
if __name__ == "__main__":
    
    #al = Everyone()
    #al.build()
    #al.write("./method3_50/master_everyone_ex_newcomers")
    #n = Newcomers()
    #n.build()
    #n.write("./method3_50/master_newcomers.csv")
    #e = Engaged()
    #e.build()
    #e.write("./method3_50/master_engaged.csv", "./method3_50/master_unengaged.csv")
    a = Adherent()
    a.build()
    a.write("./metohd3_50/csv/master_adherent", "./method3_50/csv/master_nonadherent")
