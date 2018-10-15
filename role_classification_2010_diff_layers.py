#! /usr/bin/env python

"""
Created by Julia Poncela, March 2011


Given a name.gml file of a network with community structure (atributte 'community' of each node indicates to which community it belongs),
it clasifies the nodes of the GC into different roles,
according to its connectivity inside/outside its own community.
It modifies the file name.gml with new atributtes for the nodes:
   Within-module degree zscore ('zi')
   Participation coefficient ('Pi')
   The role the node belongs to ('role')

It also genarates a file zscore_vs_ParticipationCoef.dat for the scatter plot of zi vs. Pi


For further detail, see: Cartography of complex networks: modules and universal roles.Guimera, R, Amaral, LAN. J. Stat. Mech.-Theory Exp.,  P02001 (2005).


"""



import networkx as nx
import math
import sys




def main (name):

#name='5_points_network/data/friend_graph_all0.gml'
#name=5_points_network_2010/data/new_networks/quarters/friends_graph_quarter2_comm.gml
#name=5_points_network_2010/data/new_networks/6months/friends_graph_sixmonths1_comm.gml


   
    #dir=name.split('master')[0]
    #dir=name.split('method3_50_adh')[0]
    dir=name.split('network_')[0]
   # dir=name.split('friends')[0]


    info_name=name.split('.gml')[0]   
    #info_name=info_name.split('method3_50/interim/')[1]
    #info_name=info_name.split('network_all_users/')[1]
    info_name=info_name.split('semester_quarter_window_networks/')[1]


    #info_name=info_name.split('data/')[1]
    info_name2=info_name#info_name.split('master_')[1]#for 6month networks
    
   

    H=nx.read_gml(name) # create the network from the original input file  

# al leer la red de un .gml, los nodos tiene atributos: label, activity, community,...




    coef_layer  = 1.5


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


        community_index=G.node[i]['community'].split('_')[0]
        community_size=G.node[i]['community'].split('_')[1]
        
        G.node[i]['community_index']=int(community_index)
        G.node[i]['community_size']=community_size

        #print G.node[i]['community'],community_index,G.node[i]['community_index'],G.node[i]['community_size']
        #raw_input()
        # the label comunity in the gml file: index_size


        if G.node[i]['community_index'] not in label_comm:
            label_comm.append(G.node[i]['community_index'])
    num_com=int(len(label_comm))
    #print label_comm,len(label_comm)
    

    


    




# calculate the within-module degree zscore (zi):

    average_ksi=[] #list of averages of total degree, computed inside each community si
    nodes_in_comm=[] #list of number of nodes for each community si
    deviation=[]  # standard deviation of k in community si
    for i in range(num_com):  # community indexes go from 0 to num_com-1
        average_ksi.append(0.0)
        nodes_in_comm.append(0.0)
        deviation.append(0.0)
   


    for i in list_nodes_GC:  # loop over all nodes in GC         
        average_ksi[G.node[i]['community_index']]=average_ksi[G.node[i]['community_index']]+G.degree(i)
        nodes_in_comm[G.node[i]['community_index']]=nodes_in_comm[G.node[i]['community_index']]+1
     
        
    for i in range(num_com): 
        average_ksi[i]=average_ksi[i]/nodes_in_comm[i]   
   



    for i in list_nodes_GC:
        deviation[G.node[i]['community_index']]=deviation[G.node[i]['community_index']]+(G.degree(i)-average_ksi[G.node[i]['community_index']])**2


    for i in range(num_com):
        deviation[i]=math.sqrt(deviation[i]/nodes_in_comm[i])



    for i in list_nodes_GC:   
        ki=0.0
        for node in G.neighbors(i):  # loop over  i's neighbors
            if G.node[i]['community_index']==G.node[node]['community_index']: #if both belong to the same comm
                ki=ki+1        
        #print  ki, average_ksi[G.node[i]['community_index']],deviation[G.node[i]['community_index']], G.node[i]['community_index'] 
        if  deviation[G.node[i]['community_index']] >0.0:    
            G.node[i]['zi']=(ki-average_ksi[G.node[i]['community_index']])/deviation[G.node[i]['community_index']]


    


# calculate participation coefficient:
    for i in list_nodes_GC:    
        add=0.0
        for c in range(num_com):  # loop over all communities
            kis=0.0 # number of neighbors of i belonging to comm c
            fraction=0.0     
            for node in G.neighbors(i):   #loop over i's neighbors
                if G.node[node]['community_index']==c:
                    kis=kis+1.0  
            fraction=(kis/float(G.degree(i)))**2
            add=add+fraction
        G.node[i]['Pi']=1.0-add




# asign a role to each node:
    for i in list_nodes_GC:
        if G.node[i]['zi']>= 2.0: #it is a hub
            if G.node[i]['Pi']< 0.3:
                G.node[i]['role']='R5'
                H.node[i]['role']='R5'              

            elif (G.node[i]['Pi']>= 0.3 and G.node[i]['Pi']< 0.75):
                G.node[i]['role']='standardR6'
                H.node[i]['role']='standardR6'

            elif  G.node[i]['Pi']>= 0.75:
                G.node[i]['role']='R7'              

        else: # it is not a hub
            if G.node[i]['Pi']< 0.05:
                G.node[i]['role']='R1'
                H.node[i]['role']='R1'               

            elif (G.node[i]['Pi']>= 0.05 and G.node[i]['Pi']< 0.65):
                G.node[i]['role']='R2'
                H.node[i]['role']='R2'        

            elif (G.node[i]['Pi']>= 0.65 and G.node[i]['Pi']< 0.8):
                G.node[i]['role']='R3'
                H.node[i]['role']='R3'
               
            elif round(G.node[i]['Pi']) >= 0.80:
               
                G.node[i]['role']='R4'
                H.node[i]['role']='R4'
               



    num_R6=0.
#now i modify the criterium, according to the diff. layers:
#################
    for i in list_nodes_GC:

        if float(G.node[i]['Pi']) >0:


            if (float(G.node[i]['zi']) >= 1.0/(coef_layer*float(G.node[i]['Pi']))): #it is a R6
                G.node[i]['role']='R6'
                H.node[i]['role']='R6'
                num_R6+=1
             

            if G.node[i]['zi']>= 10.0: # for the guy with over 1000 friends
                G.node[i]['role']='special_R6'
                H.node[i]['role']='special_R6'
                num_R6+=1

# write zscore-Participation to a file
    file1 = open(dir+info_name2+"_zscore_vs_ParticipationCoef_diff_layers"+str(coef_layer)+".dat",'wt')

    for i in list_nodes_GC:
        print >> file1, G.node[i]['Pi'],G.node[i]['zi']
 
    file1.close()




    num_R1=0.
    num_R2=0.
    num_R3=0.
    num_R4=0.
    num_R5=0.
  
    num_R7=0.

    for n in G.nodes():

        #print G.node[i]['role']
        if G.node[n]['role']=="R1":
            num_R1+=1
        elif G.node[n]['role']=="R2":
            num_R2+=1
        elif G.node[n]['role']=="R3":
            num_R3+=1
        elif G.node[n]['role']=="R4":
            num_R4+=1
        elif G.node[n]['role']=="R5":
            num_R5+=1
        elif G.node[n]['role']=="R7":
            num_R7+=1




# write fraction of diff. roles  to a file
    file5 = open(dir+info_name2+"fraction_diff_roles"+str(coef_layer)+".dat",'wt')   
    print >> file5, "R1s:",num_R1/len(G.nodes())
    print >> file5, "R2s:",num_R2/len(G.nodes())
    print >> file5, "R3s:",num_R3/len(G.nodes())
    print >> file5, "R4s:",num_R4/len(G.nodes())
    print >> file5, "R5s:",num_R5/len(G.nodes())
    print >> file5, "R6s:",num_R6/len(G.nodes())
    print >> file5, "R7s:",num_R7/len(G.nodes())
  
    file5.close()


    print "R1s:",num_R1/len(G.nodes()), "R2s:",num_R2/len(G.nodes()), "R3s:",num_R3/len(G.nodes()), "R4s:",num_R4/len(G.nodes()),"R5s:",num_R5/len(G.nodes()), "R6s:",num_R6/len(G.nodes()), "R7s:",num_R7/len(G.nodes())

    print "R1s:",num_R1, "R2s:",num_R2, "R3s:",num_R3, "R4s:",num_R4,"R5s:",num_R5, "R6s:",num_R6, "R7s:",num_R7

# write the list of lists (communities) sorted by role to a file
    list_roles=["R1","R2","R3","R4","R5","R6","R7"]   


    file2 = open(dir+"list_of_communities_"+info_name2+"_by_role",'wt')
    for roles in list_roles:  # loop over roles
        for i in list_nodes_GC: # loop over nodes
            try:            
                if G.node[i]['role']==roles:
                    # print i,G.node[i]['role']
                    print >> file2, i,
            except KeyError: pass

        
        print >> file2,";",
        
    file2.close()






# write zscore-Participation with info about communities to a file
    #file3 = open(dir+info_name2+"_zscore_vs_ParticipCoef_with_comm_info_diff_layers"+str(coef_layer1)+"_"+str(coef_layer2)+".dat",'wt')

    file3 = open(dir+info_name2+"_zscore_vs_ParticipCoef_with_comm_info_diff_layers"+str(coef_layer)+".dat",'wt')

    for label in label_comm:
        for i in list_nodes_GC:
            if G.node[i]['community_index']==label:

                print >> file3, G.node[i]['Pi'],G.node[i]['zi']

        print >> file3,"\n"  # extra line to separate communities
    file3.close()




# write zscore-Participation for the scatter plot, just separating into R6 or non-R6

    file3 = open(dir+info_name2+"_zscore_vs_ParticipCoef_R6_nonR6.dat",'wt')


    print "R6:",       
    for node in G.nodes():
       
        if G.node[node]['role']=="R6" or G.node[node]['role']=="special_R6":

                print >> file3, G.node[node]['Pi'],G.node[node]['zi']
                print node,G.node[node]['label']

                if G.node[node]['role']=="special_R6":
                    print "special R6", node, G.node[node]['label']
                   # raw_input()


    print >> file3,"\n"  # extra line to separate R6s from non-R6s


   # raw_input()

    print "nonR6:",          
    for node in G.nodes():  
         
        if G.node[node]['role']!="R6" and G.node[node]['role']!="special_R6":

                print >> file3, G.node[node]['Pi'],G.node[node]['zi']
                print node,


    file3.close()







#create a new gml file with the added atributes:

   # nx.write_gml(H,name+"_roles_diff_layers"+str(coef_layer1)+"_"+str(coef_layer2)+".gml")

    nx.write_gml(H,name+"_roles_diff_layers"+str(coef_layer)+".gml")

##ojoooo! los atributos zi y Pi que le doy a los nodos en el subgrafo G (GC)
# tb los tienen los correspondientes nodos en H (total)



if __name__== "__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]   
    
        main(name)

    else:
        print "Usage: python program_name path/graph_file_name.gml"
