"""
community_CK_show.py

Created by Satyam Mukherjee on 2011-01-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.

This is a quick way to visualize communities. 
"""
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import string
import random
import numpy as np
from scipy.stats import *
from matplotlib.colors import LogNorm
from operator import itemgetter
from math import pi,sin,cos,sqrt



graph_name = "5_points_network/data/friend_graph_all0.gml"
G = nx.read_gml(graph_name)
#print G.nodes()
marks = ['o','s','^','<','>','v','d','h','p','+'] ## One can overlook this ##

listcom = [[7639, 12441, 13445, 199], [14212, 14156, 2876, 12888, 13269, 3893, 7653, 7591, 4454, 3453, 14113, 7245, 18432, 2830, 10244, 419, 13588, 13639, 10079, 19116, 13069, 2509, 15966, 17747, 2310, 17734, 11340, 8414, 6412, 2707, 10950, 2624, 9516, 10537, 7885, 8204, 19210, 10472, 19029, 13375, 3386, 18519, 19538, 14350, 3407, 16015, 2000, 6972, 1338, 14163, 14357, 1539, 14216, 1685, 8715, 17278, 13632, 2980, 6222, 2571, 12778, 1956, 6787, 11209, 12059, 8538, 8240, 2733, 12280, 7125, 3257, 13652, 9566, 13243, 506, 2819, 11561], [283, 5697, 2658, 12699, 13528, 18052, 1983, 13096, 12687, 2156, 5, 15969, 6235, 14956, 14439, 8258, 2108, 8423, 2909, 13995, 18377, 7784, 16039, 12679, 15964, 3040, 14447, 11010, 8612, 10082, 1932, 14333, 2473, 10883, 9861, 15602, 5538, 2290, 3646, 14130, 2076, 2478, 1989, 10641, 14191, 4346, 3069, 2595, 2904, 9379, 11112, 335, 15912, 2047, 19430, 12985, 10075, 2537, 15695, 19584, 8550, 18983, 2028, 15545, 12945, 7713, 15896, 5478, 3202, 772, 2135, 21, 13561, 1533, 14347, 9229, 172, 2301, 14334], [2966, 3074, 6279, 6746, 14127], [3538, 11027, 12494, 1946, 7295, 5703, 7827, 2204, 2184, 1950, 6521, 13676, 2384, 12543, 11959, 15769, 3326, 6632, 12286, 8480, 10863, 13128, 9526, 2207, 8703, 6675, 2109], [15068, 16348, 13443, 2266, 12627, 2094, 913, 5368, 17410, 8016, 1202, 6753, 15388, 5314, 6249, 18641, 889, 10413, 14053, 13546, 2776, 2339, 5990, 19086, 6398, 2085, 1029, 14218, 4225, 9238, 11651, 14857, 15238, 13544, 3352, 7817, 14027, 12018, 4502, 4868, 13098, 9398, 17682, 3107], [6064, 12251], [13555, 1936, 14343, 8854, 13497, 12657, 2442, 8176, 3059, 13672, 1995, 14110, 2342, 14283, 14293, 4170, 13887, 1953, 3024, 3058, 2137, 15618, 5364, 15728, 8974, 8036, 13036, 1991, 15916, 14291, 2237, 2475, 2499, 2348, 2967, 2891, 1064, 2101, 2375, 15919, 7515, 3294, 2905, 15899, 3254, 15827, 2848, 2141, 15796, 2033, 3065, 15364, 2410, 15372, 2705, 16008, 14205, 3175, 2322, 14555, 3194, 14015, 2996, 3051, 11078, 14119, 2199, 8238, 3191, 10297, 2239, 2489, 2077, 94, 2708, 2872, 2189, 1992, 11792, 3299, 3007, 2004, 10845, 1143], [6340, 3416, 15641], [11240, 9754, 12693, 12041]]


listsort = [[6064, 12251], [6340, 3416, 15641], [7639, 12441, 13445, 199], [11240, 9754, 12693, 12041], [2966, 3074, 6279, 6746, 14127], [3538, 11027, 12494, 1946, 7295, 5703, 7827, 2204, 2184, 1950, 6521, 13676, 2384, 12543, 11959, 15769, 3326, 6632, 12286, 8480, 10863, 13128, 9526, 2207, 8703, 6675, 2109], [15068, 16348, 13443, 2266, 12627, 2094, 913, 5368, 17410, 8016, 1202, 6753, 15388, 5314, 6249, 18641, 889, 10413, 14053, 13546, 2776, 2339, 5990, 19086, 6398, 2085, 1029, 14218, 4225, 9238, 11651, 14857, 15238, 13544, 3352, 7817, 14027, 12018, 4502, 4868, 13098, 9398, 17682, 3107], [14212, 14156, 2876, 12888, 13269, 3893, 7653, 7591, 4454, 3453, 14113, 7245, 18432, 2830, 10244, 419, 13588, 13639, 10079, 19116, 13069, 2509, 15966, 17747, 2310, 17734, 11340, 8414, 6412, 2707, 10950, 2624, 9516, 10537, 7885, 8204, 19210, 10472, 19029, 13375, 3386, 18519, 19538, 14350, 3407, 16015, 2000, 6972, 1338, 14163, 14357, 1539, 14216, 1685, 8715, 17278, 13632, 2980, 6222, 2571, 12778, 1956, 6787, 11209, 12059, 8538, 8240, 2733, 12280, 7125, 3257, 13652, 9566, 13243, 506, 2819, 11561], [283, 5697, 2658, 12699, 13528, 18052, 1983, 13096, 12687, 2156, 5, 15969, 6235, 14956, 14439, 8258, 2108, 8423, 2909, 13995, 18377, 7784, 16039, 12679, 15964, 3040, 14447, 11010, 8612, 10082, 1932, 14333, 2473, 10883, 9861, 15602, 5538, 2290, 3646, 14130, 2076, 2478, 1989, 10641, 14191, 4346, 3069, 2595, 2904, 9379, 11112, 335, 15912, 2047, 19430, 12985, 10075, 2537, 15695, 19584, 8550, 18983, 2028, 15545, 12945, 7713, 15896, 5478, 3202, 772, 2135, 21, 13561, 1533, 14347, 9229, 172, 2301, 14334], [13555, 1936, 14343, 8854, 13497, 12657, 2442, 8176, 3059, 13672, 1995, 14110, 2342, 14283, 14293, 4170, 13887, 1953, 3024, 3058, 2137, 15618, 5364, 15728, 8974, 8036, 13036, 1991, 15916, 14291, 2237, 2475, 2499, 2348, 2967, 2891, 1064, 2101, 2375, 15919, 7515, 3294, 2905, 15899, 3254, 15827, 2848, 2141, 15796, 2033, 3065, 15364, 2410, 15372, 2705, 16008, 14205, 3175, 2322, 14555, 3194, 14015, 2996, 3051, 11078, 14119, 2199, 8238, 3191, 10297, 2239, 2489, 2077, 94, 2708, 2872, 2189, 1992, 11792, 3299, 3007, 2004, 10845, 1143]]

#sorted(listcom,key=len)

#print listcom
H=nx.Graph()

ynode = []
nweigtchange = []
nweigtchangep = []
nweigtchangem = []
nweigtchangez = []
activity = []
colorp = []
colorm = []
colorz = []
posnodes = []
posnodesp = []
posnodesm = []
posnodesz = []
pairsp = []
pairsm = []
pairsz = []
for com in listsort :

 xnode = []
 
 for comnodes in com :
 
  for node in G.nodes(data=True) :

    if int(node[1]['label']) == int(comnodes) :

     if float(node[1]['n_weight_change']) > 0 :
#       posnodesp.append(int(node[1]['id']))
       nweigtchangep.append((float(node[1]['n_weight_change'])))
       pairsp.append(((float(node[1]['n_weight_change'])), int(node[1]['id'])))
       pairsp.sort()

     if float(node[1]['n_weight_change']) < 0 :
#       posnodesm.append(int(node[1]['id']))
       nweigtchangem.append((float(node[1]['n_weight_change'])))
       pairsm.append(((float(node[1]['n_weight_change'])), int(node[1]['id'])))
       pairsm.sort()

     if float(node[1]['n_weight_change']) == 0 :
#       posnodesz.append(int(node[1]['id']))
       nweigtchangez.append((float(node[1]['n_weight_change'])))
       pairsz.append(((float(node[1]['n_weight_change'])), int(node[1]['id'])))
       pairsz.sort()

     posnodes.append(int(node[1]['id']))
     xnode.append(((float(node[1]['n_weight_change'])), int(node[1]['id'])))
     xnode.sort()
#      xactivity.append(np.log(float(node[1]['activity']))/np.log(4420.0))
     activity.append((float(node[1]['activity'])))
     nweigtchange.append((float(node[1]['n_weight_change'])))

     bunch = [int(node[1]['id'])]+G.neighbors(int(node[1]['id']))
     Gprime = G.subgraph(bunch)
     H.add_edges_from(Gprime.edges())
      
 ynode.append(xnode)

ynode1 = []
for n in ynode :
   xnode1 = []
   for n1, s1 in n :
    xnode1.append(s1)
    print n1, s1
   ynode1.append(xnode1)


len_count = 0.
maxweightchange = max(nweigtchange)
minweightchange = min(nweigtchange)

print minweightchange, maxweightchange

popweightp = []
for pop, node in pairsp :
  popweightp.append(float(pop+abs(minweightchange))*1.0/float(maxweightchange+abs(minweightchange)))
  posnodesp.append(node)

popweightm = []
for pop, node in pairsm :
  popweightm.append(float(pop+abs(minweightchange))*1.0/float(maxweightchange+abs(minweightchange)))
  posnodesm.append(node)

popweightz = []
for pop, node in pairsz :
  popweightz.append(float(pop+abs(minweightchange))*1.0/float(maxweightchange+abs(minweightchange)))
  posnodesz.append(node)

### Creating my own node positioning !!!

fig = plt.figure(figsize=(10,10))
ax = fig.add_axes((0.0,0.0,1.0,1.0))

nshells=len(ynode1)
size = []
for shell in ynode1:
  size.append(len(shell))
maxshellsize = max(size)
minshellsize = min(size)

pos={}
dim = 2
if len(ynode1[0])==1:
   initial_radius=0.0 # single node at center
else:
   initial_radius=1.0

for s in range(nshells):
#    print s, listcomattr[s][0], listcomattr[s][1]
    t = 0
    slist = [n for n in ynode1[s] if H.has_node(n)]
    print s, len(slist)

    if len(slist) > 10 :
      r = float(2*(s-1))
      dt = 2*pi/len(slist)
#      print r
      for n in slist:
        p=dim*[0.0]
        p[0]=r*cos(t)
        p[1]=r*sin(t)
        pos[n]=np.array(p)
        t=t+dt
     

    if len(slist) > 2 and len(slist) <= 10:
      r = float(2*s + 16)
#      print r
      dt = 2*pi*minshellsize*1.0/(maxshellsize)
      for n in slist:
        p=dim*[0.0]
        p[0]=r*cos(((1)**(1*s))*t)
        p[1]=r*sin(((1)**(1*s))*t)
        pos[n]=np.array(p)
        t=t+dt

    if len(slist) == 2 :
      r = float(26*(s+1))
#      print r
      dt = 2*pi*len(slist)*1.0/(maxshellsize)
      for n in slist:
        p=dim*[0.0]
        p[0]=r*cos(((1)**s)*t)
        p[1]=r*sin(((1)**s)*t)
        pos[n]=np.array(p)
        t=t+dt


for i in pos :
 pos[i][0] = pos[i][0] * 200.0
 pos[i][1] = pos[i][1] * 200.0

### Node position Done !!!!

for colors in popweightp :
         colorp.append(plt.cm.jet(float(colors)))

for colors in popweightm :
         colorm.append(plt.cm.jet(float(colors)))

for colors in popweightz :
         colorz.append(plt.cm.jet(float(colors)))

### Coloring the nodes Done !!


cax = ax.imshow([nweigtchange],cmap=plt.cm.jet)

nx.draw_networkx_nodes(H, pos, posnodesp, node_size = 100, node_shape='s', node_color = colorp, cmap=plt.cm.jet )
nx.draw_networkx_nodes(H, pos, posnodesm, node_size = 100, node_shape='o', node_color = colorm, cmap=plt.cm.jet )
nx.draw_networkx_nodes(H, pos, posnodesz, node_size = 100, node_shape='o', node_color = colorz, cmap=plt.cm.jet )
nx.draw_networkx_edges(H, pos, alpha=0.35)

#nx.draw_networkx_labels(H,pos,labels=None,font_size=15)

plt.rcParams["font.size"] = 12
c1=plt.colorbar(cax,orientation='vertical',shrink = 0.55)
c1.set_label("Normalized weight change for Users")
plt.title('Each shell represents a community')
plt.axis('off')
plt.show()
