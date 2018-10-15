#! /usr/bin/env python
"""
Created by Julia Poncela on January 2011.

On the one hand, it takes the modularity value of a network ('path/network_file_name'), on the other hand it takes the modularity values for a number of randomized versions of it, calculates the average and standard deviation of those, and compare both.

It prints out a 'path/network_file_name'+'_mod_rand_comparison' file with the results.

Intended to be called from within master_piping_mod_rand_comparison.py code

"""


import sys
import math


#aki input_file_name es el original que introduzco por pantalla

def main(input_file_name,iteraciones,mod):

    mod=float(mod)
    iteraciones=int(iteraciones)
    data=[]

    mod_list=[]
    average_modularity=0.0    
    for i in range(iteraciones): # leo los ficheros rand_summary_modularity... y hago la media
        name=input_file_name+'_rand_version'+str(i)+'_modularity_analysis_GC'
        file = open(name).readlines()  #devuelve una lista, cuyos elem son las lineas del fichero leido
       

        cadena=str(file[1])  #en el archivo: primera fila titulos, segunda datos

      
        lista=cadena.split(" ") #devuelve una lista, cuyos elem son el resultado de saparar cadena[0], usando los espacios en blanco que contuviera
       
       
        average_modularity=average_modularity+float(lista[5])
      

       
        mod_list.append(lista[5])


    average_modularity=average_modularity/float(iteraciones)
   

    sigma=0.0
    for i in range(int(iteraciones)):
        sigma=sigma+(float(mod_list[i])-average_modularity)**2


    sigma=sigma/float(iteraciones)
    sigma=math.sqrt(sigma)

    z_score=(mod-average_modularity)/sigma

    print "\n","Actual Modularity:","%.5f" %mod
    print "rand-versions <M>:","%.5f" %average_modularity, "(", sigma,")"
    print "z_score:","%.5f" %z_score

   



    file = open(input_file_name+'_mod_rand_comparison','wt')    
    print >> file, "Actual Modularity:","%.5f" %mod, "\nrand-versions <M>:","%.5f" %average_modularity, "(", sigma,")", "-----",iteraciones, "iter","\nz_score:","%.5f" %z_score
            
    file.close()








if __name__ == "__main__":
    if len(sys.argv) >3:
        input_file_name=sys.argv[1]
        iteraciones=sys.argv[2]
        mod=sys.argv[3]
    main(input_file_name,iteraciones,mod)
