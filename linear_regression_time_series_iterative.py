 
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


    for index_file in range(50):
        index_file+=1

        print "\n\n file:",index_file

        file_name="temporal_series/most_weigh_ins/weigh_in_time_serie_days"+str(index_file)+"_top50_t_points" 
        
        file=open(file_name+".dat",'r')
        list_lines_file=file.readlines()


        file1=open(file_name+"_residuals.dat",'wt')


            

        x_values=[]
        y_values=[]


        evolution=[]
        for line in list_lines_file:   #i create the list for the original time evolution
   
            list=line.split(" ")   # time, t, %weight_change

            point=[]
            x_values.append(float(list[0]))
            y_values.append(float(list[2]))

            point.append(float(list[0]))
            point.append(float(list[2]))

            evolution.append(point) # list for the evolution of the system: [[time1,value1],[time2,value2],[],...]


        list_cutting_times=[]
        list_series=[]
        list_series.append(evolution)
        for list_evolution in list_series:  # i analyze the current time serie (or fragment of it)                              

            for max_index  in range(len(list_evolution)):

                if max_index >=10: # at least ten points to calculate the linear regression
                    partial_x_list=[]
                    partial_y_list=[]
                    partial_MSER_list=[]
                    for index  in range(len(list_evolution)):
                        if index <= max_index : 
                            partial_x_list.append(list_evolution[index][0])
                            partial_y_list.append(list_evolution[index][1])
                                          
                    slope, intercept, Corr_coef, p_value, std_err =stats.linregress(partial_x_list,partial_y_list)  
                                                            # least squeares polinomial fit

           
               
                    list_residuals2=[]
                    for i in range(len(partial_x_list)):

                        actual_y=float(partial_y_list[i])
                        fit_value_y=float(intercept+slope*partial_x_list[i])
                        list_residuals2.append((actual_y-fit_value_y)*(actual_y-fit_value_y))
                        
                
                    MSER=scipy.mean(list_residuals2)/len(list_residuals2)
                  #  print >> file1, x_values[max_index],y_values[max_index],MSER

                    list_evolution[max_index].append(MSER)  #  [[time1,value1,MSER1],[time2,value2,MSER2],[],...]
                    partial_MSER_list.append(MSER)

                else:
                  #  print >> file1, x_values[max_index],y_values[max_index],"None"
                    list_evolution[max_index].append("None")

         #   print >> file1, "\n" # to separate segments 


            min_MSER=1000000.0
            for i in range(len(list_evolution)):                
                if list_evolution[i][2]<=min_MSER:
                    min_MSER=list_evolution[i][2]
                    index_min_MSER=i

          
            if int(list_evolution[index_min_MSER][0])<int(list_evolution[-1][0]):
                list_cutting_times.append(list_evolution[index_min_MSER][0])
               # print "min MSER:",min_MSER," for index:",index_min_MSER, "corresponding to time:",list_evolution[index_min_MSER][0] ,   # i dont consider the last point as a cutting point







            list_rest_serie=[]
            for index  in range(len(list_evolution)):
                if index > index_min_MSER:
                    point=[]
                    point.append(list_evolution[index][0])
                    point.append(list_evolution[index][1])    
                    
                
                    list_rest_serie.append(point)

            
            if len(list_rest_serie)>=20:  # i only allow to cut a serie down to a segment of 20 points
               # print "length of the rest of the serie:",len(list_rest_serie)
                list_series.append(list_rest_serie)
            else:
                pass# print "rest of the list too short, i am not cutting!"






             

        list_cutting_times=sorted(list_cutting_times)
        
        print "     # segments:",len(list_cutting_times)+1
           


        cut_inferior=0.0
        if len(list_cutting_times)!=0:

            for cut in list_cutting_times:
                
                for point in  evolution:   # original list for the evolution of the system: [[time1,value1],[time2,value2],[],...]

                    if  point[0]> cut_inferior and point[0]<= cut:
                        print >> file1, point[0],point[1]
                            
                print >> file1, "\n"

                if cut == list_cutting_times[-1]:  #for the last segment

                    for point in evolution:
                        
                        if point[0]>= cut:                        
                            print >> file1, point[0],point[1]

                cut_inferior=cut
                print >> file1, "\n"
        else:
            for point in evolution:            
                print >> file1, point[0],point[1]
                        





                

                    


      
        file1.close()



#########################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

