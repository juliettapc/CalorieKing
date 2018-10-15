import subprocess as sp
import networkx as nx


file1 = open('CK_modularity_analysis.dat','w')   # create the output file (and erase previous versions)
file1.close()



name_list=[] # list with the names of the input files



for index in range(0,11): #months    
    name_list.append("calorie_king_friends_no_staff_undirected_giant_month"+str(index))


for index in range(0,11): #mmonths    
    name_list.append("calorie_king_friends_undirected_giant_month"+str(index))


for index in range(0,4): # quarters    
    name_list.append("calorie_king_friends_no_staff_undirected_giant_quarter"+str(index))


for index in range(0,4): # quarters    
    name_list.append("calorie_king_friends_undirected_giant_quarter"+str(index))


 # year
name_list.append("calorie_king_friends_no_staff_undirected_giant_all0")
name_list.append("calorie_king_friends_undirected_giant_all0")



map (str, name_list)  # recordar que lo que escribo tiene que ser un string!!!!

 






#raw_input()





for name in name_list: # loop over files 

    calculations=[]  # list with all the atributes of the network (modularity, number of communities, averages,...)
    print "\n\nfile: "+name
    edge_data = open(name).readlines()



    calculations.append("\n") # to separate from the next set of data

    calculations.append(name)  # the list of atribute of every network (== every file)



    G=nx.read_edgelist(name) # create the network from the original input file

    degree_values=sorted(G.degree().values())  # create an ordered list of connectivities 
    #o tb: max(degree_values)    #degree_values[-1]  #  highest connectivity
    

    most_connected=[]
    for i in range (1,6):
        #print "max connectividades:",degree_values[-i] 
        most_connected.append(degree_values[-i])


    calculations.append(most_connected)  # save the connectivity values of the 5 top highest connected nodes
   
    average_network_degree=round(sum(G.degree().values())/float(len(G)),0)  

    print "<k>:",average_network_degree 
    calculations.append(average_network_degree)
   

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
            this_module = this_module[1] #this_module is the list of nodes in the current module
            this_module = map(int, this_module.split())
            modules.append(this_module) #list of modules (list of lists)
           
            
            #print this_module
            size=0
            conect_list=[]
            averageK=0
            for node in this_module:
                node=str(node)
                #print "node:", node, "degree:",G.degree(node) #ojo!! lo que le paso es la etiqueta, un string, no un num!!            
                conect_list.append(G.degree(node))  #create a connectivity list for the nodes in the module

                averageK=averageK+G.degree(node)
                size=size+1
            #print "max degree in the community:",max(conect_list), "  community size:", size
            
            size_list.append(size)# lista de los tamagnos de las comunidades
            averageK=averageK/float(size)
            average_k_list.append(round(averageK,0))
            
            if max_size < size:
               max_size = size 
            if max_max_degree < max(conect_list):
               max_max_degree = max(conect_list) 

            average_size=average_size+size
            average_max_degree=average_max_degree+max(conect_list)
            
            max_conect_list.append(max(conect_list))
            
            #for node in this_module:
             #   print sorted(G.degree(node).values())

    #average over communities
    average_size=average_size/len(modules)
    average_max_degree=average_max_degree/len(modules)

   
    #raw_input()

    calculations.append(len(modules))  #num cumunidades
   
    calculations.append(size_list)   # lista sizes comunidades
   
    calculations.append(average_size)  # media de sizes de comunidades 

    calculations.append(max_size)

    calculations.append(max_conect_list)  # lista de conectiv. maximas en cada comunidad
    
    calculations.append(average_k_list)  #lista de conectiv medias en cada comun



    print   "average_size:", average_size,"  average_max_degree:",average_max_degree
    print    "max_size:", max_size," max_max_degree:",max_max_degree
    output_string = "modularity: " + str(modularity) +"\n" #print modularity
    for s in modules:
        module_string = ",".join(map(str,s))
        output_string += module_string + ";\n" # print the elements of every community
                
#print output_string.rstrip(";")
    print output_string
    print "number of communities detected:"+str(len(modules))
    #raw_input()


    # write the output file (for now, just with the names of the input files)
 
    file1 = open('CK_modularity_analysis.dat','at')   
    for calculation in calculations:
        print >> file1, calculation  

    file1.close()
   
#ahora leo de nuevo el fichero, para tener la red
#print nx.connected_components(G)

    #print nx.degree(G)
    
    #raw_input() esperar un Intro





#write the data analysis on a file:


   
