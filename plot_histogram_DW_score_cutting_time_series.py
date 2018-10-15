import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
def main ():






    filename1="./Results/Distribution_DW_scores_lin_segments.dat"
  #  filename2="./Results/Distribution_DW_scores_const_segments.dat"
    filename3="./Results/Distribution_DW_scores_exp_segments.dat"


    list_filenames=[filename1,filename3]



    xs=[]
    ys=[]
    for filename in list_filenames:

        file=open(filename,'r')       
        lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   
        listX=[]
        listY=[]
  



    
        for line in lista_lines:  
            
            elements=[]
            items=line.strip('\n').split(' ')
# print items
            
            listX.append(float(items[0]))  
           # listY.append(float(items[1]))    # Bin_count/(Total_count*Bin_size)
            listY.append(float(items[5]))    #Bin_count/Total_count
       
        xs.append(listX)   
        ys.append(listY)
  


    list_yLegends=["Lin. segments","Exp. segments"]

    xTitle="DW score"
    yTitle="P(DW score)"
    title="" #empty
    subtitle="" #empty
    filename="./Results/Distribution_DW_score_lin_exp_segments.eps"

    colors = [1,2,3]
    

    realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename,colors)
    
    print "\n      printed out:",filename 

  



############################

####################################


def realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename, colors):
#ys is a list of y-series
#xs is a list of x-series
    
   

#1:black
#2:red
#3: light green
#4:dark blue
#5:yellow
#6:light brown
#7:grey
#8:purple
#9:cyan
#10:pink
#11:orange
#12: purple2
#13:maroon
#14:cyan2
#15:dark green

    grace = Grace()
    graph = grace.add_graph()
   # graph.title.text = graphTitle 
    graph.title.size = 1.2
    #graph.subtitle.text = subtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size =  2
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 2
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 2
    graph.yaxis.ticklabel.char_size = 2
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2


   
   

    for [i,y] in enumerate(ys):   # enumerate([j,u,l,i,a]) returs a list of tuples: [(0,j),(1,u),(2,l),(3,i),(4,a)]
 # zip([a,b,c],[1,2,3]) returns  [(a,1),(b,2),(c,3)]
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])
        dataset.symbol.shape = 1
        dataset.symbol.size = 0.7
        dataset.symbol.color = colors[i]
        dataset.symbol.fill_color = colors[i]
        dataset.line.color = colors[i]
        if "Training" in list_yLegends[i]:
            dataset.symbol.fill_color=0

    graph.legend.char_size = 1.
    graph.legend.box_linestyle=0   # NO legend box
    graph.legend.loc = (.8,.8)  # coordinate system from 0 to 1 for both axes (NOT world coordenates, but scaled)


  

   

    grace.autoscale()
    grace.write_file(filename)





######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
