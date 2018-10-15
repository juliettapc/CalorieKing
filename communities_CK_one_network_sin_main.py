import subprocess as sp
import networkx as nx



file1 = open('summary_modularity_analysis','wt') # one summary file for everything

print >> file1, "data:   #_points  time_scale  N  <k>  k(hub)  modularity  #_communities  <community_size>  max_community_size\n"  


file1.close()




name_list=[] # list of names of the input files
scale_list=[10]

for scale in scale_list:
   
    #name_list.append(str(scale)+'_points_network/data/friend_graph_all0')
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
    #print num_points, time_scale

    #raw_input()
    G=nx.read_edgelist(name) # create the network from the original input file
    #degree_values=sorted(G.degree().values())  # create an ordered list of connectivities 




    calculations.append("\n") # just to separate from the next set of data
    calculations.append(num_points) 
    calculations.append(time_scale)
    calculations.append(len(G))



    
    
    degree_values=sorted(nx.degree(G).values())
    #print degree_values
    #raw_input()

    most_connected=[]
    for i in range (1,6):        
        most_connected.append(degree_values[-i])


    list_of_data_list.append(most_connected)  # save the connectivity values of the 5 top highest connected nodes
   
    average_network_degree=int(round(sum(G.degree().values())/float(len(G)),0)  )

    
    calculations.append(average_network_degree)
    calculations.append(degree_values[-1])
   

    p = sp.Popen(["/opt/communityID"], stdin=sp.PIPE, stdout=sp.PIPE)
    output, error = p.communicate("".join(edge_data))
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


#print the results
    print "number of communities detected:"+str(len(modules))
    print   "average_size:", average_size,"  average_max_degree:",average_max_degree
    print    "max_size:", max_size," max_max_degree:",max_max_degree
    output_string = "modularity: " + str(modularity) +"\n" #print modularity
    for s in modules:
        module_string = ",".join(map(str,s))
        output_string += module_string + ";\n" # print the elements of every community
                

    print output_string

    
   


# write the output files  

    file2 = open(name+'_list_modularity_analysis','wt') #one output file per each input file

    print >> file2, "data:  list_5top_hubs  list_max(k)_each_comm  list_<k>_each_comm  list_community_sizes\n"

    for item in list_of_data_list:
        print >> file2, item
        print >> file2, "\n"

    file2.close()





    
    file1 = open('summary_modularity_analysis','at') # one summary file for everything
       
    for calculation in calculations:
       print >> file1, calculation,  # with a comma at the end, there is not \n between values  

    file1.close()
