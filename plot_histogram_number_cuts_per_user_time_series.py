import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
def main ():






    filename_actual_evol="./Results/Distribution_num_segments_per_user.dat"
    file=open(filename_actual_evol,'r')

    listX=[]
    listY=[]
  



    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   

    
    for line in lista_lines:  
        
        elements=[]
        items=line.strip('\n').split(' ')
       # print items

        listX.append(int(items[0]))  
        listY.append(float(items[1]))  
       

  
    xTitle="Number of segments per user"
    yTitle="P(number of segments)"
    title="" #empty
    subtitle="" #empty
    filename="./Results/histogram_num_segments_per_user.png"
    
    
    linegraph(listX,listY,xTitle,yTitle,title,subtitle,filename)

    print "\n      printed out:",filename 
    




############################

def linegraph(x,y,xTitle,yTitle,title,subtitle,filename):

    data = zip(x,y)
    
    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size =1.5
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 1
    graph.xaxis.ticklabel.prec = 0
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1.5 
    graph.yaxis.ticklabel.char_size = 1
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = .9 
    graph.subtitle.text = subtitle
    graph.subtitle.size = .7
   
    
    dataset1 = graph.add_dataset(data)
    dataset1.symbol.shape = 1  # 0: no symbol
    dataset1.symbol.color =2 
    dataset1.symbol.fill_color =2 
    dataset1.symbol.size = 1  

    dataset1.line.color = 2
    graph.legend.box_linestyle=0   # NO legend box

    grace.autoscale()
    grace.write_file(filename) 
    

######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
