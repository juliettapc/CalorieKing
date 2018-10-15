#! /usr/bin/env python


import sys
import os
import numpy
import csv
from matplotlib import mlab

def main():
   


    input_name="/home/staff/julia/at_Northwestern/calorieking/time_series/fake_time_series/Batch_830054_batch_results_just_time_series.csv"  
    resultado= csv.reader(open(input_name, 'rb'), delimiter=',')#, quotechar='"')


    file1=open("./fake_time_series/all_rearrange_fake_time_series.dat",'wt')

    cont_valid_series=0
    cont_lines=-1
    for row in resultado:      
     
        cont_lines+=1
        if cont_lines>0:  # the first line is just the headers

                file2=open("./fake_time_series/rearrange_fake_time_series"+str(cont_lines)+".dat",'wt')

                cont_week=1
                list_weigh_ins=[]
                for item in row:
                    try:
                        if float(item)>=200. and float(item)<=400. : # IS IT OK TO JUST REMOVE BAD DATA FOR PART OF A TIME SERIES???
                            pair_week_weight=[]
                            pair_week_weight.append(cont_week)
                            pair_week_weight.append(float(item))

                            list_weigh_ins.append(pair_week_weight)
                        else:
                         print "bad data in line", cont_lines+1,"week",cont_week

                    except ValueError:
                        print  "empty value in line:",cont_lines+1
                      
                    cont_week+=1


                print "line:",cont_lines+1
                if len(list_weigh_ins)>2:
                    for pair in list_weigh_ins:
                        print pair[0],pair[1]
                        print >> file1,pair[0],pair[1]
                        print >> file2,pair[0],pair[1]

                    print >> file1,"\n"
                    cont_valid_series+=1
                else:
                    print "too short a time series"
                #raw_input()
    print "total # of valid time series:",cont_valid_series
####################################
######################################
if __name__ == '__main__':
   
    main()
   
