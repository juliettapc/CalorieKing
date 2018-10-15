#! /usr/bin/env python

"""
Created by Julietta PC, March 2011.


Given a name.gml network, it calculates de average & standard deviation of weight change and activity for the nodes belonging to the same role and also for communities.


"""





import networkx as nx
import math
import sys




def main (name):







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
    



    weight_change_av_R1=0.0
    weight_change_av_R2=0.0
    weight_change_av_R3=0.0
    weight_change_av_R4=0.0
    weight_change_av_R5=0.0
    weight_change_av_R6=0.0
    weight_change_av_R7=0.0
    weight_change_av_outside=0.0
    

    norm_R1=0.0
    norm_R2=0.0
    norm_R3=0.0
    norm_R4=0.0
    norm_R5=0.0
    norm_R6=0.0
    norm_R7=0.0
    norm_outside=0.0
    

    for node in G.nodes():

        print node

        try:
            if G.node[node]['role']=='R1':
                print 'R1'
                weight_change_av_R1=weight_change_av_R1+G.node[node]['weight_change']
                norm_R1= norm_R1+1
                
            elif  G.node[node]['role']=='R2':
                weight_change_av_R2=weight_change_av_R2+G.node[node]['weight_change']
                norm_R2= norm_R2+1
                
                print 'R2'
            elif  G.node[node]['role']=='R3':
                weight_change_av_R3=weight_change_av_R3+G.node[node]['weight_change']
                norm_R3= norm_R3+1
                
                print 'R3'
                
            elif  G.node[node]['role']=='R4':
                weight_change_av_R4=weight_change_av_R4+G.node[node]['weight_change']
                norm_R4= norm_R4+1
                
                print 'R4'
                
            elif  G.node[node]['role']=='R5':
                weight_change_av_R5=weight_change_av_R5+G.node[node]['weight_change']
                norm_R5= norm_R5+1
                
                print 'R5'
                
            elif  G.node[node]['role']=='R6':
                weight_change_av_R6=weight_change_av_R6+G.node[node]['weight_change']
                norm_R6= norm_R6+1
                
                print 'R6'
                
            elif  G.node[node]['role']=='R7':
                weight_change_av_R7=weight_change_av_R7+G.node[node]['weight_change']
                norm_R7= norm_R7+1
                
                print 'R7'
                
        except KeyError:   
            weight_change_av_outside=weight_change_av_outside+G.node[node]['weight_change']
            norm_outside= norm_outside+1

            print G.node[node]['n_weight_change']
   



print weight_change_av_R7/norm_R7,weight_change_av_R7/norm_R7
            

#################################3
if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
