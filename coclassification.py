import itertools
from heapq import merge
from collections import defaultdict
import pprint

#read if the list of communities from a dat file and then create 

q0 = [[1,2,3],[4,5,6],[9,10,11]]
q1 = [[2,3,4,5],[11,1],[9,10]]

t = merge(q0,q1)


words = []

for q in t:
    words.append(map(lambda x:(min(x),max(x)),itertools.combinations(q,2)))

f = list(itertools.chain.from_iterable(words))

real_words = ["_".join(map(str,x)) for x in f]

d = {}


d = defaultdict(int)
for k in real_words:
    d[k]= d[k]+1

print "d", list(d.items())


