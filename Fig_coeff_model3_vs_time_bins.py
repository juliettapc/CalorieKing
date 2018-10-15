
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():


    xs=[]
    ys=[]

    
### Actual evolution :



    coeff='alpha3'   #alpha3'  # or beta3


    list_of_list_data=[]

    list_yLegends=[]
   

    list_bmi_groups_included=[1,2,5,9]

    for i in (list_bmi_groups_included):
        i+=1   # bmi_group

        list_yLegends.append("bmi group "+str(i))

        filename_coeff="./analysis_time_bins_bmi_groups/coeff_model3_group"+str(i)+".dat"
        file1=open(filename_coeff,'r')

        lista_lines=file1.readlines()   # each element is a line of the file  STRING TYPE!!   



        listX=[]
        
        listY1=[]
        listY2=[]
        listY3=[]
        listY4=[]
        
        listXYsd=[]


        for line in lista_lines:     
            trios=[]               
            items=line.strip('\n').split(' ')

            trios.append(int(items[0])) # time bin 

            if  coeff=='alpha3':
                    
              
          #  trios.append(float(items[1]))   # cte 
           # trios.append(float(items[2]))  # sd cte
                trios.append(float(items[3]))   # alpha 
                trios.append(float(items[4])) # sd alpha

            elif  coeff=='beta3':

                trios.append(float(items[5]))   # beta 
                trios.append(float(items[6])) # sd beta

            else:
                print "wrong coeff name"
                exit()
    
            listXYsd.append(trios)
 
  
        list_of_list_data.append(listXYsd)

     



        


   
    xTitle="time bin" 

    if  coeff=='alpha3':
        yTitle="alpha3"
    elif  coeff=='beta3':
        yTitle="beta3"

  #  filename="./analysis_time_bins_bmi_groups/coeff_"+str(coeff)+"_model3_all_groups.agr" 
    filename="./analysis_time_bins_bmi_groups/coeff_"+str(coeff)+"_model3_all_groups.eps" 
  

    colors = [1,2,3,4,5,6,7,8,9,10]  # for each series
       
        
        
   
        
       
        
    realmultilinegraph(list_of_list_data,xTitle,yTitle,list_yLegends,filename,colors,coeff)
    
    print "\n      printed out:",filename 
    





####################################


def realmultilinegraph(list_of_list_data,xTitle,yTitle,list_yLegends,filename, colors,coeff):
#ys is a list of y-series
    
    

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
  #  obj1 = grace.add_drawing_object(DrawText)
    



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


   
    cont=0

    for i in range(len(  list_of_list_data)):

        dataset = graph.add_dataset(list_of_list_data[i],type='xydy',legend=list_yLegends[i])
        
        dataset.symbol.shape = 1       
        dataset.symbol.color = colors[i]                 
        dataset.symbol.fill_color = colors[i]   
        dataset.line.linewidth = 3
        dataset.errorbar.color = colors[i]   
        
        
        
        dataset.line.color = colors[i]
    
  

    graph.legend.char_size = 1.
    if coeff=='alpha3':
        graph.legend.loc = (.8,.61)

    elif coeff=='beta3':
        graph.legend.loc = (.2,.41)


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

    
