"""
Generator for Network Structure 

"""
import networkx as nx
import random,sys
from math import *
import matplotlib.pyplot as plot
import numpy as np
from networkx import *  
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
from matplotlib.ticker import LogFormatter 
import matplotlib.cm as cm
from matplotlib.numerix import asarray
import networkx_pylab_new as nx1



fh=open("2_points_network/data/friend_graph_all0")
raw_data = []

for line in fh:
  line = line.split()
  raw_data.append((line[0], line[1]))


H = nx.DiGraph() #### For undirected graph use H = nx.Graph()
H.add_edges_from(raw_data)
pos=nx.graphviz_layout(H,prog='neato',args='')

fg=open("2_points_network/data/friend_2_list.dat")

actval = []

for line in fg:
  line = line.split()
  actval.append(float(line[1]))
  maxfac = max(actval)
  minfac = min(actval)

fg=open("2_points_network/data/friend_2_list.dat")

pop = []
nodepos = []
for line1 in fg:
  line1 = line1.split()
  nodepos.append(line1[0])
  pop.append(((float(line1[1]))/(float(maxfac))))
  popmin = min(pop)
  popmax = max(pop)
print popmin, popmax

colors = []
for rank in pop:
    colors.append(plot.cm.Accent(float(rank)))
    

fig = plot.figure(figsize=(10,10))
ax = fig.add_axes((0.0,0.0,1.0,1.0))

#cax = ax.imshow([actval],cmap=cm.jet,norm=LogNorm(vmin=1, vmax=maxfac))

cax = ax.imshow([actval],cmap=cm.Accent)
nx1.draw_networkx_edges(H,pos,edgelist=None,edge_color='k',style='solid',alpha=0.4)
                      
nx1.draw_networkx_nodes(H,pos,nodelist=nodepos,node_size = 300 ,node_color=colors, cmap=plot.cm.Accent)

#nx1.draw_networkx_labels(H,pos,labels=None,font_size=10) ### For labeling the nodes with uid


#formatter=ticker.LogFormatterMathtext()
#colorbar(format=formatter)

plot.rcParams["font.size"] = 12
c=plot.colorbar(cax,orientation='vertical',shrink = 0.75)
    
c.set_label("Total Activity of Users")
plot.axis('off')
plot.show() 



