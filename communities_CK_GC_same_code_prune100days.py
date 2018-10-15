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
from transform_labels_to_nx import *




#  OJOOO! EL PRIMER PRINT DEL PROGR. DEBE SER LA MODULARIDAD (LOS SIG, DA =)





def main(input_file_name):

   #cuando uso la red original: input_file_name=input_file_name (original )
   #cuando uso la red randomizada: input_file_name=input_file_name+'_rand_version'+str(iteracion)




  #  nombre=input_file_name.split("friend_")
   # directorio=nombre[0]


  
    cont=0
#i create the edgelist without the non-engaged users
    G=nx.read_gml(input_file_name)
    G = transform_labels_to_nx(G)  #transform, so G.nodes() is a list of label, not ids!

    print "before pruning:",len(G.nodes())

    edgelist_file_name=input_file_name.split(".gml")[0]
    nx.write_edgelist(G, edgelist_file_name, data=False)



   # for node in G.nodes():
    #    if int(G.node[node]['time_in_system'])<= int(100):
     #       G.remove_node(node)
      #      print "removing:", node
       #     cont=cont+1


    print "tot. nonengaged users excluded:", cont
    edgelist_file_name=input_file_name.split(".gml")[0]
    edgelist_file_name=edgelist_file_name+'_100days'
    nx.write_edgelist(G, edgelist_file_name, data=False)
    

    print "after pruning:",len(G.nodes())

    file1 = open(edgelist_file_name +'_100days_modularity_analysis_GC','wt') # one summary file for everything

    print >> file1, "data:   #_points  time_scale  GC_size  <k>  k(hub)  modularity  #_communities  <community_size>  max_community_size"  

    file1.close()




   

    name_list=[] # list of names of the input files
   
    name_list.append(edgelist_file_name)




    map (str, name_list)  # recordar que lo que escribo tiene que ser un string!!!!

 








    for name in name_list: # loop to go over files (== over networks)

       
        calculations=[]  # list of atributes for every network (modularity, number of communities, averages,...)
        list_of_data_list=[] #list of atributes that are lists (5top hubs, communitiy sizes,...)


    
       
        edge_data = open(name).readlines()

        #partir=name.split("_points_network/data/friend_graph_")  #parto el nombre del fichero en una lista con dos componentes: num_ptos y time_scale
        num_points=5#partir[0]
        time_scale='all0'#partir[1]
   
   





        H=nx.read_edgelist(name) # create the network from the original input file  

        components=nx.connected_component_subgraphs(H)  
   
        G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]
   


       
        calculations.append(num_points) 
        calculations.append(time_scale)
        calculations.append(len(G))


    




        new_edge_data = [] #this list is what i will pass to Roger's code
        for e in G.edges(): # e is a list of two neighbors: [n1,n2]
                        #i have to convert e to str because it is in some other format and the algorithm may not recognise it
             
            new_edge_data.append(" ".join(map(str,e))) # i join the two neighbors, separating them just by a space, so now they are just one element of the edge_list, which is: [n1 n2, n3 n4, n2 n3,...]
   
    
        degree_values=sorted(nx.degree(G).values())
    
        most_connected=[]
        for i in range (1,11):        
            most_connected.append(degree_values[-i])


        list_of_data_list.append(most_connected)  # save the connectivity values of the 5 top highest connected nodes
   
        average_network_degree=int(round(sum(G.degree().values())/float(len(G)),0)  )

    
        calculations.append(average_network_degree)
        calculations.append(degree_values[-1])
   

        p = sp.Popen(["/opt/communityID"], stdin=sp.PIPE, stdout=sp.PIPE)
        output, error = p.communicate("\n".join(new_edge_data))
        community_lines = output.split("part")
        modularity = float(community_lines[0])
        partition_lines = community_lines[1].split("\n")
        modules = []


        calculations.append(modularity)
   
        max_max_degree=0
        max_size=0
        average_size=0
        average_max_degree=0
        size_list=[]  
        max_conect_list=[]
        average_k_list=[]
        for p in partition_lines:
            this_module = p.split("---")         
            if len(this_module) > 1:
                this_module = this_module[1] # 'this_module' is the list of nodes in the current module
                this_module = map(int, this_module.split())
                modules.append(this_module) # list of modules (list of lists)
           
                   
               # print modules
               # raw_input()
    
                size=0
                conect_list=[]
                averageK=0

                for node in this_module:   # loop over the nodes of the current module
                    node=str(node)                  
               
                    conect_list.append(G.degree(node))  #create a connectivity list for the nodes in the module
                
                
                
                    averageK=averageK+G.degree(node)
                    size=size+1
                
            
    
           
            
                size_list.append(size)#  list of community sizes
                averageK=averageK/float(size)
                average_k_list.append(int(round(averageK,0)))
            
                if max_size < size:
                    max_size = size 
                if max_max_degree < max(conect_list):
                    max_max_degree = max(conect_list) 

                average_size=average_size+size
                average_max_degree=average_max_degree+max(conect_list)
            
                max_conect_list.append(max(conect_list))
      
    #average over communities
        average_size=average_size/len(modules)
        average_max_degree=average_max_degree/len(modules)

   
   

        calculations.append(len(modules))  #number of cummunities  
        calculations.append(average_size)  # average sizes of communities 
        calculations.append(max_size)     # maximum size of communities 




        list_of_data_list.append(max_conect_list)  # list of maximum conectivity per each community    
        list_of_data_list.append(average_k_list)  # list of average conectivity per each community    
        list_of_data_list.append(size_list)   # list of community sizes



        output_string = "modularity: " + str(modularity) +"\n" #print modularity
        for s in modules:
            module_string = ",".join(map(str,s))
            output_string += module_string + ";\n" # print the elements of every community
                

        print modularity, input_file_name

       



# write the output files  

        file2 = open(name+'_list_modularity_analysis_GC','wt') #one output file per each input file

        print >> file2, "data:  list_k_10top_hubs  list_max(k)_each_comm  list_<k>_each_comm  list_community_sizes\n"
        for item in list_of_data_list:
            print >> file2, item
            print >> file2, "\n"
        file2.close()





    
        file1 = open(name+'_modularity_analysis_GC','at') # one summary file for everything       
        for calculation in calculations:
            print >> file1, calculation,  # with a comma at the end, there is not \n between values  
        file1.close()



# i transform the list of list into:  n1,n2,n3;n4,n5;n6,n7,n8

        element=[]
        for list in modules:
            element.append(",".join(map(str,list)))

        #print element

        string=";".join(map(str,element))

      #  print string

        file3 = open(name+'_list_of_communities_csv','wt') 
        print >> file3, string 
        file3.close()
            
        file3 = open(name+'_list_of_communities','wt') 
        print >> file3, modules 
        file3.close()




if __name__== "__main__":
    if len(sys.argv)>1:
        input_file_name=sys.argv[1]   
    
        main(input_file_name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
