import networkx as nx
from transform_labels_to_nx import *
import pprint
from look_up_table import *
from heapq import merge
from copy import *
import statistics
from bootstrap2 import bootstrap
from bootstrapfrac import bootstrapfrac
from bootstrapmeans import bootstrapmeans

dict = look_up_table()
data = look_up_table()

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

def frac(list,threshold = -5, data=dict):
   
    x = values(data, list)
    value = []  
    for item in x:
        if item <= threshold:
            value.append(item)
            
    return (float(len(value))/float(len(list)))*100

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

all = map(int,[x.split(",")[0] for x in open("./master_adherent.csv").readlines()[1:]])
master_5 =  all

print "number of users meeting adherence and days conditions", len(all)

overweight_nodes = []
    
for n in master_5:  
    if float(dict["initial_BMI"][n])>25.0 and float(dict["initial_BMI"][n]) <30.0:
        overweight_nodes.append(n)
    else: pass

print "overweightnodes", len(overweight_nodes)

overweight = overweight_nodes

obese_nodes = []
for n in master_5:    
    if float(dict["initial_BMI"][n])>=30.0 :
        obese_nodes.append(n)
    else: pass

print "obese", len(obese_nodes)

obese = obese_nodes

normal_nodes = []
for n in master_5:
    if float(data["initial_BMI"][n])<=25.0 :
        normal_nodes.append(n)
    else: pass

print "normal", len(normal_nodes)

print "should sum to 11,242", len(normal_nodes)+len(obese_nodes)+len(overweight_nodes)

#extract the nodes in engaged and adherent network 
giant = nx.read_gml("./method3/networks/method3_adherent_giant.gml")
giant = nx.connected_component_subgraphs(giant)[0]
giant = transform_labels_to_nx(giant)
sc = nx.read_gml("./method3/networks/method3_adherent_sc.gml")
sc = transform_labels_to_nx(sc)

print "number of small component nodes"
print len(sc)

print "number of giant component nodes"
print len(giant.nodes())

obese = map(int, obese)
overweight = map(int, overweight)

obese_giant = list(set(map(int,obese))&set(map(int,giant.nodes())))
print "obese giant"
print len(obese_giant)

overweight_giant = list(set(map(int,overweight))&set(map(int,giant.nodes())))
print "overweight giant"
print len(overweight_giant)

obese_sc = []
for n in sc.nodes():
    if float(data["initial_BMI"][int(n)]) > 30.0:
        obese_sc.append(n)
    
print "obese sc"
print len(obese_sc)

overweight_sc = []
for n in sc.nodes():
    if float(data["initial_BMI"][int(n)]) > 25.0 and float(data["initial_BMI"][int(n)]) < 30.0:
        overweight_sc.append(n)

print "overweight sc"
print len(overweight_sc)

normal_sc = []
for n in sc.nodes():
    if float(data["initial_BMI"][int(n)]) < 25.0:
        normal_sc.append(n)

#print "normal sc"
#print len(normal_sc)

not_networked_obese = set(obese) - set(list(merge(obese_giant,obese_sc)))
print "obese not_networked"
print len(not_networked_obese)

not_networked_overweight = set(overweight) - set(list(merge(obese_giant,obese_sc)))
print "overweight not_networked"
print len(not_networked_overweight)

#print "overweight networked", len(set(map(int,Gcc.nodes()))|set(sc)&set(overweight))
#print "above number should be equal to overweight_giant + overweight_sc", len(overweight_giant) + len(overweight_sc)

#print "check obese giant average", mean_value(data,obese_giant)


obj = bootstrap(list(not_networked_overweight), len(not_networked_overweight))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(overweight_sc), len(overweight_sc))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(overweight_giant), len(overweight_giant))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(not_networked_obese), len(not_networked_obese))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(obese_sc), len(obese_sc))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

obj = bootstrap(list(obese_giant), len(obese_giant))
d   = obj.bootstrapCI(frac)
b   = obj.bootstrapCI(mean_value)

 
#Significance tests
obj = bootstrapfrac([list(not_networked_overweight), list(overweight_sc),list(overweight_giant)])
d   = obj.hypo()

obj = bootstrapfrac([list(not_networked_obese), list(obese_sc),list(obese_giant)])
d   = obj.hypo()

obj = bootstrapmeans([list(not_networked_overweight), list(overweight_sc),list(overweight_giant)])
d   = obj.hypo()

obj = bootstrapmeans([list(not_networked_obese), list(obese_sc),list(obese_giant)])
d   = obj.hypo()
 




#calculate stats for each set of values
mean0, median0, stddev0, min0, max0, confidence0 = statistics.stats(values(data, not_networked_overweight))
mean1, median1, stddev1, min1, max1, confidence1 = statistics.stats(values(data, overweight_sc))
mean2, median2, stddev2, min2, max2, confidence2 = statistics.stats(values(data, overweight_giant))
mean3, median3, stddev3, min3, max3, confidence3 = statistics.stats(values(data, not_networked_obese))
mean4, median4, stddev4, min4, max4, confidence4 = statistics.stats(values(data, obese_sc))
mean5, median5, stddev5, min5, max5, confidence5 = statistics.stats(values(data, obese_giant))

not_networked_overweight_frac   = frac(not_networked_overweight)
overweight_sc_frac              = frac(overweight_sc)
overweight_giant_frac           = frac(overweight_giant)

not_networked_obese_frac        = frac(not_networked_obese)
obese_sc_frac                   = frac(obese_sc)
obese_giant_frac                = frac(obese_giant)

print "not_networked_overweight_frac,overweight_sc_frac,overweight_giant_frac,\
        not_networked_obese_frac, obese_sc_frac, obese_giant_frac"
print not_networked_overweight_frac,overweight_sc_frac,overweight_giant_frac,\
        not_networked_obese_frac, obese_sc_frac, obese_giant_frac
        
print "Means and confidence intervals for not_networked_overweight,overweight_sc,overweight_giant,\
        not_networked_obese, obese_sc, obese_giant"
    
print 1*-mean0, confidence0
print 1*-mean1, confidence1
print 1*-mean2, confidence2
print 1*-mean3, confidence3
print 1*-mean4, confidence4
print 1*-mean5, confidence5

if __name__=="__main__":
    try:
        import psycho
        pyscho.full()
    except ImportError:
        pass














