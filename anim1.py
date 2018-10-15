import networkx as nx
from collections import defaultdict
from copy import copy
from matplotlib import pyplot

fh=open("5_points_network/data/friend_graph_all0")
raw_data = []

for line in fh:
  line = line.split()
  raw_data.append((line[0], line[1]))


G = nx.Graph() #### For undirected graph use H = nx.Graph()
G.add_edges_from(raw_data)
layout=nx.graphviz_layout(G,prog='neato',args='')

metric = nx.betweenness_centrality(G) # or whatever metric you want

sorted_metric = metric.values()
sorted_metric.sort()
sorted_metric.reverse()

reverse_metric = defaultdict(list)
pairs = zip(metric.values(), metric.keys())
for p in pairs:
    reverse_metric[p[0]].append(p[1])

layout = nx.spring_layout(G)
node = reverse_metric[sorted_metric[0]][0]
#build your subgraph
bunch = [node]+G.neighbors(node)
Gprime = G.subgraph(bunch)

master_layout = copy(layout)
for key in layout.keys():
  if key not in bunch:
    continue

nx.draw(Gprime, pos=layout)
pyplot.show()
