#! /usr/bin/env python
"""
Created by Julia Poncela on January 2011.

Given a network 'path/network_file_name' it calculates the modulary, number and size of communities, ..., for the giant component.

It prints out the results in a general 'path/network_file_name'+'_modularity_analysis_GC' file, and also in a bunch of other files 'path/network_file_name'+'_list_modularity_analysis_GC', one for each network.

Intended to be called from within master_piping_mod_rand_comparison.py code


It takes as argument the network filename.

"""



import subprocess as sp
import networkx as nx
import sys








def main(input_file_name_list_comm):



  #  nombre=input_file_name.split("friend_")
   # directorio=nombre[0]








    input_file_name_roles="5_points_network_2010/data/friend_graph_all.gml"


    H=nx.read_gml(input_file_name_roles) # create the network from the original input file  
    components=nx.connected_component_subgraphs(H)      
    G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]   



    file=open(input_file_name_list_comm)
    datos=file.readlines()  # the whole thing is a list (with one single element)


   
    for i in datos:
        i=str(i)
        modules=i.split(";")#separate communities --->> list of communities



      


    list_roles=["R1","R2","R3","R4","R5","R6","R7"] #for the role restriction

    for  role in list_roles:

        modules_role_discrimination=[]
        for i in modules:  # loop over different communities
            
            this_module=i.split(",") #separate all nodes from the same module
       
        

            this_module_ids=[]
            for label in this_module:# create a list of ids of the nodes in this_module
            
                for node in G.nodes():   
                #print type(G.node[node]['label']),type(label)  #int and str
                    if str(G.node[node]['label'])==label:
                        this_module_ids.append(G.node[node]['id'])
                    
        
            this_module_role_restriction=[]            
            for node in this_module_ids:  # i filter only the role a want
            #print type(G.node[node]['role']),type(role)  #unicode and str
                if str(G.node[node]['role'])==role:
                    this_module_role_restriction.append(G.node[node]['label'])
            
            if len(this_module_role_restriction)>0:
                modules_role_discrimination.append(this_module_role_restriction)

        

       


        print modules_role_discrimination




    

# i transform the list of list into:  n1,n2,n3;n4,n5;n6,n7,n8

        element=[]
        for list in modules_role_discrimination:
            element.append(",".join(map(str,list)))
        
   
            string=";".join(map(str,element))
    
        if len(element)>0:
                
            file3 = open(input_file_name_list_comm+'_'+str(role),'wt') 
            print >> file3, string 
            file3.close()
    
       





########################################################
if __name__== "__main__":
    if len(sys.argv)>1:
       
        input_file_name_list_comm=sys.argv[1]   
    
        main(input_file_name_list_comm)

    else:
        print "Usage: python program_name   path/graph_file_name_LIST_COMM_csv "
