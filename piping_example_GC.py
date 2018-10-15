import subprocess as sp
import networkx as nx
import GraphRandomization_to_play_with as mcg

#import shlex
#print "print some command line"
#command_line=raw_input()
#arguments = shlex.split(command_line)
#print arguments
#raw_input()
#p = sp.Popen(arguments)


#p = sp.Popen(["python","hola.py"])


p = sp.Popen(["python","communities_CK_one_network_GC.py"],stdin=sp.PIPE, stdout=sp.PIPE)  #le mando ejecutar otro programa 


salida=p.communicate()  #es una tupla en la q guarda lo que sale 
#print salida # por pantalla en el programa, de la forma: ('todo_lo_que_sea', None)

#lista=[]
#lista=salida[0].split(" ") 
#raw_input() 

mod=float(salida[0])
print mod



network_file_name="10_points_network/data/friend_graph_all0" # the same file used by the program communities_...py


H=nx.read_edgelist(network_file_name) # create the network from the original input file  

components=nx.connected_component_subgraphs(H)  
   
G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]




iteraciones=10 # how many randomized networks wanna get

for iteracion in range(int(iteraciones)):
    #print "iter in piping:", iteracion

    H= mcg.mc_randomize_m(G,iteracion) #randomized version of G (and print it to a file)


    p = sp.Popen(["python","communities_CK_randomized_version_with_main.py", str(iteracion)])



raw_input()  #esto esta aki para asegurarme de que no llama al sig progr antes de 
#               que acabe el anterior (que le cuesta!)


p = sp.Popen(["python","comparison.py", str(iteraciones),str(mod)])


