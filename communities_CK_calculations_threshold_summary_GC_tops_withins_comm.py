"""
Created by Julia Poncela on January 2011.

It reads all the graph files at once (months, quarters, year) from the 2, 5 and 10-point folders and calculates the modulary, number and size of communities, ..., just for the giant component of each network.

It prints out the results in a general 'summary_modularity_analysis' file, and also in a bunch of other files 'path/graph_name'+'_list_modularity_analysis', one for each network.

It doesn't take any arguments.
"""



import subprocess as sp
import networkx as nx



file1 = open('summary_modularity_analysis_GC','wt') # one summary file for everything

print >> file1, "data:   #_points  time_scale  GC_size  <k>  k(hub)  modularity  #_communities  <community_size>  max_community_size\n"  


file1.close()






name_list=[] # list of names of the input files
scale_list=[2,5,10]

for scale in scale_list:

    for index in range(0,11): #months    
        name_list.append(str(scale)+'_points_network/data/friend_graph_month'+str(index))


    for index in range(0,4): # quarters    
        name_list.append(str(scale)+'_points_network/data/friend_graph_quarter'+str(index))


        # year
    name_list.append(str(scale)+'_points_network/data/friend_graph_all0')




map (str, name_list)  # recordar que lo que escribo tiene que ser un string!!!!

 








for name in name_list: # loop to go over files (== over networks)

    calculations=[]  # list of atributes for every network (modularity, number of communities, averages,...)
    list_of_data_list=[] #list of atributes that are lists (5top hubs, communitiy sizes,...)


    
    print "\n\nfile: "+name
    edge_data = open(name).readlines()

    partir=name.split("_points_network/data/friend_graph_")  #parto el nombre del fichero en una lista con dos componentes: num_ptos y time_scale
    num_points=partir[0]
    time_scale=partir[1]
   
   





    H=nx.read_edgelist(name) # create the network from the original input file  

    components=nx.connected_component_subgraphs(H)  
   
    G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]
   


    calculations.append("\n") # just to separate from the next set of data
    calculations.append(num_points) 
    calculations.append(time_scale)
    calculations.append(len(G))


    



    #print len(G) # N
    #print G.number_of_nodes()# N


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

    
    most_connected_within_all_network=[]
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

            label_and_k=[]#lista de conectividades y label_nodos en una communidad

            modules.append(this_module) # list of modules (list of lists)           
                       
            size=0
            conect_list=[]
            averageK=0
            degree_values_within=[]#list of k within the current community
            for node in this_module:   # loop over the nodes of the current module
                node=str(node)                  
               
                conect_list.append(G.degree(node))  #create a connectivity list for the nodes in the module
                
                
                
                averageK=averageK+G.degree(node)
                size=size+1
                degree_values_within.append(G.degree(node)) #ESTOY GUARDANDO K'S NO LAS LABEL DE LOS NODOS!!!!!
                pair=[]                
                pair.append(G.degree(node))
                pair.append(node)   
                label_and_k.append(pair) #guardo parejas de [k_nodo,label_nodo]
            # end loop nodes of a given module.
           
            
            label_and_k=sorted(label_and_k) # i sorted the nodes belonging to the current community by connectivity            
    
            most_connected_within=[]#list of top-10 most connected nodes in the community
            if len(this_module) >= 10:                
                for i in range (1,11):                
                    most_connected_within.append(label_and_k[-i][1])
            elif len(this_module) >= 5:                
                for i in range (1,6):                
                    most_connected_within.append(label_and_k[-i][1])
                    
            else:                     
                for i in range(len(this_module)):
                    most_connected_within.append(label_and_k[-i][1])

            
          
            most_connected_within_all_network.append(most_connected_within)#list lists of top-10 most connected nodes in the community

           

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
          
        # end of loop over communities

    #average over communities
    average_size=average_size/len(modules)
    average_max_degree=average_max_degree/len(modules)

   
   

    calculations.append(len(modules))  #number of cummunities  
    calculations.append(average_size)  # average sizes of communities 
    calculations.append(max_size)     # maximum size of communities 




    list_of_data_list.append(max_conect_list)  # list of maximum conectivity per each community    
    list_of_data_list.append(average_k_list)  # list of average conectivity per each community    
    list_of_data_list.append(size_list)   # list of community sizes


#print the results
    print "N:",len(G),"  number of communities detected:"+str(len(modules))
    print   "average_size:", average_size,"  average_max_degree:",average_max_degree
    print    "max_size:", max_size," max_max_degree:",max_max_degree
    output_string = "modularity: " + str(modularity) +"\n" #print modularity
    for s in modules:
        module_string = ",".join(map(str,s))
        output_string += module_string + ";\n" # print the elements of every community
                

    #print output_string

    
   


# write the output files  

    file2 = open(name+'_list_modularity_analysis_GC','wt') #one output file per each input file

    print >> file2, "data:  list_10top_hubs  list_max(k)_each_comm  list_<k>_each_comm  list_community_sizes\n"

    for item in list_of_data_list:
        print >> file2, item
        print >> file2, "\n"

    file2.close()





    
    file1 = open('summary_modularity_analysis_GC','at') # one summary file for everything
       
    for calculation in calculations:
       print >> file1, calculation,  # with a comma at the end, there is not \n between values  
    file1.close()




    if name== '5_points_network/data/friend_graph_all0':
    
        file3 = open('list_of_communities_'+str(num_points)+'points_'+str(time_scale),'wt')   
        print >> file3, modules   # imprimo lista de listas (==nodos en cada comunidad)
  
        file3.close()




        file4 =open('list_of_top10_hubs_withing_communities_'+str(num_points)+'points_'+str(time_scale),'wt')
        print >> file4, most_connected_within_all_network

        file4.close()
