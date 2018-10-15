#! /usr/bin/env python

"""
Created by Julia Poncela of March 2011

Given a .gml file with a "role" label, counts the number of nodes in every 
role (only for the GC), and then creates equivalent groups (meaning, 
with the same number of members each) according to ordered degree.


It takes as an argument the path/network_file.gml and returns a new
 .gml file with a new attribute (for the nodes belonging to the GC)


"""





import sys
import os
import networkx as nx




def main (name):


    dir=name.split('friend_graph')[0]

    H=nx.read_gml(name)

    components=nx.connected_component_subgraphs(H)  
   
    G=components[0] #  

   
    

    list_of_roles=['R1','R2','R3','R4','R5','R6','R7']
    Num_ele_role=[0]*8
    total=0

    for node in G.nodes():
        try:
            #print G.node[node]['role'],
            for role in list_of_roles:
                if G.node[node]['role']==role:
                    index=int(role.split('R')[1])
                    #print index                   
                    Num_ele_role[index]=Num_ele_role[index]+1
                    total= total+1
        except KeyError: 
            print "not in the GC"
            pass


    print Num_ele_role,total
    #raw_input()
   

    list_degrees=[]

    for node in G.nodes():
        list_degrees.append([G.degree(node),node])
        
       
    sorted_list_degrees=sorted(list_degrees)
   
# print list_degrees  
  
 #   print sorted_list_degrees  #ordered list of [degree,node]

    boundaries=[0]*8
   
    for b in range(1,len(boundaries)):
        value=0
        
        for num in range(b+1):           
            if Num_ele_role[num] >0:
                value=value+Num_ele_role[num]         
                boundaries[b]=value

    print boundaries   

        

    index_i=0
    index_f=1
    maximum=max(boundaries)
    for b in range(maximum+1):
        #print b,  boundaries[index_i],boundaries[index_f],index_i, index_f
        if b > boundaries[0]:
            if b<= boundaries[1]:
                G.node[b]['degree_rank']=index_f
                print "node:",node, G.degree(node), index_f
        else:
            index_i=index_i+1
            index_f=index_f+1
            print index_i, index_f







###########################################3
if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
