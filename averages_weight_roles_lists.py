#! /usr/bin/env python

"""
Created by Julietta PC, March 2011.


Given a name.gml network, it calculates de average & standard deviation of weight change and activity for the nodes belonging to the same role and also for communities.


"""





import networkx as nx
import math
import sys
import numpy
from pylab import *


def main (name):



    directory=name.split('fr')[0]
   


    G=nx.read_gml(name) # create the network from the original input file  
    #print G.nodes(data=True)


    list_of_roles=[]
    list_of_roles.append('R1')
    list_of_roles.append('R2')
    list_of_roles.append('R3')
    list_of_roles.append('R4')
    list_of_roles.append('R5')
    list_of_roles.append('R6')
    list_of_roles.append('R7')
    

    dicc_roles={'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7}
   

    weight_change_av=[0.0]*8


   
    list_w_c=[]
    for i in range(len(list_of_roles)+1):
        list_w_c.append([])    ### ojooooo!!! si quiero definir una lista de listas vacias, hacerlo exactamente asi!

   



    norm=[0.0]*8

       

    for node in G.nodes():  

        if G.node[node]['weigh_ins']>=5:   # only >=5 weight-in point individuals                                                   
            for role in list_of_roles:
                try:     
                    if G.node[node]['role']==role:
                        
                        index=dicc_roles[role]                        
                         
                        weight_change_av[index]=weight_change_av[index]+float(G.node[node]['weight_change'])

                        #print node, G.node[node]['role'],index,weight_change_av[index]
                      
                        norm[index]= norm[index]+1.0
                        list_w_c[index].append(float(G.node[node]['weight_change']))
                       
               
                except KeyError: #if the node doesnt have a role (== doesnt belong to the GC)
                    weight_change_av[0]=weight_change_av[0]+float(G.node[node]['weight_change'])
                    norm[0]= norm[0]+1.0
                    list_w_c[0].append(float(G.node[node]['weight_change']))
                    break  # dont want to loop over the rest of the nodes!!

    

    for index in range(8):
        try:            
            weight_change_av[index]=weight_change_av[index]/norm[index]
        except ZeroDivisionError:
            weight_change_av[index]=0.0

 
  

    deviation=[0.0]*8
    index=0    
    for list in list_w_c:                               
        for i in list:   # loop over all values of weight for a given role                       
            deviation[index]=deviation[index] +(i - weight_change_av[index])**2            
        index=index+1


# i print out the averages
    file = open(directory+"Average_weight_change_roles.dat",'wt')
    for index in range (8):       
        try:
            deviation[index]=deviation[index]/norm[index]
            deviation[index]=sqrt(deviation[index])
            print >> file,"R",index,":",weight_change_av[index],"(+-",deviation[index],")"
            print "R",index,":",weight_change_av[index],"(+-",deviation[index],")"
            
        except ZeroDivisionError:
            deviation[index]=0.0
            print >> file,"R",index,"  empty"
            print "R",index,"  empty"
    file.close()







# bins for the distributions:
########################################

    file = open(directory+"Distributions_weight_change_roles.dat",'wt')
    file.close()


    list_index=range(8)


    for index in  list_index:                     
                         
        print "\n\n\n",index
        if len(list_w_c[index])>1:

            
            min_boundary= min(list_w_c[index])        
            max_boundary= max(list_w_c[index])


          

  
            Nbins=30
            boundaries=[]

           

            interval=(max_boundary-min_boundary)/float(Nbins) +1.0
            print "max:",max_boundary, "min:",min_boundary, "interval:",interval
    

            start=min_boundary
            for i in range(Nbins+1):        
                boundaries.append(start)
                start=start+interval


#            print boundaries
        

            number_events_box=[0]*(Nbins+1)  # histogram
    

            for i in list_w_c[index]:  
                b_index=0         
                for b in boundaries:  
                    if i < b:                
                        number_events_box[b_index]=number_events_box[b_index]+1              
                        b_index=b_index+1               
                        break
                    else:
                        b_index=b_index+1
           

            file = open(directory+"Distributions_weight_change_roles.dat",'at')
            for i in range(len(number_events_box)):    
                print >> file, i*float(interval)+min_boundary, number_events_box[i]
            print >> file, "\n"  # to separate roles
            file.close()
   
       

       

#################################3
if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
