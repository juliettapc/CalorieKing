"""
Created by Julia Poncela on January 2011.

It reads all the graph files at once (months, quarters, year) from the 2, 5 and 10-point folders and calculates the number of n-cliques for the whole network, being n=1,2,...,7

It prints out the results in a general 'summary_clique_analysis' file.

It doesn't take any arguments.
"""




import networkx as nx
from copy import copy


network_list=[] #names of the different files


file1 = open('summary_clique_analysis','wt') 
print >> file1, "data:  #_points   time_scale  N_size   n-clique:#_n-cliques   max_clique_size   num_tot_cliques"
   
file1.close()





scale_list=[2,5,10]
for scale in scale_list:

    for index in range(0,11): #months    
       network_list.append(str(scale)+'_points_network/data/friend_graph_month'+str(index))


    for index in range(0,4): # quarters    
        network_list.append(str(scale)+'_points_network/data/friend_graph_quarter'+str(index))


 # year
    network_list.append(str(scale)+'_points_network/data/friend_graph_all0')




map (str, network_list)  # recordar que lo que escribo tiene que ser un string!!!!

 


oldG = None
for name in network_list: # loop to go over files (== over networks)

    print name

    G=nx.read_edgelist(name)
    if oldG:
        if oldG.edges() == G.edges():
            print "same graph?"
            print name


    partir=name.split("_points_network/data/friend_graph_")  #parto el nombre del fichero en una lista con dos componentes: num_ptos y time_scale
    num_points=partir[0]
    time_scale=partir[1]




    lista=list(nx.find_cliques(G))

    max_clique=nx.graph_clique_number(G)  #finds out max size clique
    num_tot_clique=nx.graph_number_of_cliques(G) #finds out total number of cliques

# count number of 2, 3, 4, 5, 6  and 7cliques:

    num_2cliques=0
    num_3cliques=0
    num_4cliques=0
    num_5cliques=0
    num_6cliques=0
    num_7cliques=0

    for element in lista: 
        if len(element)==2:
            num_2cliques=num_2cliques +1


            for node in element:
                G.node[node]['max_clique_size']=2
        elif len(element)==3:
            num_3cliques=num_3cliques+1
        elif len(element)==4:
            num_4cliques=num_4cliques+1
        elif len(element)==5:
            num_5cliques=num_5cliques+1
        elif len(element)==6:
            num_6cliques=num_6cliques+1
        elif len(element)==7:
            num_7cliques=num_7cliques+1
            
            
    #print "network: ", name,"  2: ",num_2cliques, "     3: ",num_3cliques, "   4: ",num_4cliques, "     5: ",num_5cliques, "   6: ",num_6cliques, "   7: ",num_7cliques, "   max_clique_size:",max_clique, "   num_tot_cliques:", num_tot_clique
   
         
    file1 = open('summary_clique_analysis','at') 
    print >> file1, num_points, time_scale,"  N: ",len(G),"  2:",num_2cliques, "     3:",num_3cliques, "   4:",num_4cliques, "     5:",num_5cliques, "   6:",num_6cliques, "   7:",num_7cliques, max_clique, num_tot_clique
   
    file1.close()
    oldG = copy(G)
