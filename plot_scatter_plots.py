
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
def main ():





    what_scatterplot='exp'  # 'exp'   or lin

    if what_scatterplot == 'lin':
        filename_actual_evol="./Results/Scatter_plot_length_slope_lin.dat"
    elif what_scatterplot == 'exp':
        filename_actual_evol="./Results/Scatter_plot_tau_deltaY_exp.dat"


    file=open(filename_actual_evol,'r')

    listX=[]
    listY=[]
  

    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   

    
    for line in lista_lines:  
        
        elements=[]
        items=line.strip('\n').split(' ')
       # print items

        listX.append(float(items[0]))  
        listY.append(float(items[1]))  


    
    if what_scatterplot == 'lin':
        xTitle="Duration segment (days)"
        yTitle="Slope"
    elif what_scatterplot == 'exp':
        xTitle="Tau (days)"
        yTitle="Delta Weight"



    title="" #empty
    subtitle="" #empty


    if what_scatterplot == 'lin':
        filename="./Results/Scatterplot_duration_vs_slope.agr"
    elif what_scatterplot == 'exp':
        filename="./Results/Scatterplot_tau_vs_deltaWeight.agr"
    
    


    scatterplot(listX,listY,xTitle,yTitle,title,subtitle,filename)

    print "\n      printed out:",filename 



######################################

def scatterplot(x_points,y_points,xTitle,yTitle,graphTitle,subTitle,filename):

    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle
    graph.title.size = .9
    graph.subtitle.text = subTitle
    graph.subtitle.size = .7
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = 1.5
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 1
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1.5
    graph.yaxis.ticklabel.char_size = 1
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2

    points = graph.add_dataset(zip(x_points,y_points))
    points.symbol.shape = 1
    points.symbol.color = 2   # perimeter of the symbol
    points.symbol.fill_color = 2  # inside the symbol

    points.line.color = 0   #NO LINE
 
    grace.autoscale()
    grace.write_file(filename)

######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
