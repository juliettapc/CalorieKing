#! /usr/bin/env python
"""
Created by Julia Poncela on January 2011.

On the one hand, it takes the modularity value of a network ('path/network_file_name'), on the other hand it takes the nodularity values for a number of randomized versions of it, calculates the average and standard deviation of those, and compare both.

It prints out a 'path/network_file_name'+'_mod_rand_comparison' file with the results.

Intended to be called from within master_piping_mod_rand_comparison.py code

"""


import sys
import math


#aki input_file_name es el original que introduzco por pantalla



def main():

    #name="modularidad.txt"          # to test  this code on its own
    #data = open(name).readlines() 



    data=sys.stdin.readlines()  # tomo los datos del archivo de output que genera ziggy con los print

    modularity=[]                        
    for line in data:              
        modularity.append(float(line)) # los valores de la modularidad

    print modularity

    mod=float(modularity[0])
    lim_sup=len(modularity) # number of rand_mod values that i've got
    print "lim:",lim_sup


    average_modularity=0.0
    for i in range(1,lim_sup):   
        average_modularity=average_modularity+float(modularity[i])   

    average_modularity=average_modularity/(float(lim_sup)-1.0)
  


    sigma=0.0
    for i in range(1,lim_sup):
        print i
        sigma=sigma+(float(modularity[i])-average_modularity)**2


    sigma=sigma/float(lim_sup)
    sigma=math.sqrt(sigma)

    z_score=(mod-average_modularity)/sigma

    print "\n","Actual Modularity:","%.5f" %mod
    print "rand-versions <M>:","%.5f" %average_modularity, "(", sigma,")"
    print "z_score:","%.5f" %z_score
            
  # todo lo que imprima en el reducer va a un archivo en el hadoop distributed file system







if __name__ == "__main__":   
    main()
