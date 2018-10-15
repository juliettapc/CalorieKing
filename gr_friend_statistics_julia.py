#! /usr/bin/env python

#from ziggy.GraphReduce import gr_path as grp
#from ziggy.GraphReduce import gr_link_analysis as grl
import networkx as nx
from build_friend_graph_julia import *

ckg = CKGraph()
ckg.build_undirected_graph()
#ckg.get_weight_timeseries()
ckg.build_undirected_graph("quarters")
#ckg.get_weight_timeseries("quarters")
ckg.build_undirected_graph("months")
#ckg.get_weight_timeseries("months")
ckg.build_no_staff_graph()
ckg.build_no_staff_graph("quarters")
ckg.build_no_staff_graph("months")
#ckg.build_directed_graph()
#ckg.build_directed_graph("quarters")
#ckg.build_directed_graph("months")

#Dan's Ziggy testing
#G = nx.read_edgelist("calorie_king_friends_undirected_giant_month0")
#grp.shortest_path(G, name="calorie_king_friends_undirected_giant_month0")
