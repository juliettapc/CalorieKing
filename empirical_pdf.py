from collections import defaultdict
import pprint, sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

class EmpiricalCDF:
    
    def __init__(self,x, filename, x_axis ="X", y_axis="Y"):
   
        self.filename = filename
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.d = defaultdict(int)
        self.x = map(int,x)    
        self.x = list(sorted(self.x, reverse=False))        
        self._pdfdata()
        self._pdfplotting()

    def _pdfdata(self):
        for k in self.x:
            self.d[k] += 1
        
        pprint.pprint(self.d)
        print len(self.d.values())
        
        #this is the data for plotting the pdf
        self.plotdata = zip(self.d.keys(),map(lambda x: 1.0*self.d[x]/sum(self.d.values()), self.d.keys()))
        print "data", self.plotdata
        
    def _pdfplotting(self):
    
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
        
        graph.yaxis.set_log()
        graph.xaxis.set_log()
                   
        xmin,xmax,ymin,ymax = 0.80,10000,0.00001,1
       
        graph.set_world(xmin,ymin,xmax,ymax)
        graph.xaxis.set_format('decimal',0)
        
        graph.title.text = str(self.filename)
        graph.title.size = 1.2
        graph.subtitle.size = 1.2
             
        grace.write_file("./"+str(self.filename)+'.agr')   
    
if __name__ == "__main__":
    
    #enter the file with the values for time_in_system
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    if len(sys.argv) > 2:
        x_axis = sys.argv[2]
    
    if len(sys.argv) > 3:
        y_axis = sys.argv[3]
    
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass
        
    x = [x.strip() for x in open(filename).readlines()]
        
    obj = EmpiricalCDF(x, filename)
        
    
        
        
        
