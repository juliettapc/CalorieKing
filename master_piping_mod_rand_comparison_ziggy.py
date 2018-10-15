#! /usr/bin/env python



"""
Created by Julia Poncela on January 2011.

It analyzes the community structure of the giant component of a given network, comparing the value of the modularity with the average value of n randomized versions of it, to determine if it is statistically significant.

It prints out the results in a 'path/network_file_name'+'_mod_rand_comparison' file

It takes as arguments: path/network_file_name  n


Made to run with Ziggy, and distribute the n calculations among all computers from the Lab.


"""



import subprocess as sp
import networkx as nx
import GraphRandomization_modified  as mcg
import sys
from ziggy import hdmc
from ziggy.hdmc import hadoop_config as config
import ziggy.hdmc.hdfs as hdfs


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
                
    deleting_name=input_file_name.split("/")[-1]+'_mod_rand_comparison'

    hdfs.rm(deleting_name) # delete output file from previous runs, so it wont freak out. they are in the directory where ziggy works: 
# /usr/local/hadoop/bin/
 



    p = sp.Popen(["python","communities_CK_GC_same_code_ziggy.py",input_file_name],stdin=sp.PIPE, stdout=sp.PIPE)  #le mando ejecutar otro programa 


    salida=p.communicate()  #es una tupla en la q guarda lo que sale 
         # por pantalla en el programa, de la forma: ('todo_lo_que_sea', None)

   

    lista=[]
    lista=salida[0].split()
   
    
    mod=float(lista[0])
   # print "mod:", mod

    iteraciones=int(iteraciones)



   

    randomization_mapper='randomizing_commID_routine.py'
    output_name='mod_rand_comparison'
    supporting_files=["GraphRandomization_modified.py","communities_CK_GC_same_code_ziggy.py",input_file_name]
    mean_collector='comparison_ziggy.py'  #None


    hdmc.submit_inline(randomization_mapper, output_name, iteraciones, supporting_files, mean_collector, debug=False, num_mappers = config.num_map_tasks)


   

if __name__== "__main__":
    if len(sys.argv)>2:
        input_file_name=sys.argv[1]   
        iteraciones=sys.argv[2]
        main(input_file_name,iteraciones)

    else:
        print "Usage: python program_name path/graph_file_name #_randomizations"
