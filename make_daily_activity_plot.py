#!/usr/bin/env python
# encoding: utf-8
"""
make_daily_activity_plot.py

Created by Daniel McClary on 2011-01-27.
Copyright (c) 2011 __Daniel McClary__. All rights reserved.

This code queries the activity_combined table, builds a numpy matrix and then makes a broken bar chart for each day
"""

from database import *
from copy import copy
from build_friend_graph import CKGraph
import numpy
import os
import sys
from matplotlib import pyplot
from matplotlib import colors
import random
import networkx as nx

class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)


def get_candidates(candidate_file):
    candidates = open(candidate_file).readlines()
    candidates = candidates[1:]
    candidates = map(lambda x: [x.split(",")[1],x.split(",")[0]], candidates)
    return dict(candidates)
    

def main(candidate_file):
    candidates = get_candidates(candidate_file)
    # get the graph of users for the whole year
    calorie_king_social_network = CKGraph()
    graphs = calorie_king_social_network.build_undirected_graph(uids=candidates.keys())
    G = graphs[0]
    components = nx.connected_component_subgraphs(G)
    giant_component = components[0]
    giant_nodes = giant_component.nodes()

    #get the active users for each day
    master_query ="""Select distinct(ck_id) from activity_time_log """
    db = DBConnection()
    #get the field names for each day of the year
    result = db.query("DESCRIBE activity_time_log")
    days = filter(lambda y: y != 'ck_id', map(lambda x: str(x['Field']), result))
    #make the matrix of user activity
    activity = numpy.zeros((len(giant_nodes),len(days)))
    rows = {}
    row_count = 0
    column_count = 0
    for day in days:
        active_users = db.query(master_query + "WHERE " + day + " IS NOT NULL")
        active_users = map(lambda x: str(x['ck_id']), active_users)
        for user in active_users:
            if user in candidates.keys() and int(candidates[user]) in giant_nodes:
                if user not in rows.keys():
                    row_count += 1
                    rows[user] = row_count
                activity[rows[user],column_count] = 1
        column_count += 1


    
    #for each row in the plot, make a list of the days of activity
    plot_rows = {}
    for r in rows.values():
        plot_rows[r] = []
        current_column_start = -1
        current_column_width = 0
        for i in range(len(activity[r,:])):
            #if there's activity today
            if activity[r,i] == 1:
                #then if we haven't started a bar, start one
                if current_column_start == -1:
                    current_column_start = i
                current_column_width += 1
                #if there's not activity today and it's the end of a bar
            elif activity[r,i] < 1 and current_column_start != -1:
                plot_rows[r].append((current_column_start, current_column_width))
                current_column_start = -1
                current_column_width = 0
    #make the broken bar blot
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    #colors
    colormap = pyplot.cm.autumn
    #add the bars
    column_width = [1,3]
    increment = lambda x: [x[0]+3, 3]
    random_rows = random.sample(plot_rows.keys(),len(plot_rows.keys()))
    for i in range(1,len(random_rows)+1):
        color = colormap((random.random(), random.random(), random.random()))
        ax.broken_barh(plot_rows[random_rows[i-1]], tuple(column_width), facecolor=color)
        column_width = increment(column_width)
    ax.set_xlabel("Days of user activity")
    ax.set_xlim(0,365)
    ax.set_ylabel("User")
    ax.set_title('User Activity Map')
    pyplot.show()
                
    
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        candidate_file = sys.argv[1]
        main(candidate_file)

