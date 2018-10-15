#!/usr/bin/env python

"""
Created by Julia Poncela on Ag. 2011.

Given a csv file containing percentage_weight_change and other variables
for the users, and provided the values for the coefficients in the linear model,
it returns a .dat file for the scatter plot Predicted_percentage_weight_change vs Observed.

"""


import sys
import os
import csv


 
def main(file_name,flag):

  
  

    if flag=='1': #for Isolated Users

        dir=file_name.split('isolated_')[0]  
        result= csv.reader(open(file_name, 'r'), delimiter=',')   


        C0= 3.3     # interception
        C1=-0.19     # iBMI
        C2=-0.04    # w-ins
        C3= 0.0     #homophily
        C4= 0.0      #k
        C5= 0.0      #R6s
        dir=dir+"IU"

        file1 = open(dir+"_scatter_plot_predicted_vs_observed.dat",'wt')

#id, ck_id, initial_weight, weigh_ins, activity, weight_change, percentage_weight_change, time_in_system, age, height, initial_bmi, final_bmi

        cont=0
        for row in result:        
            if row[0] != 'id':  # i exclude the first line 
                       
                if float(row[10])<=40. :  # to exclude false data IBMI>60
     
                    predicted=C0+ C1*float(row[10])+ C2*float(row[3])
                    observed=row[6]
                #  print predicted,  observed         
                    print >>file1,predicted,  observed                 
                

                else:
                    print "# wi:",row[3],"\t w:",float(row[2])*0.45359237,"\t %wc:",row[6],"\t h:",float(row[9])*2.54,"\t ibmi:",row[10],"\t fbmi:",row[11]
                    cont+=1
        file1.close()

        print "# excluded users:",cont


    elif flag=='2': #for Small Clusters

        dir=file_name.split('method3_adh')[0]  
        result= csv.reader(open(file_name, 'r'), delimiter=' ')   
  

        C0=-2.0 
        C1= 0.0
        C2=-0.06
        C3= 0.22
       
        dir=dir+"SC"

        file1 = open(dir+"_scatter_plot_predicted_vs_observed.dat",'wt')

#label pwc act log_act wi wi/12 ibmi sqrt_ibmi k log_k t naw
        cont=0
        for row in result:        
            if row[0] != 'label':  # i exclude the first line 

                if float(row[6])<=40.0 :
                    if row[11]!='nan':               
                        predicted=C0+ C1*float(row[6])+ C2*float(row[4])+ C3*float(row[11])
                        observed=row[1]
                       # print predicted,  observed         
                        print >>file1,predicted,  observed      
                    else:
                        predicted=C0+ C1*float(row[6])+ C2*float(row[4])
                        observed=row[1]
                        #print predicted,  observed  , "nan friends!"       
                        print >>file1,predicted,  observed      
                else:
                    print "# wi:",row[4],"\t ibmi",row[6]             
                    cont+=1
        file1.close()
        print "# excluded users:",cont

    elif flag=='3': # for GC

        dir=file_name.split('method3_adh')[0]  
        result= csv.reader(open(file_name, 'r'), delimiter=' ')   
  

        C0=-0.04   
        C1=-0.1 
        C2=-0.06
        C3=0.0
        C4=-0.21
        C5=0.0
        dir=dir+"GC"


#label pwc act log_act wi wi/12 ibmi sqrt_ibmi R6 R6_2 k log_k cs cs_2 t naw
        cont=0
        file1 = open(dir+"_scatter_plot_predicted_vs_observed.dat",'wt')
        for row in result:        
            if row[0] != 'label':  # i exclude the first line                              
                if float(row[6])<40.0:
                    predicted=C0+ C1*float(row[6])+ C2*float(row[4])+ C3*float(row[15])+ C4*float(row[10])+ C5*float(row[8])
                    observed=row[1]
                   # print predicted,  observed         
                    print >>file1,predicted,  observed                      
                else:
                    print "# wi:",row[4],"\t ibmi:",row[6]           
                    cont+=1

        file1.close()
        print "# excluded users:",cont



    else:
        print "wrong case scenario"
      

   
   




####################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        flag=sys.argv[2]
        main(file_name,flag)

    else:
        print "usage: python program.py path/file_name.csv  1 or 2 or 3 (IU, SC or GC respectively)"

    
