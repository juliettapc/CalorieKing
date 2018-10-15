'''
Created on Nov 8, 2010

@author: rufaro
'''

if __name__ == '__main__':
    pass

import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def histogram_plotting(datalist, path, filename, x_axis, y_axis):
   
    grace = Grace(colors=ColorBrewerScheme('Paired'))
    graph = grace.add_graph()
    
    graph.set_labels(str(x_axis),str(y_axis))
    
    dataset1 = graph.add_dataset(datalist)

    dataset1.line.type =0 
    dataset1.line.color = 7
    dataset1.line.linewidth = 4.0
    dataset1.symbol.fill_color = 'white'
    dataset1.symbol.shape = 1
    
    graph.legend.box_color  = 0
    graph.legend.char_size  = 0.85
    graph.legend.loc        = (0.55,0.80)

    xmin,ymin,xmax,ymax = graph.get_world()

    graph.set_world(0,0.001,200,1000)

    graph.yaxis.set_log()
    graph.autoscalex()
    
    graph.xaxis.set_format('decimal',0)

    grace.write_file(str(path)+str(filename)+'_histogram_points.agr')
    
    
