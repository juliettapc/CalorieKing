import itertools
from heapq import merge
from collections import defaultdict
import pprint,os
from numpy import *
import pylab

#read if the list of communities from a dat file and then create 
path = os.getcwd()+"/5_points_network_2010/data/new_networks/"
all_communities = []

for ii in range(8):
    q = [x.strip().split(";") for x in open(str(path)+"friends_undirected_all_quarter"+str(ii)+"_list_of_communities_csv")]    
    q= sorted([x.strip().split(",") for x in q[0]],key=len, reverse = True)
    
    all_communities.append(q)

#print all_communities


#all_communities = [[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[1,2,3,4],[5,6,7,8],[9,10,11,12]]]

print map(len,all_communities) 
print len(all_communities)

#print all_communities

nodelist = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(all_communities))))
community_lists =list(itertools.chain.from_iterable(all_communities))

unique_nodelist = map(int,list(set(nodelist)))

unique_nodelist = sorted(unique_nodelist, reverse = False)

print "nodelist, unique_nodelist", len(nodelist), len(unique_nodelist)

pairings = []

for q in community_lists:
    pairings.append(map(lambda x:(min(x),max(x)),itertools.combinations(q,2)))

print "hard part is done"

f = list(itertools.chain.from_iterable(pairings))
print "f is done"
joined_pairs = ["_".join(map(str,x)) for x in f]
print "joined pairs are done", len(joined_pairs)
d = defaultdict(int)

for k in joined_pairs:
    d[k]+=1

d = list(d.items())
#d = [(x,joined_pairs.count(x)) for x in joined_pairs]
print "d has been made"

#create the adjacency
mapping = {}

j=0

for n in unique_nodelist:
    print n
    mapping[n]=j
    j+=1

print "mapping is done"

pprint.pprint(mapping)

matrix=zeros((len(unique_nodelist),len(unique_nodelist)))

for x in d:
    
    #print "x0", x[0].split("_")[0]
    #print "x1", x[0].split("_")[1]
    #print "w", x[1]
    key_x = int(x[0].split("_")[0])
    key_y = int(x[0].split("_")[1])
    


    matrix[mapping[key_x]][mapping[key_y]] = matrix[mapping[key_y]][mapping[key_x]]=float(x[1])/4.0
    

colormap = pylab.cm.Spectral
pylab.matshow(matrix, cmap=pylab.cm.Reds)
#pylab.matshow(matrix, cmap=colormap)
pylab.colorbar()
#savefig('test')
pylab.show()

if __name__=="__main__":
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass
