#! /usr/bin/env python

from build_friend_graph import CKGraph, DBConnection
import networkx as nx
import numpy
import os
import sys
import random

class CKActivityMetrics(object):
    def __init__(self, candidate_file, graph_file = None, cut_off=10):
        #get a hash of hashes of candidate information
        self.candidates = self._get_candidates(candidate_file)
        self.n = cut_off
        uids = []
        for key in self.candidates:
            uids.append(self.candidates[key]["ck_id"])
        #build a networkx graph of the candidates
        if not graph_file:
            ckg = CKGraph()
            self.graph = ckg.build_undirected_graph(uids=uids, write=False)[0]
        else:
            if ".gml" in graph_file:
                self.graph = nx.read_gml(graph_file)
                self.graph = nx.Graph(self.graph.to_undirected())
            else:
                self.graph = nx.read_edgelist(graph_file)
            self.graph = nx.relabel_nodes(self.graph, dict(zip(self.graph.nodes(),map(int, self.graph.nodes()))))
        #extract only the giant component
        self.output = {}
        
    def _get_candidates(self, candidate_file):
        #we want a hash of hashes here, so use a lambda function to make each line of candidates its own hash
        candidates = open(candidate_file).readlines()
        candidates = candidates[1:]
        candidates = map(lambda x: [int(x.split(",")[0]),dict(zip(["ck_id", "weigh_ins", "weight_change", "days","n_weight_change" ],\
            x.split(",")[1:6]))], candidates)
        return dict(candidates)
    
    def _annotate_graph(self, metric_hash, metric_name, greater=True):
        #compute the 10 most-metric nodes and their neighbors
        b_values = metric_hash.values()
        b_values.sort()
        if not greater:
            b_values.reverse()
        b_values = b_values[-int(self.n):]
        b_nodes = {}
        #get the top ten values
        for k in metric_hash:
            if metric_hash[k] in b_values:
                #if we have less than n nodes
                if len(b_nodes) < self.n:
                    b_nodes[k] =[metric_hash[k], self.graph.neighbors(k)]
                else:
                    #if we have 10 nodes and one is less between, replace it
                    if greater and min(map(lambda x:b_nodes[x][0], b_nodes)) < metric_hash[k]:
                        #find the node with minimum betweenness
                        min_bet = min(map(lambda x: b_nodes[x][0], b_nodes))
                        min_bet_nodes = filter(lambda x: b_nodes[x][0] == min_bet, b_nodes)
                        #choose a node at random
                        node_to_remove = random.choice(min_bet_nodes)
                        #delete its key
                        del b_nodes[node_to_remove]
                        #add the new one
                        b_nodes[k] = [metric_hash[k], self.graph.neighbors(k)]
                    elif not greater and max(map(lambda x:b_nodes[x][0], b_nodes)) > metric_hash[k]:
                            #find the node with minimum betweenness
                            min_bet = max(map(lambda x: b_nodes[x][0], b_nodes))
                            min_bet_nodes = filter(lambda x: b_nodes[x][0] == min_bet, b_nodes)
                            #choose a node at random
                            node_to_remove = random.choice(min_bet_nodes)
                            #delete its key
                            del b_nodes[node_to_remove]
                            #add the new one
                            b_nodes[k] = [metric_hash[k], self.graph.neighbors(k)]
        
        #annotate the graph in terms of betweenness
        for v in metric_hash:
            self.graph.node[v][metric_name]=metric_hash[v]

        return b_nodes

    def _get_activity_hash(self):
        #query the activity table to get activity counts for all nodes
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
        """compute the n most-between nodes and their neighbors"""
        betweenness_hash =nx.betweenness_centrality(self.graph)
        betweenness_nodes = self._annotate_graph(betweenness_hash, 'betweenness')
        self.build_output_data(betweenness_nodes, 'betweenness')

    def degree(self):
        """compute the n highest degree nodes and their neighbors"""
        degree_hash = self.graph.degree()
        degree_nodes = self._annotate_graph(degree_hash, 'degree')
        self.build_output_data(degree_nodes, 'degree')

    def pagerank(self):
        """compute the n highest page-ranked nodes and their neighbors"""
        pr_hash = nx.pagerank(self.graph)
        pr_nodes = self._annotate_graph(pr_hash, 'pagerank')
        self.build_output_data(pr_nodes, 'pagerank')

    def vitality(self):
        """compute the n nodes with highest vitality"""
        vit_hash = nx.closeness_vitality(self.graph)
        vit_nodes = self._annotate_graph(vit_hash, 'vitality')
        self.build_output_data(vit_nodes, 'vitality')
    

    def clustering(self):
        """compute the n nodes with greatest clustering coefficient"""
        cluster_hash = nx.clustering(self.graph)
        cluster_nodes = self._annotate_graph(cluster_hash, "clustering")
        self.build_output_data(cluster_nodes, 'clustering')

    def triangles(self):
        """compute the n nodes with the greatest number of triangles"""
        tri_hash = nx.triangles(self.graph)
        tri_nodes = self._annotate_graph(tri_hash, "triangles")
        self.build_output_data(tri_nodes, 'triangles')

    def weight_loss(self):
        weight_loss_hash = {}
        for key in self.graph.nodes():
            weight_loss_hash[key] = int(self.candidates[key]['weight_change'])
            
        weight_loss_nodes = self._annotate_graph(weight_loss_hash, "weightloss", greater=False)
        self.build_output_data(weight_loss_nodes, 'weightloss')
    
    def n_weight_loss(self):
        n_weight_loss_hash = {}
        for key in self.graph.nodes():
            n_weight_loss_hash[key] = float(self.candidates[key]["n_weight_change"])

        n_weight_loss_nodes = self._annotate_graph(n_weight_loss_hash,"n_weight_change", greater = False) 
        self.build_output_data(n_weight_loss_nodes, "n_weight_change")


    def total_num_weigh_ins(self):
        num_weigh_ins_hash = {}
        for key in self.graph.nodes():
            num_weigh_ins_hash[key] = int(self.candidates[key]["weigh_ins"])
        
        weigh_ins_nodes = self._annotate_graph(num_weigh_ins_hash, "weigh_ins", greater = True)
        self.build_output_data(weigh_ins_nodes, "weigh_ins")

    def activity(self):
        activity_hash = self._get_activity_hash()
        activity_nodes = self._annotate_graph(activity_hash, "activity")
        self.build_output_data(activity_nodes, "activity")

    def _build_output_row(self, entry_key, entry):
        #entries are structures: node, metric, neighbor1:neighbor2:
        entry_list = [entry_key,entry[0],":".join(map(str, entry[1]))]
        return ",".join(map(str,entry_list))

    def build_output_data(self, nodes, metric_name):
          """add a new metric to the output hash"""
          self.output[metric_name] = []
          for key in nodes:
              self.output[metric_name].append(self._build_output_row(key, nodes[key]))
      
    def write(self, filename):
        #write a csv file of the output we could do this with combinations, 
        #but I don't know if it preserves order
        header = []
        header_categories = ["nodes", "metrics", "neighbors"]
        for key in self.output:
            for cat in header_categories:
                header.append(key+"_"+cat)
      
        header = ",".join(header)
      
        rows = zip(*self.output.values())
        for i in range(len(rows)):
            rows[i] = ",".join(rows[i])
        if len(header.split(",")) == len(rows[0].split(",")):
            f = open(filename, "w")
            print >> f, header
            for row in rows:
                print >> f, row
            f.close()

    def write_graph(self, filename):
        "write the annotated_graph"
        nx.write_edgelist(self.graph, filename, data=True)
        nx.write_gml(self.graph, filename+".gml")

if __name__ == "__main__":
    cf = sys.argv[1]
    if len(sys.argv) > 2:
        gf = sys.argv[2]
    else:
        gf = None
        
    if len(sys.argv)>3:
        cut_off = sys.argv[3]
    else:
        cut_off = 10
        
    cam = CKActivityMetrics(cf, gf, cut_off)
    print cam.weight_loss()
    cam.activity()
    cam.total_num_weigh_ins()
    cam.betweenness()
    cam.n_weight_loss()
    cam.degree()
    cam.pagerank()
    cam.vitality()
    cam.clustering()
    cam.triangles()

    output_file = cf.split("/")[0:-1]+[str(cf.strip().rsplit("_")[2][-2:])+"_points_top"+str(cut_off)+"_cam_summary.csv"]
    print "out file", output_file
    output_file = "/".join(output_file)
    cam.write(output_file)

    cam.write_graph(gf)

