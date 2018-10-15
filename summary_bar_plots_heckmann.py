from transform_labels_to_nx import *
import networkx as nx
import statistics
from look_up_table import *
from bootstrap_module import *
from bootstrapfrac import *
from bootstrapmeans import *

""" 
Created by Rufaro Mukogo on 2011-05-23.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

This script is used to calculate the values of figure 2 in the paper. 
"""

data = look_up_table()
dict = look_up_table()

def mean_value(x):
    return float(sum(x)/len(x))
        
def values(dict, list, property ="percentage_weight_change"):

    values = []
    for n in list:
        try:
            if abs(float(dict[property][int(n)])<50.0):
                values.append((float(dict[property][int(n)]))) 
            else: pass
        except ValueError:
            pass
    return values

def frac(list,threshold = -5, data=data):
    value = []   
    for item in x:
        if item < threshold:
            value.append(item)
            
    return (float(len(value))/float(len(list)))*100


#get information for engaged adherent
all = map(float,[x.strip("\n").split(",")[0] for x in \
open("./network_all_users/master_csv_all_pwc.csv").readlines()[1:]])

not_net = map(float,[x.strip("\n").split(",")[0] for x in\
open("./network_all_users/master_not_net_pwc.csv").readlines()[1:]])

net = map(float,[x.strip("\n").split(",")[0] for x in \
open("./network_all_users/master_net_pwc.csv").readlines()[1:]])

full = nx.read_gml("./network_all_users/full_network_all_users.gml")

gc = map(float,[x.strip("\n").split(",")[0] for x in \
open("./network_all_users/master_csv_gc_wts.csv").readlines()[1:]])

sc = map(float,[x.strip("\n").split(",")[0] for x in \
open("./network_all_users/master_csv_sc_wts.csv").readlines()[1:]])

mean0, median0, stddev0, min0, max0, confidence0 = statistics.stats(all)
mean1, median1, stddev1, min1, max1, confidence1 = statistics.stats(not_net)
mean2, median2, stddev2, min2, max2, confidence2 = statistics.stats(net)
mean3, median3, stddev3, min3, max3, confidence3 = statistics.stats(sc)
mean4, median4, stddev4, min4, max4, confidence4 = statistics.stats(gc)
#mean5, median5, stddev5, min5, max5, confidence5 = statistics.stats(sc)

print "means and 95% CIs for (a) and (b) panels"
print 1*-mean0, confidence0, len(all)
print 1*-mean1, confidence1, len(not_net)
print 1*-mean2, confidence2, len(net)
print 1*-mean3, confidence3, len(sc)
print 1*-mean4, confidence4, len(gc)
#print 1*-mean5, confidence5, len(ad_giant)

_all  	   =   frac(list(all))
_net       =   frac(list(net))
_not_net   =   frac(list(not_net))
_small     =   frac(list(sc))
_giant     =   frac(list(gc))

#error bars for fraction 

obj = bootstrap(list(all), len(all))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(not_net), len(not_net))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(net), len(net))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(sc), len(sc))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(gc), len(gc)) 
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

test = bootstrapmeans([list(all), list(not_net),list(net), list(sc), list(gc)])
t = test.hypo()

#test = bootstrapfrac([list(nonad_not_net), list(nonad_sc)])
#t = test.hypo()

#test = bootstrapmeans([list(ad_not_net), list(ad_sc),list(ad_giant)])
#t = test.hypo()

#test = bootstrapmeans([list(nonad_not_net), list(nonad_sc)])
#t = test.hypo()


