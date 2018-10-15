import itertools
from heapq import merge
from collections import defaultdict
import pprint,os, sys
from numpy import *
import pylab
import numpy
from sort_matrix import main
from matplotlib.backends.backend_pdf import PdfPages


"""

This script is used to generate the co-occurrence matrix for the networks
in different time slices over a two year period from 2009-2010 in the CalorieKing friendship network.
The co-occurence is defined as the number of time that two nodes occur in the same subgroup (community or role)
in each of the n number of time slices.

This matrix can then be sorted by some algorithm to show grouping and structure

Created by Rufaro Mukogo on 2011-03-30.
Copyright (c) 2011 __Northwestern University. All rights reserved.

"""

def co_occurrence_matrix(path,period):

    print "Computing the cooccurrence matrix for %s network slices" %(period)

    path = path
    period = period

    all_communities = []

    if period =="quarter":
        r = 8
    elif period =="sixmonths":
        r = 4

    for ii in range(r):
<<<<<<< local
        q = [x.strip().split(";") for x in open(str(path)+"friends_undirected_all_"+str(period)+str(ii)+"_list_of_communities_csv")]
        q= sorted([x.strip().split(",") for x in q[0]],key=len, reverse = True)

=======
        q = [x.strip().split(";") for x in\
        open(str(path)+"friends_undirected_all_"+str(period)+str(ii)+"_list_of_communities_csv")]    
       
        q = sorted([x.strip().split(",") for x in q[0]],key=len, reverse = True)
        
>>>>>>> other
        all_communities.append(q)

    #print all_communities
    #all_communities = [[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[1,2,3,4],[5,6,7,8],[9,10,11,12]]]

    print "size of all communities", map(len,all_communities)
    print "number of total communities", len(all_communities)

    nodelist = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(all_communities))))
    community_lists =list(itertools.chain.from_iterable(all_communities))
    unique_nodelist = map(int,list(set(nodelist)))
    unique_nodelist = sorted(unique_nodelist, reverse = False)

    print "nodelist, unique_nodelist", len(nodelist), len(unique_nodelist)

    pairings = []

    # get all the possible co-occuring pairs
    for q in community_lists:
        pairings.append(map(lambda x:(min(x),max(x)),itertools.combinations(q,2)))

    #flatten the list of list of tuples into one large list of tuples eg (1,233) when 1_233 occur together
    f = list(itertools.chain.from_iterable(pairings))

    # create a "word" i.e a unique string for each possible pairing which can thenbe counted
    joined_pairs = ["_".join(map(str,x)) for x in f]

    #use defaultdict to count the number of possible pairings
    d = defaultdict(int)

    for k in joined_pairs:
        d[k]+=1

    d = list(d.items())

    #create a mapping for the nodes so there are no gaps and the matrix
    mapping = {}

    j=0
    for n in unique_nodelist:
        mapping[n]=j
        j+=1

    #create the empty matrixmatrix
    matrix=zeros((len(unique_nodelist),len(unique_nodelist)))

    for x in d:
        #print "x0", x[0].split("_")[0]
        #print "x1", x[0].split("_")[1]
        #print "w", x[1]
        key_x = int(x[0].split("_")[0])
        key_y = int(x[0].split("_")[1])

       matrix[mapping[key_x]][mapping[key_y]] = matrix[mapping[key_y]][mapping[key_x]]=float(x[1])/r

    return matrix

if __name__=="__main__":
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass

    if len(sys.argv)>1:
        period = sys.argv[1]
    else:
        period = "sixmonths"

    if len(sys.argv)>2:
        path = sys.argv[2]
    else:
        path = os.getcwd()+"/"

    if period =="quarter":
        path = path+"5_points_network_2010/data/new_networks/"+str(period)+"s"+"/"+str(period)+"s"+"/"

        path = path+"5_points_network_2010/data/new_networks/"+str(period)+"s/"
    
    elif period == "sixmonths":
        path = path+"5_points_network_2010/data/new_networks/"+str(period)+"/"


    matrix = co_occurrence_matrix(path=path,period=period)

    filename = str(path)+"/"+'co_occurence_matrix_unsorted_'+str(period)
    
    filename = str(path)+"/"+'co_occurence_matrix_R1_unsorted_'+str(period)
    numpy.savez(str(filename), matrix)

    #plot heat map
    pp = PdfPages(filename)
    colormap = pylab.cm.Spectral
    pylab.matshow(matrix, cmap=pylab.cm.Reds)
    pylab.colorbar()
    pp.savefig()
    pylab.show()








