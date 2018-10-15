if __name__ == '__main__':
    pass

from numpy import *
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from look_up_table import *


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
            
            self.median = median(array(self.numbers))
            
            print self.plotdata
            
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
            
            xmin,xmax,ymin,ymax = 0.80,10000,0.00001,1
           
            graph.set_world(xmin,ymin,xmax,ymax)
            graph.xaxis.set_format('decimal',0)
            
            graph.title.text = str(self.filename)
            graph.title.size = 1.2
            graph.subtitle.size = 1.2
            
            grace.write_file(Dir+str(self.filename)+'.agr')


if __name__ == '__main__':
                         
    x = [x.split(",")[0] for x in open("./master_engaged.csv").readlines()[1:]]

    look_up = look_up_table()
    x = map(int, x)

    x = map(int,[look_up["weigh_ins"][n] for n in x])
    print "x", x

    obj = EmpiricalCDF(x, "./","master_engaged_weighins_dist","cumulative\
    distribution", "weigh-ins (wi)",)
    obj.cdf_data()
    obj.cdf_plotting()
