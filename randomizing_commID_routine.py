
import subprocess as sp
import networkx as nx
import GraphRandomization_modified as mcg






#it needs to know  'input_file_name' POR AHORA, A MANO!!!

input_file_name="5_points_network/data/friend_graph_all0"
iteracion=1
#POR AHORA, A MANO!!!



H=nx.read_edgelist(input_file_name) # create the network from the original input file  

components=nx.connected_component_subgraphs(H)  
   
G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm.   G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]





H= mcg.mc_randomize_m(G,iteracion,input_file_name) #randomized version of G and print it to a file that i will read next:

 

p = sp.Popen(["python","communities_CK_GC_same_code.py",input_file_name+'_rand_version'+str(iteracion)])  #i use the same code for commID, applied to the rand_version





espera=p.wait()  #esto esta aki para asegurarme de que no llama al sig progr antes de 
#               que acabe el anterior (que le cuesta!)
