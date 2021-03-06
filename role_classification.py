#!/usr/bin/env python
"""
Created by Julia Poncela, February 2011


Given a name.gml file of a network with community structure (atributte 'community' of each node indicates to which community it belongs),
it clasifies the nodes of the GC into different roles,
according to its connectivity inside/outside its own community.

It generates a new file name_roles.gml with new atributtes for the nodes:
   Within-module degree zscore ('zi')
   Participation coefficient ('Pi')
   Its role, or role the node belongs to ('role')

It also genarates a file zscore_vs_ParticipationCoef.dat for the scatter plot of zi vs. Pi


For further detail, see: Cartography of complex networks: modules and universal roles.Guimera, R, Amaral, LAN. J. Stat. Mech.-Theory Exp.,  P02001 (2005).


"""



import networkx as nx
import math
import sys
from transform_labels_to_nx import *





def main (name):
#name='5_points_network/data/friend_graph_all0.gml'

    #dir=name.split('friend_graph')[0]
    dir=name.split('method3_adherent')[0]




    H=nx.read_gml(name) # create the network from the original input file  

# al leer la red de un .gml, los nodos tiene atributos: label, activity, community,...



    name=name.split('.')
    name=name[0]   #  remove the extension of the filename

    components=nx.connected_component_subgraphs(H)  
   
    G=components[0] #  take just the GC as a subgraph to perform the community ID algorithm
                   


    list_nodes_GC=G.nodes()

  

   

    num_nodes_GC=int(len(list_nodes_GC))

    
    label_comm=[] #list of community labels
    for i in list_nodes_GC: 
        G.node[i]['zi']=0.0  # i add a new attribute to the nodes
        G.node[i]['Pi']=0.0  # i add a new attribute to the nodes

        if G.node[i]['community'] not in label_comm:
            label_comm.append(G.node[i]['community'])
    num_com=int(len(label_comm))







# calculate the within-module degree zscore (zi):

    average_ksi=[] #list of averages of total degree, computed inside each community si
    nodes_in_comm=[] #list of number of nodes for each community si
    deviation=[]  # standard deviation of k in community si
    for i in range(num_com+1):  # community indexes go from 1 to num_com
        average_ksi.append(0.0)
        nodes_in_comm.append(0.0)
        deviation.append(0.0)
   


    for i in list_nodes_GC:  # loop over all nodes in GC         

        
        print i, type(i),G.node[i]['community'],type(G.node[i]['community'])
        exit()


        average_ksi[G.node[i]['community']]=average_ksi[G.node[i]['community']]+G.degree(i)
        nodes_in_comm[G.node[i]['community']]=nodes_in_comm[G.node[i]['community']]+1
     
    

    for i in range(1,num_com+1): 
        average_ksi[i]=average_ksi[i]/nodes_in_comm[i]   
   



    for i in list_nodes_GC:
        deviation[G.node[i]['community']]=deviation[G.node[i]['community']]+(G.degree(i)-average_ksi[G.node[i]['community']])**2


    for i in range(1,num_com+1):
        deviation[i]=math.sqrt(deviation[i]/nodes_in_comm[i])



    for i in list_nodes_GC:   
        ki=0.0
        for node in G.neighbors(i):  # loop over  i's neighbors
            if G.node[i]['community']==G.node[node]['community']: #if both belong to the same comm
                ki=ki+1                     
        G.node[i]['zi']=(ki-average_ksi[G.node[i]['community']])/deviation[G.node[i]['community']]


    


# calculate participation coefficient:
    for i in list_nodes_GC:    
        add=0.0
        for c in range(1,num_com+1):  # loop over all communities
            kis=0.0 # number of neighbors of i belonging to comm c
            fraction=0.0     
            for node in G.neighbors(i):   #loop over i's neighbors
                if G.node[node]['community']==c:
                    kis=kis+1  
            fraction=(kis/G.degree(i))**2
            add=add+fraction
        G.node[i]['Pi']=1.0-add



# asign a role to each node:
    for i in list_nodes_GC:
        if G.node[i]['zi']>= 2.0: #it is a hub
            if G.node[i]['Pi']< 0.3:
                G.node[i]['role']='R5'

            elif G.node[i]['Pi']>= 0.3 and G.node[i]['Pi']< 0.75:
                G.node[i]['role']='R6'

            elif  G.node[i]['Pi']>= 0.75:
                G.node[i]['role']='R7'

        else: # it is not a hub
            if G.node[i]['Pi']< 0.05:
                G.node[i]['role']='R1'

            elif G.node[i]['Pi']>= 0.05 and G.node[i]['Pi']< 0.65:
                G.node[i]['role']='R2'

            elif G.node[i]['Pi']>= 0.65 and G.node[i]['Pi']< 0.8:
                G.node[i]['role']='R3'

            elif G.node[i]['Pi']>= 0.8:
                G.node[i]['role']='R4'






# write zscore-Participation to a file
    file1 = open(dir+"zscore_vs_ParticipationCoef.dat",'wt')
    for i in list_nodes_GC:
        print >> file1, G.node[i]['Pi'],G.node[i]['zi']
 
    file1.close()




# write the list of lists (communities) sorted by role to a file
    list_roles=["R1","R2","R3","R4","R5","R6","R7"]   


    file2 = open(dir+"list_of_communities_5points_all0_by_role",'wt')
    for roles in list_roles:  # loop over roles
        for i in list_nodes_GC: # loop over nodes
            if G.node[i]['role']==roles:
               # print i,G.node[i]['role']
                print >> file2, i,

        
        print >> file2,";",
        
    file2.close()






# write zscore-Participation with info about communities to a file
    file3 = open(dir+"zscore_vs_ParticipCoef_with_comm_info.dat",'wt')
    for label in label_comm:
        for i in list_nodes_GC:
            if G.node[i]['community']==label:

                print >> file3, G.node[i]['Pi'],G.node[i]['zi']

        print >> file3,"\n"  # extra line to separate communities
    file3.close()









#create a new gml file with the added atributes:

    nx.write_gml(H,name+"_roles.gml")

##ojoooo! los atributos zi y Pi que le doy a los nodos en el subgrafo G (GC)
# tb los tienen los correspondientes nodos en H (total)



if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
