#! /usr/bin/env python

"""
Created by Julia Poncela of February 2012

It calculates the average of each column for a file with multiple columns

"""



import sys
import os
from scipy import stats
import scipy
import math
import numpy


def main ():

    file_name="Mech_Turk_experiment_input.dat"       
    
    file=open(file_name,'r')
    list_lines_file=file.readlines()

    cont=0
    list_initial=[]
    list_final=[]
    list_w_ins=[]
    list_num_days=[]
    for line in list_lines_file:   #i create the list for the original file
        if cont>0:
            list=line.split("\t")   #  initial_weight	final_weight	num_w-ins	num_days
        
           
                      
            list_initial.append(float(list[0]))
            list_final.append(float(list[1]))
            list_w_ins.append(float(list[2]))
            list_num_days.append(float(list[3]))
            

        cont+=1



    print "avg initial weight:",numpy.mean(list_initial),"\navg final weight:",numpy.mean(list_final),"\navg #w ins:",numpy.mean(list_w_ins),"\navg num days:",numpy.mean(list_num_days),"\n\n"


    print "median initial weight:",numpy.median(list_initial),"\nmedian final weight:",numpy.median(list_final),"\nmedian #w ins:",numpy.median(list_w_ins),"\nmedian num days:",numpy.median(list_num_days)

#########################
          
if __name__== "__main__":
   
    main()

   
##############################################

 
