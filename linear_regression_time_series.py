 
#! /usr/bin/env python

"""
Created by Julia Poncela of Oct 2011

It makes the linear regression for the time series, only cutting at the point where the fit gets bad.

It doesnt take any arguments.

"""


import sys
import os
from scipy import stats
import scipy
import math
import numpy



def main ():


    min_lenght=30  # to cut the series



    for index_file in range(50):
        index_file+=1

        print index_file

        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50_t_points"       
        
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()


        file1=open(file_name+"_residuals.dat",'wt')


            

        x_values=[]
        y_values=[]


       
        for line in list_lines_file:
   
            list=line.split(" ")   # time, t, %weight_change

            x_values.append(float(list[0]))
            y_values.append(float(list[2]))


            
        list_series=[]
        list_series.append()
        for list_evolution in list_series:  # i analyze the current time serie (or fragment of it)       



        for max_index  in range(len(x_values)):

            if max_index >=2: # at least two points to calculate the fit
                partial_x_list=[]
                partial_y_list=[]
                for index  in range(len(x_values)):
                    if index <= max_index : 
                        partial_x_list.append(x_values[index])
                        partial_y_list.append(y_values[index])

                  

                slope, intercept, Corr_coef, p_value, std_err =stats.linregress(partial_x_list,partial_y_list)  # least squeares polinomial fit

           

                list_residuals2=[]
                for i in range(len(partial_x_list)):
                    actual_y=float(partial_y_list[i])
                    fit_value_y=float(intercept+slope*partial_x_list[i])
                    list_residuals2.append((actual_y-fit_value_y)*(actual_y-fit_value_y))

                
                print >> file1, x_values[max_index],y_values[max_index],scipy.mean(list_residuals2)/len(list_residuals2)

              

           


                    
            


    file1.close()



#########################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

