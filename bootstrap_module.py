import scipy.stats as stat
from math import *
import random, scipy
from random import gauss, randint
from look_up_table import *

dict = look_up_table()

class bootstrap:

    def __init__(self,data,n):
        self.data = data
        self.n = n        
    
    def _average(self,X):
        return sum(X)/float(len(X))
    
    def mean(self,X):
        return sum(X)/float(len(X))
        
   
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
        
        try:
            results.sort()
        except:
            results = map(lambda x: x[0], results)
            results.sort()
        
        avg = self._average(results)
        
        print "results for plotting in grace  avg: %g ub: %g lb:%g for function: %s"%\
        (avg,abs(results[975])-abs(avg),abs(avg)-abs(results[25]), str(statistic.__name__))
        
        return (avg,abs(results[975])-abs(avg),abs(avg)-abs(results[25]))
         
    
if __name__=='__main__':
    pass
   
