import scipy.stats as stat
from math import *
import random, scipy
from random import gauss, randint
from look_up_table import *
import pylab

dict = look_up_table()

class bootstrap:

    def __init__(self,data,n):
        self.data = data
        self.n = n        
    
    def _average(self,X):
        return sum(X)/float(len(X))
    
    def mean_value(dict, list, property ="percentage_weight_change"):

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
    
    def mean(self,X):
        X = self.values(dict,X)
        return sum(X)/float(len(X))
        
    def _true_value(self,x):
        return sum(X)/float(len(X))
        
    def values(self,dict, list, property ="percentage_weight_change"):
    
        values = []
        for n in list:
            try:
                if abs(float(dict[property][int(n)])<50.0):
                    values.append((float(dict[property][int(n)]))) 
                else: pass
            except ValueError:
                pass
        return values
    
    def frac(self,list,threshold = -5, data=dict):    
        x = self.values(data, list) 
        value = []  
        
        for item in x:
            if item < threshold:
                value.append(item)
        return (float(len(value))/float(len(list)))*100
    
    def sample_wr(self,population, k):
        """Chooses k random elements (with replacement) from a population"""
        n = len(population)
        _random, _int = random.random, int  
        result = [None] * k
        for i in xrange(k):
            j = _int(_random() * n)
            result[i] = population[j]
        return result
    
    def bootstrap(self,statistic, nsamples = 1000):
        """
        Arguments:
           sample - input sample of values
           nsamples - number of samples to generate
           samplesize - sample size of each generated sample
           statfunc- statistical function to apply to each generated sample.
     
        Performs resampling from sample with replacement, gathers
        statistic in a list computed by statfunc on the each generated sample.
        """                                                                 

        if not self.n:
            self.n = len(self.data)
        
        X = []
        for i in range(nsamples):
            resample = self.sample_wr(self.data,self.n)
            x = statistic(resample)
            X.append(x)
        return X
        
    def bootstrapCI(self, statistic, clevel=0.975, N=1000, n=None):
        """Compute bootstrap confidence interval for real-valued statistic."""
        results = self.bootstrap(statistic)
        
        #pylab.hist(results, bins =100)
        #pylab.show()
        try:
            results.sort()
        except:
            results = map(lambda x: x[0], results)
            results.sort()

        print "results", results[25],self._average(results), results[975]
        
        avg = self._average(results)
        print "average for"+str(statistic), avg
        
        print "results +\- for"+str(statistic), (abs(results[975])-abs(avg),abs(avg)-abs(results[25]))
        
         
    
if __name__=='__main__':
    pass
   
