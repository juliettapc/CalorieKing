"""
hexbin is an axes method or pyplot function that is essentially
a pcolor of a 2-D histogram with hexagonal cells.  It can be
much more informative than a scatter plot; in the first subplot
below, try substituting 'scatter' for 'hexbin'.
"""

import numpy as np
import matplotlib.cm as cm
import  matplotlib.pyplot as plt
from matplotlib import mlab as ML
import sys



def main (data_filename,xlabel, ylabel,col1,col2):
    
    
    a_file = open(data_filename,'r')
    data = a_file.readlines()
    a_file.close()
    
    
    dist = []
    prob = []
    deltan = []
    for row in data:
        row = row.split()
        
        dist.append(row[col1])  # x column
        prob.append(row[col2])  # y column
        
        
        prob_ij = map(lambda x: float(x), prob)
        dist_ij = map(lambda x: float(x), dist)
   
    xmin = min(dist_ij)  #or  i can pick the limits manually here
    xmax = max(dist_ij)
    ymin = min(prob_ij)
    ymax = max(prob_ij)
    
    
    gridsize=40
    
    print xmin ,xmax, ymin, ymax
    
    
    plt.ylabel (xlabel, size = 20)
    plt.xlabel(ylabel, size = 20)
    
    plt.hexbin(dist_ij,prob_ij, bins='None',gridsize=gridsize, cmap=cm.jet,mincnt=1)   #hexagonal bins.  
#if bins=None, the color of each hexagon directly corresponds to its count value
#if bins=integer, divide the couts in the specified number of bins
#if bins='log' use a logarithmic color scale
    
#gridsize is the NUMBER of hexagons in the x-direction (=100 by default)
#mincnt=1 to diferenciate in colors between count=0 and count=1

    ax = plt.gca()
    fontsize = 18
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)


#ax.set_xscale('log')
#ax.set_yscale('log')


    plt.axis([xmin, xmax, ymin, ymax])
#plt.title("With a log color scale")
    cb = plt.colorbar()
    cb.set_label('log(N)', size = 18)
    
    plt.show()


####################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_filename = sys.argv[1]

        if len(sys.argv) >2:
            xlabel = sys.argv[2]
            ylabel = sys.argv[3]
        else:
            xlabel = "X"
            ylabel = "Y"

        if  len(sys.argv) >4:
            col1 = int(sys.argv[4])
            col2 = int(sys.argv[5])
        else:
            col1 = 0
            col2 = 1

        main(data_filename,xlabel, ylabel,col1,col2)

    else:
        print "usage: python program.py path/data_file  [xlabel  ylabel  colX colY]"

    
