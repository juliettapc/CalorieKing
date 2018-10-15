#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
from matplotlib import pylab as P
import os
from transform_labels_to_nx import *
from pylab import *

path = os.getcwd()
graph_file = "friend_graph_all_5_2010.gml"
G = nx.read_gml(str(path)+"/5_points_network_2010/data/"+str(graph_file))


G = transform_labels_to_nx(G)
Gcc= nx.connected_component_subgraphs(G)[0]

print "Gcc", len(Gcc)

cuts = ["200","300","400","500"]
dist_list = []

for ct in cuts:

	distrib = []
	for n in Gcc.nodes():
		if int(Gcc.node[n]["time_in_system"])>=int(ct):
			distrib.append(float(Gcc.node[n]["weight_change"]))
	print "distrib", len(distrib)
	dist_list.append(distrib)


P.subplot(221)
n, bins, patches = P.hist(dist_list[0], bins=100, normed=0, histtype='bar', rwidth=0.8)
title("time in system greater than 200 days")
ylabel("Probability Density")

P.subplot(222)
n, bins, patches = P.hist(dist_list[1],bins=100, normed=0, histtype='bar', rwidth=0.8)
title("time in system greater than 300 days")


P.subplot(223)
n, bins, patches = P.hist(dist_list[2], bins = 75, normed=0, histtype='bar', rwidth=0.8)
title("time in system greater than 400 days")
ylabel("Probability Density")
xlabel("change in weight")


P.subplot(224)
n, bins, patches = P.hist(dist_list[3], bins=50, normed=0, histtype='bar', rwidth=0.8)
title("time in system greater than 500 days")
xlabel("change in weight")
P.show()



