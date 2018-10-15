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

#get information for engaged adherent
ad = [x.split(",")[0] for x in open("./master_adherent.csv").readlines()[1:]]

ad_giant = [x.split(",")[0] for x in open("./method3/csv/adherent_giant_pwl.csv").readlines()]
ad_sc = [x.split(",")[0] for x in open("./method3/csv/adherent_sc_pwl.csv").readlines()]
ad_not_net = [x.strip().split(",")[0] for x in open("./method3/csv/adherent_not_networked_pwl.csv").readlines()]

nonad = [x.split(",")[0] for x in open("./master_nonadherent.csv").readlines()[1:]]

nonad_giant = [x.split(",")[0] for x in open("./method3/csv/nonadherent_giant_pwl.csv").readlines()]
nonad_sc = [x.split(",")[0] for x in open("./method3/csv/nonadherent_sc_pwl.csv").readlines()]
nonad_not_net = [x.strip().split(",")[0] for x in open("./method3/csv/nonadherent_not_networked_pwl.csv").readlines()]


#check sizes sections

print "ad_giant, ad_sc, ad_not_net", len(ad_giant), len(ad_sc), len(ad_not_net)
print "nonad_giant, nonad_sc, nonad_not_net", len(nonad_giant), len(nonad_sc), len(nonad_not_net)

mean0, median0, stddev0, min0, max0, confidence0 = statistics.stats(values(data, nonad_not_net))
mean1, median1, stddev1, min1, max1, confidence1 = statistics.stats(values(data, nonad_sc))
mean2, median2, stddev2, min2, max2, confidence2 = statistics.stats(values(data, nonad_giant))
mean3, median3, stddev3, min3, max3, confidence3 = statistics.stats(values(data, ad_not_net))
mean4, median4, stddev4, min4, max4, confidence4 = statistics.stats(values(data, ad_sc))
mean5, median5, stddev5, min5, max5, confidence5 = statistics.stats(values(data, ad_giant))

print "means and 95% CIs for (a) and (b) panels"
print 1*-mean0, confidence0, len(nonad_not_net)
print 1*-mean1, confidence1, len(nonad_sc)
print 1*-mean2, confidence2, len(nonad_giant)
print 1*-mean3, confidence3, len(ad_not_net)
print 1*-mean4, confidence4, len(ad_sc)
print 1*-mean5, confidence5, len(ad_giant)

non_ad_not_net_frac  =   frac(list(nonad_not_net))
non_ad_sc_frac       =   frac(list(nonad_sc))
non_ad_giant_frac    =   frac(list(nonad_giant))
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

obj = bootstrap(list(nonad_giant), len(nonad_giant))
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

test = bootstrapfrac([list(ad_not_net),list(ad_sc),list(ad_giant)])
t = test.hypo()

test = bootstrapfrac([list(nonad_not_net), list(nonad_sc), list(nonad_giant)])
t = test.hypo()

test = bootstrapmeans([list(ad_not_net),list(ad_sc),list(ad_giant)])
t = test.hypo()

test = bootstrapmeans([list(nonad_not_net),list(nonad_sc),list(nonad_giant)])
t = test.hypo()

print "non_ad_not_net_frac, non_ad_sc_frac, non_ad_giant_frac, ad_not_net_frac, ad_sc_frac, ad_giant_frac"
print non_ad_not_net_frac, non_ad_sc_frac, non_ad_giant_frac, ad_not_net_frac, ad_sc_frac, ad_giant_frac


