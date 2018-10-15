#! /usr/bin/env python

from build_friend_graph import CKGraph, DBConnection
import networkx as nx
import numpy, os, sys, random
from database import *
import re
from transform_labels_to_nx import *


"""
AnnotateGraph.py

This script is used to generate a GraphML file which stores all of the attributes for the nodes and the edgelists

Created by Daniel McClary on 2010-12-21 and Modified by Rufaro Mukogo on 2011-03-08.
Copyright (c) 2010 __Northwestern University. All rights reserved.

The class DBConnection provides an interface to Facebook's MySQLDB wrapper.  The class CKGraph enables building undirected and directed
graphs (via NetworkX) from the CalorieKing database.
"""

class DBConnection(object):

    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!", dbdate="2010"):

        if dbdate == "2010":
            self.database = "calorie_king_social_networking_2010"
        else:
            self.database = "calorie_king_social_networking"

        self.db = Connection(server, self.database, user, passwd)

    def query(self, q_string):
        return self.db.query(q_string)


class AnnotateGraph(object):

    def __init__(self, candidate_file, graph_file = None, num_points=5 , dbdate = "2010"):

        self.db = DBConnection(dbdate=dbdate)
        self.dbdate = dbdate

        #get a hash of hashes of candidate information
        self.candidates = self._get_candidates(candidate_file)
        print "keys", self.candidates['40961']
        
        uids = []
        for key in self.candidates:
            #print self.candidates[key]['ck_id']
            uids.append(self.candidates[key]['ck_id'])
        #build a networkx graph of the candidates
        if not graph_file:
            ckg = CKGraph()
            self.graph = ckg.build_undirected_graph(uids=uids, write=False)[0]
        else:
            if ".gml" in graph_file:
                self.graph = nx.read_gml(graph_file)
                self.graph = nx.Graph(self.graph.to_undirected())
                self.graph = transform_labels_to_nx(self.graph)
            else:
                self.graph = nx.read_edgelist(graph_file)
            #self.graph = nx.relabel_nodes(self.graph, dict(zip(self.graph.nodes(),map(int, self.graph.nodes()))))

       #extract only the giant component
        self.output = {}

    def _get_candidates(self, candidate_file):
        #we want a hash of hashes here, so use a lambda function to make each line of candidates its own hash
        candidates = open(candidate_file).readlines()
        header = candidates[0]
        prepare_header= lambda x: x.strip().strip('"')
        header = map(prepare_header, header.split(","))
        print header
        candidates = candidates[1:]
        self.candidates = dict(map(lambda x: [str(x.split(",")[0]),dict(zip(header,x.strip().split(",")))], candidates))


#        print dict(candidates)

        return self.candidates

    def _annotate_graph(self, metric_hash, metric_name):

        #annotate the graph
        for v in metric_hash:
            self.graph.node[v][metric_name]=metric_hash[v]

    def _get_activity_hash(self):

        #query the activity table to get activity counts for all nodes including weigh-ins
        db = DBConnection()
        activity_hash = {}
        activity_query = """SELECT COUNT(activity_date) FROM activity_combined where ck_id = """

        for node in self.graph.nodes():
            #query the activity table for all the days this user was active
            q = activity_query + "'"+str(self.candidates[node]['ck_id'])+"'"
            result = db.query(q)
            activity_hash[node] =  int(result[0]['COUNT(activity_date)'])

        return activity_hash

    def betweenness(self):
        """compute betweeness"""
        betweenness_hash =nx.betweenness_centrality(self.graph)
        betweenness_nodes = self._annotate_graph(betweenness_hash, 'betweenness')

    def degree(self):
        """compute degree"""
        degree_hash = self.graph.degree()
        degree_nodes = self._annotate_graph(degree_hash, 'degree')

    def pagerank(self):
        """compute pagerank"""
        pr_hash = nx.pagerank(self.graph)
        pr_nodes = self._annotate_graph(pr_hash, 'pagerank')

    def vitality(self):
        """compute vitality"""
        vit_hash = nx.closeness_vitality(self.graph)
        vit_nodes = self._annotate_graph(vit_hash, 'vitality')

    def clustering(self):
        """compute clustering coefficient"""
        cluster_hash = nx.clustering(self.graph)
        cluster_nodes = self._annotate_graph(cluster_hash, "clustering")

    def triangles(self):
        """compute number of triangles"""
        tri_hash = nx.triangles(self.graph)
        tri_nodes = self._annotate_graph(tri_hash, "triangles")

    def total_num_weighins(self):
        """total number of weighins"""
        num_weighins_hash = {}
        for key in self.graph.nodes():
            num_weighins_hash[key] = int(float(self.candidates[key]["weighins"]))

        weighins_nodes = self._annotate_graph(num_weighins_hash, "weighins")

    def initial_weight(self):
        """initial_weight"""
        initial_weight_hash = {}
        for key in self.graph.nodes():
            initial_weight_hash[key] = int(float((self.candidates[key]["initial_weight"])))

        initial_weight_nodes = self._annotate_graph(initial_weight_hash, "initial_weight")

    def weight_loss(self):
        """weight loss for each user"""
        weight_loss_hash = {}
        for key in self.graph.nodes():
            print key, type(key),self.candidates[40961]['weight_change'],self.canid
            weight_loss_hash[key] = float(self.candidates[key]['weight_change'])

        weight_loss_nodes = self._annotate_graph(weight_loss_hash, "weight_change")

    def total_num_days(self):
        """ number of days between first and last weighins"""
        num_days_hash = {}
        for key in self.graph.nodes():

            num_days_hash[key] = int(float(self.candidates[key]["days"]))
        num_days_nodes = self._annotate_graph(num_days_hash, "days")

    def n_weight_loss(self):
        """weight loss divided by the number of days"""
        n_weight_loss_hash = {}
        for key in self.graph.nodes():
            try:
                n_weight_loss_hash[key] = float(self.candidates[key]["n_weight_change"])
            except KeyError:pass

        n_weight_loss_nodes = self._annotate_graph(n_weight_loss_hash,"n_weight_change")

    def percentage_weight_change(self):
        """ percentage of weight gained / lost  compared to initial weight"""
        percentage_weight_change_hash = {}
        for key in self.graph.nodes():
            percentage_weight_change_hash[key] = float(self.candidates[key]["percentage_weight_change"])

        percentage_weight_change_nodes = self._annotate_graph(percentage_weight_change_hash,\
                "percentage_weight_change")

    def time_in_sys(self):
        """ tme between the join date and the last known activity"""
        time_in_sys_hash = {}
        for key in self.graph.nodes():
            time_in_sys_hash[key] = int(float(self.candidates[key]["time_in_system"]))

        time_in_sys_nodes = self._annotate_graph(time_in_sys_hash, "time_in_system")

    def activity(self):
        """number of instances of activity, including weigh-ins"""
        activity_hash = self._get_activity_hash()
        activity_nodes = self._annotate_graph(activity_hash, "activity")

    def age(self):
        """ ages of the users in years"""
        age_hash = {}
        for key in self.graph.nodes():
            age_hash[key] = int(float(self.candidates[key]["age"]))

        age_nodes = self._annotate_graph(age_hash, "age")

    def state(self):
        """ the state of residence/registration of the user"""
        state_hash = {}
        for key in self.graph.nodes():
            state_hash[key] = str(self.candidates[key]["state"])

        state_nodes = self._annotate_graph(state_hash, "state")


    def last_day_act(self):
        """ last day on which the user was active"""

        last_day_act_hash = {}
        for key in self.graph.nodes():
            last_day_act_hash[key] = str(self.candidates[key]["last_day_act"])

        last_day_act_nodes = self._annotate_graph(last_day_act_hash, "last_day_act")


    def days_since_last_act(self):
        """ number of days since the users last"""

        days_since_last_act = {}
        for key in self.graph.nodes():
             days_since_last_act[key] = int(float(self.candidates[key]["days_since_last_act"]))

        days_since_last_act_nodes = self._annotate_graph(days_since_last_act_hash, "days_since_last_act")


    def height(self):
        """height of the users in inches"""
        height_hash = {}
        for key in self.graph.nodes():
            height_hash[key] = int(float((self.candidates[key]["height"])))
        height_nodes = self._annotate_graph(height_hash, "height")

    def initial_BMI(self):
        """ (initial weight in lbs * 703 )/inches**2"""
        initial_BMI_hash = {}
        for key in self.graph.nodes():
            try:
            	initial_BMI_hash[key] = float(self.candidates[key]["initial_bmi"])
            except KeyError:
                pass
        initial_BMI_nodes = self._annotate_graph(initial_BMI_hash, "initial_bmi")

    def final_BMI(self):
        """ (final weight in lbs * 703 )/inches**2"""
        final_BMI_hash = {}
        for key in self.graph.nodes():
            try:
            	final_BMI_hash[key] = float(self.candidates[key]["final_bmi"])
            except KeyError:
                pass
        final_BMI_nodes = self._annotate_graph(final_BMI_hash, "final_bmi")

    def change_in_BMI(self):
        """change in BMI"""
        change_in_BMI_hash = {}
        for key in self.graph.nodes():
            change_in_BMI_hash[key] = float(self.candidates[key]["change_in_BMI"])
        change_in_BMI_nodes = self._annotate_graph(change_in_BMI_hash, "change_in_BMI")

    def write_graph(self, filename):
        "write the annotated graph"
        nx.write_edgelist(self.graph, filename, data=True)
        nx.write_gml(self.graph, filename+".gml")

if __name__ == "__main__":

    if len(sys.argv)>1:
        cf = sys.argv[1]
    else:
        print "please enter location on candidate file e.g.\
                ./5_points_network_2010/data/candidate_timeseries_with_%s"%(num_points)

    if len(sys.argv) > 4:
        dbdate = sys.argv[4]
    else:
        dbdate = "2010"

    if len(sys.argv) > 2 :
        gf = sys.argv[2]
    else:
        gf = None

    if len(sys.argv)>3:
        num_points = sys.argv[3]
    else:
        num_points = 5

    cam = AnnotateGraph(candidate_file=cf, graph_file=gf, num_points=num_points, dbdate=dbdate)
    #cam.height()
    #cam.age()
    cam.initial_BMI()
    cam.final_BMI()
    cam.weight_loss()
    cam.activity()
    cam.total_num_weighins()
    #cam.betweenness()
    cam.total_num_days()
    cam.initial_weight()
    #cam.n_weight_loss()
    #cam.days_since_last_act()
    #cam.last_act_date()
    cam.percentage_weight_change()
    cam.time_in_sys()
    cam.degree()
    #cam.pagerank()
    #cam.vitality()
    #cam.clustering()
    #cam.triangles()
    #cam.change_in_BMI()

    if dbdate == "2010":
        cam.write_graph("./method2_50/networks/method2_50_nonadherent")
    else:
        pass

