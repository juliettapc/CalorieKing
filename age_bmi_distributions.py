import networkx as nx
from read_a_gml import *
from look_up_table import *
import sys
from numpy import *
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from GraphRandomization import *
from scipy import stats
import numpy as np
from scipy.stats import ks_2samp
import itertools
 
look_up = look_up_table()

class EmpiricalCDF:
    
    def __init__(self, datalist, Dir, filename,y_axis = 'cumulative probability density',x_axis = 'x_axis'):
        
        
        ''' 
        class that holds a list of data and returns an empirical cdf 
        defined as p(X>=x). The data are return as a list of tuple (x,y)
        with x representing the value of the variable and y the cumulative probability.

        The plotting method returns a pygrace plot of the cdf toa specified location
        
        ''' 
        
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.n = len(datalist)
        self.datalist = datalist
        self.filename = filename
        
        print self.datalist, self.n

        self.Dir = Dir
        self.filename = filename
        
    def cdf_data(self):
            
            data = self.datalist
            self.plotdata = []
            
            try:
                for i in range(data):
                    if data[i+1]<data[i]:
                        raise ValueError
            except:
                pass
    
            self.denominator = self.n
            
            self.bar = dict((i,data.count(i)) for i in set(data))
            self.barlist = [(k,v) for k,v in self.bar.iteritems()]
            
            self.numbers = [item[0] for item in self.barlist]
            
            self.numbers.sort()
            
            self.list_of_counts = [item[1] for item in self.barlist]
            
            self.cumsum =[]
            self.cumsum.append(0.0)
            
            for x in self.list_of_counts:
                self.cumsum.append(self.cumsum[-1] + x if self.cumsum else x)
            
            last_term = self.cumsum[-1]
            
            self.numerator = [last_term-item for item in self.cumsum]
            
            self.probabilities = [item/last_term for item in self.numerator]
            self.plotdata = zip(self.numbers,self.probabilities)
            
            
            #print len(self.plotdata)
            
            return self.plotdata


    def cdf_plotting(self):
    
            Dir = self.Dir
            
            data = self.plotdata

            grace = Grace(colors=ColorBrewerScheme('Paired'))
            graph = grace.add_graph()
            
            graph.set_labels(str(self.x_axis),(self.y_axis))
            
            dataset1 = graph.add_dataset(data)
            
            dataset1.line.type = 0
            dataset1.line.color = 1
            dataset1.line.linewidth = 4.0
            dataset1.symbol.fill_color = 'white'
            dataset1.symbol.shape = 1
            dataset1.symbol.size = 0.7
            dataset1.symbol.color = 1
            dataset1.symbol.color = 'black' 
            
            graph.legend.box_color  = 0
            graph.legend.char_size  = 0.85
            graph.legend.loc        = (0.55,0.80)
            
            graph.autoscaley()
            graph.xaxis.set_log()
            
            #graph.autoscaley()
            #graph.autoscalex()
            
            xmin,xmax,ymin,ymax = 0.80,100,0.0001,1
           
            graph.set_world(xmin,ymin,xmax,ymax)
            graph.xaxis.set_format('decimal',0)
            
            graph.title.text = str(self.filename)
            graph.title.size = 1.2
            graph.subtitle.size = 1.2
            
            grace.write_file(Dir+str(self.filename)+'.agr')     

class distributions:
    
    def __init__(self, G, outdir):
    
        
        self.G = read_a_gml(G)
        self.outdir = outdir
        
    def age(self, G):
        
        self.age_diff = []
        for u,v in G.edges_iter():
            if float(look_up["age"][int(u)]) <100:
                if float(look_up["age"][int(v)]) > 10:
                    t = float(look_up["age"][int(u)]) 
                    s = float(look_up["age"][int(v)])       
                    self.age_diff.append(abs(s-t))
            
        f = open("./method3_50/interim/age_differences_sc.csv", "w")
        
        for r in self.age_diff:
            print>>f, r
        f.close()
        
        return self.age_diff
        
    def ibmi(self, G):
        self.ibmi_diff = []
        for u,v in G.edges_iter():

            if float(look_up["initial_bmi"][int(u)]) <70:
                if float(look_up["initial_bmi"][int(v)]) > 0:
                    t = float(look_up["initial_bmi"][int(u)]) 
                    s = float(look_up["initial_bmi"][int(v)])       
                    self.ibmi_diff.append(abs(s-t))

        print self.ibmi_diff

        f = open("./method3_50/interim/ibmi_differences_sc.csv", "w")
        
        for r in self.ibmi_diff:
            print>>f, r
        f.close()
        
        return self.ibmi_diff
             
    def randomization(self):
    
    
        base_disrib = map(int, self.G.nodes())
        base_distrib = itertools.combinations(*base_distrib)
        
        self.base_age_diff = []
        
        for pair in base_distrib:
            for u,v in pair:       
                if float(look_up["age"][int(u)]) <70:
                        if float(look_up["age"][int(v)]) > 0:
                            t = float(look_up["age"][int(u)]) 
                            s = float(look_up["age"][int(v)])       
                        
                            self.base_age_diff.append(abs(s-t))
            
        
        print "ks test between network age distribution and fully connected network",\
            
        
        
        dist_D_age = []
        dist_D_ibmi = []
        
        for N in xrange(1000):   
            
            G = mc_randomize_m(self.G)
            
            age = self.age(G)
            ibmi = self.ibmi(G)
            
            age_ks_test = ks_2samp(self.age_diff,age)
            D_age = age_ks_test[1]

            ibmi_ks_test = ks_2samp(self.ibmi_diff,ibmi)
            D_ibmi = ibmi_ks_test[1]
            
            dist_D_age.append(D_age)
            dist_D_ibmi.append(D_ibmi)
            
            dist_D_age.sort()
            dist_D_ibmi.sort()
            
        return dist_D_age, dist_D_ibmi
        
    def main(self):
        
        ibmi = self.ibmi(self.G)
        age = self.age(self.G)
        
        #age_obj = EmpiricalCDF(age, self.outdir, "age_difference_distribution_",y_axis = 'Cumulative probability density',x_axis = 'age difference')
        #age_obj.cdf_data()
        #age_obj.cdf_plotting()
        
        #ibmi_obj = EmpiricalCDF(ibmi, self.outdir, "ibmi_difference_distribution_sc",y_axis = 'Cumulative probability density',x_axis = 'initial BMI difference')
        #ibmi_obj.cdf_data()
        #ibmi_obj.cdf_plotting()
        
        dist_D_age, dist_D_ibmi = self.randomization()
        
        print "p-values dist_D_age", dist_D_age
        
if __name__ == "__main__":
    
    try:
        import pyscho
        pyscho.full()
    except ImportError:
        pass
    
    if len(sys.argv) > 1:
        G = sys.argv[1]
    
    if len(sys.argv) > 2:
        outdir = sys.argv[2]
   
    print sys.argv

    obj = distributions(G,outdir)
    obj.main()
    
    
