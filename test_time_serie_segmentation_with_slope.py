#! /usr/bin/env python

"""
Created by Julia Poncela of October 2011

Given a file for a non-stationary time serie, it calculates the optimum points to cut it, that mark different trends.

More info: It follows the method proposed by Fukuda, Stanley and Amaral PRL 69, 2004.



"""


import sys
import os
from datetime import *
import math
import numpy
import random
from scipy import stats




def main ():


    amplitude=1.
    delta_y=1.0


    origen_y=0
    slope=0.001
    final=0


    file_name="temporal_series/most_weigh_ins/test_time_series"
    
    
    file=open(file_name+".dat",'wt')
    file1=open(file_name+"_t_points_amplitude"+str(amplitude)+"_deltaY"+str(delta_y)+"_slope"+str(slope)+".dat",'wt')      #"slope1.dat",'wt')   



    list_times=[]
    values_time_serie=[]

    
    for i in range(259):
        if i <=150:
            value=origen_y-float(i)*slope+random.random()*amplitude
            #value=random.random()*amplitude
            print >> file, i,value
            values_time_serie.append(value)
            list_times.append(i)
            final=value
        elif i >150 and i <=175:
            value=final+random.random()*amplitude
            #value=delta_y+random.random()*amplitude
            print >> file, i,value
            values_time_serie.append(value)
            list_times.append(i)
        elif i > 175:
            #value=2.0*delta_y+random.random()*amplitude
            value=final+delta_y+random.random()*amplitude
            print >> file, i,value
            values_time_serie.append(value)
            list_times.append(i)

    num_lines=len(values_time_serie)
    file.close()



    t_max=0.0
    index_max_t=0
    for index in range(num_lines):
           
            if index>=1  and index < num_lines-1:  # to cut the serie, at least need one point in each list

                list1=[]
                list2=[]
                
                for x1 in range(num_lines):
                    if x1 <= index:
                        list1.append(values_time_serie[x1])
                    else:
                        list2.append(values_time_serie[x1])

         





                mu1=numpy.mean(list1)
                mu2=numpy.mean(list2)
                
                sd1=numpy.std(list1)
                sd2=numpy.std(list2)
                
                N1=float(len(list1))
                N2=float(len(list2))


               
                S_D=math.sqrt(((N1-1)*sd1*sd1 + (N2-1)*sd2*sd2)/(N1+N2-2))*math.sqrt(1.0/N1 + 1.0/N2)
                t=math.fabs((mu1-mu2)/S_D)
                
               # print index,mu1,mu2,N1,N2,S_D,t
    #        raw_input()
                

                if t > t_max:
                    t_max=t
                    index_max_t=index

                print >> file1, list_times[index],t,values_time_serie[index]


                #print >> file1,0.0, 0.0,values_time_serie[index], t, list_times[index]
                


    file1.close()


    
    eta=4.19*math.log(float(num_lines))-11.54
    delta=0.40
    nu=float(num_lines)-2.0
    
    a=delta*nu  #for the Incomplete beta function
    b=delta
    x=nu/(nu+t_max*t_max)
    I=stats.mstats.betai(a,b,x)
    
    significance_t_max=math.pow((1.0-I),eta)     #Return x raised to the power y. 
    
    
    print "amplitude:",amplitude,"delta_y:", delta_y,"slope:",slope
    
    print "max_t:", t_max, "at time:",list_times[index_max_t],"significance:",significance_t_max,"           I:",I,"eta:",eta,"x:",x,"a:",a,"N:",num_lines
        


#########################
          
if __name__== "__main__":

    main()
    
     

##############################################
