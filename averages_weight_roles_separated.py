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

    file = open(directory+"Distributions_weight_change_roles_n.dat",'wt')
    file.close()
    file = open(directory+"Distributions_weight_change_roles_p.dat",'wt')
    file.close()

    list_index=range(8)


    for index in  list_index:                     
                         
        print "\n\n\n",index
        if len(list_w_c[index])>1:

            if min(list_w_c[index])<=0:        

                if max(list_w_c[index]) >=0:        
                    n_min_boundary= min(list_w_c[index])
                    n_max_boundary= 0.0
                  
                    p_min_boundary= 0.0
                    p_max_boundary= max(list_w_c[index])          

                elif max(list_w_c[index]) <=0:  
                    n_min_boundary= min(list_w_c[index])
                    n_max_boundary= max(list_w_c[index])
                  
                    p_min_boundary= 0.0
                    p_max_boundary= 0.0

            elif min(list_w_c[index])>=0:        

                n_min_boundary= 0.0
                n_max_boundary= 0.0
                  
                p_min_boundary= min(list_w_c[index])
                p_max_boundary= max(list_w_c[index])  




            n_Nbins=20 
            n_boundaries=[]

            p_Nbins=15 
            p_boundaries=[]


            n_interval=(n_max_boundary-n_min_boundary)/float(n_Nbins) +1.0  ## always positive amount
            p_interval=(p_max_boundary-p_min_boundary)/float(p_Nbins) +1.0 ## always positive amount
            print "n_max:",n_max_boundary, "n_min:",n_min_boundary, "n_interval:",n_interval
            print "p_max:",p_max_boundary, "p_min:",p_min_boundary, "p_interval:",p_interval
    

            n_start=n_max_boundary   #ojo! del cero hacia mas negativos!!
            for i in range(n_Nbins+1):                  
                n_boundaries.append(n_start)                                
                n_start=n_start-n_interval
               

            p_start=p_min_boundary #ojo! del cero hacia mas positivos!!
            for i in range(p_Nbins+1):        
                p_boundaries.append(p_start)
                p_start=p_start+p_interval

           
            print n_boundaries 
            print p_boundaries
           

            n_number_events_box=[0]*(n_Nbins+1)  # histogram
            p_number_events_box=[0]*(p_Nbins+1)  # histogram
    

            for i in list_w_c[index]:                                
                if i<=0:
                    b_index=0                             
                    for b in n_boundaries:  
                        if i > b:                
                            n_number_events_box[b_index]=n_number_events_box[b_index]+1 
                            b_index=b_index+1               
                            break
                        else:
                            b_index=b_index+1
           
                if i>=0:
                    b_index=0                             
                    for b in p_boundaries:  
                        if i < b:                
                            p_number_events_box[b_index]=p_number_events_box[b_index]+1 
                            b_index=b_index+1               
                            break
                        else:
                            b_index=b_index+1



            file = open(directory+"Distributions_weight_change_roles_n.dat",'at')
            for i in range(len(n_number_events_box)):  
                if  n_number_events_box[i] >0:
                    print >> file, n_max_boundary-i*float(n_interval)-float(n_interval)/2.0, n_number_events_box[i]
            print >> file, "\n"  # to separate roles
            file.close()
                    


            file = open(directory+"Distributions_weight_change_roles_p.dat",'at')
            for i in range(len(p_number_events_box)):    
                 if  p_number_events_box[i] >0:
                     print >> file, p_min_boundary+i*float(p_interval)+float(p_interval)/2.0, p_number_events_box[i]
            print >> file, "\n"  # to separate roles
            file.close()

       

       

#################################3
if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
