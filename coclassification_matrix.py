import itertools
from heapq import merge
from collections import defaultdict
import pprint
from numpy import *
import pylab

#read if the list of communities from a dat file and then create 

q0 = [[1,2,292],[4,123,6],[9,10,11]]
q1 = [[2,3,4,123],[11,1],[9,10]]

nodelist = merge(q0,q1)
nodelist = list(itertools.chain.from_iterable(nodelist))
unique_nodelist = set(list(sorted(nodelist, reverse=False)))
print "nodelist", nodelist

t = merge(q0,q1)

words = []

for q in t:
    words.append(map(lambda x:(min(x),max(x)),itertools.combinations(q,2)))
      
    f = list(itertools.chain.from_iterable(words))

    real_words = ["_".join(map(str,x)) for x in f]
    
    d = [(x,real_words.count(x)) for x in real_words]

print "dictionary", d
#create the adjacency

print "nodes", nodelist

mapping = {}
j=0

for n in unique_nodelist:
    print n
    mapping[n]=j
    j+=1

pprint.pprint(mapping)
matrix=zeros((len(unique_nodelist),len(unique_nodelist)))

for x in d:
    
    print "x0", x[0].split("_")[0]
    print "x1", x[0].split("_")[1]
    print "w", x[1]
    key_x = int(x[0].split("_")[0])
    key_y = int(x[0].split("_")[1])
    
    matrix[mapping[key_x]][mapping[key_y]] = float(x[1])
    
print matrix


colormap = pylab.cm.Spectral
pylab.matshow(matrix, cmap=pylab.cm.Purples)
#pylab.matshow(matrix, cmap=colormap)
pylab.colorbar()
#savefig('test')
pylab.show()
   
