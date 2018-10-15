import subprocess as sp
import networkx as nx
import GraphRandomization_to_play_with as mcg
import sys


#import shlex
#print "print some command line"
#command_line=raw_input()
#arguments = shlex.split(command_line)
#print arguments
#raw_input()
#p = sp.Popen(arguments)


#p = sp.Popen(["python","hola.py"])



def main(input_file_name,iteraciones):

   #ojo!! lo que entra al sistema por argv sera de tipo STRING!!!

    
    p = sp.Popen(["python","communities_CK_GC_same_code.py",input_file_name],stdin=sp.PIPE, stdout=sp.PIPE)  #le mando ejecutar otro programa 


    salida=p.communicate()  #es una tupla en la q guarda lo que sale 
         # por pantalla en el programa, de la forma: ('todo_lo_que_sea', None)
   
    #print "0:",salida[0]  el primer elemento de la tupla (==todo lo escrito por pantalla en el programa anterior)

    lista=[]
    lista=salida[0].split() #parto la cadena de todo lo impreso por pantalla
    
    
    mod=float(lista[0])  # the modularity of the original network
   

    print "mod:", mod


    H=nx.read_edgelist(input_file_name) # create the network from the original input file  

    components=nx.connected_component_subgraphs(H)  
   
    G=components[0] # i take just the GC as a subgraph to perform the community ID algorithm
                    # G is a list of tuples:  [(n1,n2),(n3,n4),(n2,n3),...]




    

    for iteracion in range(int(iteraciones)):
    #print "iter in piping:", iteracion

        H= mcg.mc_randomize_m(G,iteracion,input_file_name) #randomized version of G and print it to a file that i will read next:


        p = sp.Popen(["python","communities_CK_GC_same_code.py",input_file_name+'rand_version'+str(iteracion)])  #i use the same code for commID, applied to the rand_version





    espera=p.wait()  #esto esta aki para asegurarme de que no llama al sig progr antes de que acabe el anterior (que le cuesta!)


    p = sp.Popen(["python","comparison.py", input_file_name, str(iteraciones),str(mod)])





if __name__== "__main__":
    if len(sys.argv)>2:
        input_file_name=sys.argv[1]   
        iteraciones=sys.argv[2]
        main(input_file_name,iteraciones)

    else:
        print "Usage: python program_name path/graph_file_name #_iterations"
