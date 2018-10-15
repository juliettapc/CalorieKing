from transform_labels_to_nx import *
import networkx as nx
import statistics
from look_up_table import *
from bootstrap2 import bootstrap
from bootstrapfrac import *
from bootstrapmeans import *

""" 
Created by Rufaro Mukogo on 2011-05-23.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

This script is used to calculate the values of figure 2 in the paper. 
"""

data = look_up_table()
dict = look_up_table()

def mean_value(list,dict=dict, property ="percentage_weight_change"):

    count = 0.0
    for n in list:
        try:
            if abs(float(dict[property][int(n)])<50.0):
                count += float(dict[property][int(n)])
                #print count
            else: pass

        except ValueError:
            pass
    try:
        mean = float(count/len(list))
    except ZeroDivisionError:
        mean = 0
        pass
        
    return mean
    
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
    x = values(data, list) 
    value = []   
    for item in x:
        if item < threshold:
            value.append(item)
            
    return (float(len(value))/float(len(list)))*100


#get information for engaged adherent
ad = [x.split(",")[0] for x in open("./master_adherent.csv").readlines()[1:]]
ad_giant = nx.read_gml("./method3/method3_adherent_giant.gml")
ad_sc = nx.read_gml("./method3/method3_adherent_sc.gml")

ad_giant   = transform_labels_to_nx(ad_giant)
ad_sc      = transform_labels_to_nx(ad_sc)
ad_not_net = [x.strip().split(",")[0] for x in open("./method3/adherent_not_networked_pwl.csv").readlines()]

nonad = [x.split(",")[0] for x in open("./master_nonadherent.csv").readlines()[1:]]
nonad_giant = nx.read_gml("./method3/method3_nonadherent_giant.gml")
nonad_sc = nx.read_gml("./method3/method3_nonadherent_sc.gml")
nonad_not_net = [x.strip().split(",")[0] for x in open("./method3/nonadherent_not_networked_pwl.csv").readlines()]

print "nonad not net, ad not net", len(nonad_not_net), len(ad_not_net)
nonad_giant   = transform_labels_to_nx(nonad_giant)
nonad_sc      = transform_labels_to_nx(nonad_sc)
nonad_giant   = 0

print "eng_nonad_sc", len(nonad_sc)


mean0, median0, stddev0, min0, max0, confidence0 = statistics.stats(values(data, nonad_not_net))
mean1, median1, stddev1, min1, max1, confidence1 = statistics.stats(values(data, nonad_sc))
mean2, median2, stddev2, min2, max2, confidence2 = statistics.stats(values(data, eng_nonad_giant))
mean3, median3, stddev3, min3, max3, confidence3 = statistics.stats(values(data, ad_not_net))
mean4, median4, stddev4, min4, max4, confidence4 = statistics.stats(values(data, ad_sc))
mean5, median5, stddev5, min5, max5, confidence5 = statistics.stats(values(data, ad_giant))

print "means and 95% CIs for (a) and (b) panels"
print 1*-mean0, confidence0, len(nonad_not_net)
print 1*-mean1, confidence1, len(nonad_sc)
print 1*-mean2, confidence2, len(eng_nonad_giant)
print 1*-mean3, confidence3, len(ad_not_net)
print 1*-mean4, confidence4, len(ad_sc)
print 1*-mean5, confidence5, len(ad_giant)

non_ad_not_net_frac  =   frac(list(nonad_not_net))
non_ad_sc_frac       =   frac(list(nonad_sc))
non_ad_giant_frac    =   frac(list(eng_nonad_giant))
ad_not_net_frac      =   frac(list(ad_not_net))
ad_sc_frac           =   frac(list(ad_sc))
ad_giant_frac        =   frac(list(ad_giant))

#error bars for fraction 

obj = bootstrap(list(nonad_not_net), len(nonad_not_net))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(nonad_sc), len(nonad_sc))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(ad_not_net), len(ad_not_net))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(ad_sc), len(ad_sc))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(ad_giant), len(ad_giant)) 
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

test = bootstrapfrac([list(ad_not_net), list(ad_sc),list(ad_giant)])
t = test.hypo()

test = bootstrapfrac([list(nonad_not_net), list(nonad_sc)])
t = test.hypo()

test = bootstrapmeans([list(ad_not_net), list(ad_sc),list(ad_giant)])
t = test.hypo()

test = bootstrapmeans([list(nonad_not_net), list(nonad_sc)])
t = test.hypo()

print "non_ad_not_net_frac, non_ad_sc_frac, non_ad_giant_frac, ad_not_net_frac, ad_sc_frac, ad_giant_frac"
print non_ad_not_net_frac, non_ad_sc_frac, 0, ad_not_net_frac, ad_sc_frac, ad_giant_frac

f = open("./figure2_bottom_panel_homo.dat","w")
print>>f, non_ad_not_net_frac
print>>f, non_ad_sc_frac
#print>>f, non_ad_giant_frac
print>>f, ad_not_net_frac
print>>f, ad_sc_frac
print>>f, ad_giant_frac
f.close()

g = open("./figure2_top_panel_homo.dat","w")
print>>g, 0, -1*mean0, confidence0
print>>g, 1, -1*mean1, confidence1
#print>>g, 2, -1*mean2, confidence2
print>>g, 3, -1*mean3, confidence3
print>>g, 4, -1*mean4, confidence4
print>>g, 5, -1*mean5, confidence5
g.close()

