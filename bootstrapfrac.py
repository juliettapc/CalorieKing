import itertools, sys, os
from itertools import chain
import networkx as nx
from transform_labels_to_nx import *
from look_up_table import *
import random
from numpy import std
from math import sqrt
from scipy import stats

look_up = look_up_table()

class bootstrapfrac:
    
    def __init__(self,set_of_all_samples):      
    
        self.dataset = self._values(set_of_all_samples, "percentage_weight_change")
        
        #print "dataset", self.dataset
        self.pairs = self._pairs(self.dataset)
        
        mean_delta = self._true_mean_difference()    
        frac_delta = self._true_frac_difference()    
        #print "mean difference between pairs", mean_delta
        #print "pairs", self.pairs
        
        
    def _pairs(self, dataset):
        """given a lists of lists , returns the combination of list pairings"""
        return list(itertools.combinations(dataset,2))
    
    def bootstrap   (self,N=1000):
        """ bootstrap algorithm to test for equality of means"""     
        dist_of_stat = []
        
        for p in self.pairs:
          
            population = list(itertools.chain(*p))
            
            k1,k2 = map(len,p)   
            print "k1,k2", k1,k2
            print "p-value for equivalence of fracs", stats.ttest_ind(p[0],p[1])
            statistic = []
                 
            for i in xrange(N):
                statistic.append(self._frac_difference(self._sample_wr(population,k1),\
                self._sample_wr(population,k2)))
                
                #print "statistic", statistic
            dist_of_stat.append(statistic)
    
        return dist_of_stat
        
    def _true_mean_difference(self):
        """calculate the true mean difference between a pair of lists with percentage weight change"""
           
        mean_diff = []   
        for x in self.pairs:
            mean_diff.append(self._mean_difference(x[0],x[1]))                    
        return mean_diff
        
    def _true_frac_difference(self):
        """calculate the true frac difference between a pair of lists with percentage weight change"""
           
        frac_diff = []   
        for x in self.pairs:
            frac_diff.append(self._frac_difference(x[0],x[1]))                    
        return frac_diff
        
    def _mean(self,x):
        return float(sum(x)) / float(len(x))
    
    def _frac(self,list,threshold = -5, data=look_up):    
        value = []  
        
        for item in list:
            if item < threshold:
                value.append(item)
        return (float(len(value))/float(len(list)))*100
        
    def _mean_difference(self,x,y):
        return float(self._mean(x) - self._mean(y))
    
    def _frac_difference(self,x,y):
        
        print "sets to consider", len(x), len(y)
        print "p-value for equivalence of fracions", stats.ttest_ind(x,y)
        return abs(float(self._frac(x) - self._frac(y)))
               
    def _values(self,pair, metric):
        """returns the values for a given metric for each list in the pair"""
        return [[float(look_up[str(metric)][int(n)]) for n in x] for x in pair]
    
    def _sample_wr(self,population, k):
        """Chooses k random elements (with replacement) from a population"""
        n = len(population)
        _random, _int = random.random, int  # speed hack 
        result = [None] * k
        for i in xrange(k):
            j = _int(_random() * n)
            result[i] = population[j]
        return result
        
    def _hypothesis_test(self,x,org_stat):
        value = []
        
        for item in x:
            if item >= org_stat:
                value.append(item)
       
        return (float(len(value))/float(len(x)))
        
    def hypo(self):
        """hypothesis test"""        
        orig_test_statistics = self._true_frac_difference()
        distribs = self.bootstrap()
        
        print "should be 3 distributions", len(distribs)

        values = []
        for i in range(len(distribs)):
            values.append(self._hypothesis_test(distribs[i],orig_test_statistics[i]))
        print "test results fractions", values
        
        return values
    
if __name__== "__main__":
    pass
    
    try:
        import pyscho
        pyscho.full()
    except ImportError:
        pass
    
    #G = nx.read_gml("./master_adherent.gml")
    #G = transform_labels_to_nx(G)
    #Gcc = nx.connected_component_subgraphs(G)[0]
    
    #datasets = [Gcc.nodes(),G.nodes()]
    #obj = bootstrapmeans(datasets)
    #t = obj._true_mean_difference()
    #h = obj.bootstrap()
    #m = obj.hypo()
    
    print "m", m
