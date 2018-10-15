import itertools
from itertools import combinations
from scipy import stats
import numpy as np
from scipy.stats import ks_2samp
from look_up_table import *
import os, sys
  
'''
Created by Rufaro Mukogo on 2011-05-27.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

This script test the hypothesis that the distributions of the percentage weight chnage for various communities 
are statistically equivalent.

A pairwise ks-test analysis is used to determine if all of these distributions are the statistically the same.
The rejection threshold for the ks-test is initially set at 1%.

The overall p value for the test is determined by the fraction of failed individual tests over the total number of 
pairwise tests.

'''

def mean(x):
    return float(sum(x)) / float(len(x))

def test_means(alpha, filename):
    
    filename = str(filename)

    x = [x.strip().split(";") for x in open(filename)\
        .readlines()]
    x = sum(x,[])
    x = [x.split(",") for x in x]
    
    print "X", x
    
    #This is a list of labels, which need to be converted to a list of real user ids
    comlist = [[int(y) for y in x] for x in x]
    print "size of communities", comlist
    
    look_up = look_up_table()
    comlist_values = [[look_up["percentage_weight_change"][int(n)] for n in x] for x in comlist]
    
    avg_weightloss_per_com = []
    for n in comlist_values:
        n = map(float,n)
        avg_weightloss_per_com.append(mean(n))
    
    print "avg percentage weight change for communities", avg_weightloss_per_com
    #print "number of values",map(len,comlist_values)
    
    communitypairs = itertools.combinations(comlist_values,2)
    p_values = []
    for com in communitypairs:
        D, p = ks_2samp(com[0], com[1])
        p_values.append(p)
    
    counter = 0
    for i in p_values:
        if float(i) < alpha:
            counter = counter + 1
            
    print "number of times that we can reject the null hypothesis that the two distributions are equivalent", counter
    overall_pvalue = counter/float(len(p_values))
    print "confidence level that distributions are equivalent", 1-overall_pvalue

if __name__== "__main__":
    
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass
        
    if len(sys.argv)>1:
        alpha = sys.argv[1]
    else:
       alpha = 0.01
    
    if len(sys.argv)>2:
        filename = sys.argv[2]
    else:
        filename = "./5_points_network_2010/data/list_of_lists_merged_communities_label_csv"
        
    test_means(alpha=alpha,filename=filename)
            
