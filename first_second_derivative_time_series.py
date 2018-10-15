#! /usr/bin/env python

"""
Created by Julia Poncela of September 2011

Given a file for a time serie, calculates the numerical first and second
derivatives, and prints out the new time series.




"""



import sys
import os
from datetime import *
import math
import numpy



def main ():



    for index_file in range(50):
        index_file+=1

        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50"   # to get the FIRST derivative


       
        file1=open(file_name+"_derivative_pwc.dat",'wt')



        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()


        file1=open(new_name+"second_derivative_pwc.dat",'wt')

   

        t0=0.0
        pwc0=0.0
        
        cont_lines=1
        for line in list_lines_file:

        #print line: index  weight  %weight_ch  BMI  days

            list=line.split(" ")
      


       
            if list[4]!="0:00:00\n":  # i avoid the first line   #for the first derivative

           
            
                if cont_lines<2:

                    t1=float(list[4])                
                    pwc1=float(list[2])
                    
                    cont_lines+=1
               

                else:
                    
                    t2=float(list[4])
                    pwc2=float(list[2])
           

                    derivative= (pwc2-pwc0)/ (t2-t0)   

                    print t1,derivative#, "because (", pwc2,"-",pwc0,")/(",t2,"-",t0,")"
                    print >> file1, t1, derivative

               





                    t0=t1   #update the values for the next point
                    t1=t2
                    pwc0=pwc1
                    pwc1=pwc2
                

                #print "updated values:","t0:",t0,"t1:",t1,"pwc0:",pwc0,"pwc1:",pwc1

               
                    cont_lines+=1


        file1.close()



            


      






#########################
          
if __name__== "__main__":
   
    main()
    
     
   

##############################################

 
