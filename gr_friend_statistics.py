#! /usr/bin/env python

#from ziggy.GraphReduce import gr_path as grp
#from ziggy.GraphReduce import gr_link_analysis as grl
"""
gr_friend_statistics.py

Created by Dan McClary on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

A harness script for the CKGraph class -- given a file with candidate UIDs, a CKGraph for the selected users is constructed.

"""
import networkx as nx
import sys
from build_friend_graph import *


if len(sys.argv) > 1:
    candidate_points = str(sys.argv[1])
else:
    candidate_points = "5"
print candidate_points
candidates = open(candidate_points+"_points_network_2010/data/weigh_in_candidates_with_"+candidate_points+"_total_points.dat").readlines()
candidates = candidates[1:]
print candidates[0]
uids = []
for c in candidates:
    uids.append(c.split(",")[1])

ckg = CKGraph()
ckg.build_undirected_graph(duration=None, uids=uids)
#ckg.get_weight_timeseries()
ckg.build_undirected_graph("quarters", uids)
#ckg.get_weight_timeseries("quarters")
ckg.build_undirected_graph("months", uids)
#ckg.get_weight_timeseries("months")
#ckg.build_no_staff_graph()
#ckg.build_no_staff_graph("quarters")
#ckg.build_no_staff_graph("months")
#ckg.build_directed_graph()
#ckg.build_directed_graph("quarters")
#ckg.build_directed_graph("months")

#Dan's Ziggy testing
#G = nx.read_edgelist("calorie_king_friends_undirected_giant_month0")
#grp.shortest_path(G, name="calorie_king_friends_undirected_giant_month0")
