
#! /usr/bin/env python

"""
Created by Julia Poncela of January 2013

Get some statistics on time series cutting from the database



"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import histograma_gral
import histograma_bines_gral

 
def main ():


      
    file2=open("./Results/Scatter_plot_length_slope_lin.dat",'wt')
    file3=open("./Results/Scatter_plot_tau_deltaY_exp.dat",'wt')
   

    file4=open("./Results/Summary_results_cutting_time_series.dat",'wt')
   



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    query="""select * from weigh_in_cuts order by id, start_day""" 
    result = db.query(query)  # is a list of dict.


    list_distinct_users=[]
    list_num_segments_per_user=[]

    list_quality_values_lin=[]   #DW score
    list_quality_values_con=[]   #DW score
    list_quality_values_exp=[]   #DW score


    list_pairs_tau_deltaW=[]
    list_pairs_slope_time_length=[]

    num_segments=0
    num_lin_segments=0
    num_con_segments=0
    num_exp_segments=0
    num_isolates=0

    num_segments_per_user=0
    for line in result:  # each line is a dict, each line is a segment
       
        user=line['ck_id']
        fit_type=str(line['fit_type'])
        start_day=int(line['start_day'])
        stop_day=int(line['stop_day'])
        start_weight=float(line['start_weight'])
        stop_weight=float(line['stop_weight'])
       
          


        if fit_type != "isolated":        # isolated datapoint (with gaps at both sides)
            num_segments+=1
          
            try:
                quality=float(line['quality'])
            except TypeError:
                print user
                raw_input()#                pass  # isolated points dont have quality



       #parameters for linear:  1:cte,  2:slope. for exponential:  1:cte, 2:multiplicative_cte, 3:multipli_cte_in_the_exp
            param1=float(line['param1'])  

            try:
                param2=float(line['param2'])

            except TypeError:
                print "\nconstant segment!", user
                param2=0.


            try:
                param3=float(line['param3'])
            except TypeError:  pass  # cos the linear segments dont have a param3

           
            
            print "\n",user

            if user not in list_distinct_users:
                list_distinct_users.append(user)
                if num_segments_per_user!=0:
                    list_num_segments_per_user.append(num_segments_per_user)  # i save the value from the previous user before starting the count for this one.
                
                num_segments_per_user=1
            else:
                num_segments_per_user+=1




            

            if fit_type=="linear"  or fit_type=="constant":
                
               
                if fit_type=="linear":
                    num_lin_segments+=1
                    list_quality_values_lin.append(quality)
  
                elif fit_type=="constant":
                    num_con_segments+=1
                    list_quality_values_con.append(quality)



                tupla=[]
               
                tupla.append(float(stop_day-start_day+1.))
                tupla.append(param2)   
                list_pairs_slope_time_length.append(tupla)   



                
            elif fit_type=="exponent":
                num_exp_segments+=1
                
                list_quality_values_exp.append(quality)

                tupla=[]            
                
                tupla.append(1./param3)   
                tupla.append(float(stop_weight-start_weight))  # FAKE VALUES FOR NOW!!!!  CAMBIAR ESTO POR LOS NOMBRES DE LOS CAMPOS QUE AUN NO EXISTEN: startY , stopY 
                
                

               
                
                list_pairs_tau_deltaW.append(tupla)   
                
            else:
                print fit_type,"nor lin nor exp!",type(fit_type),
                
                
 
        else:
            num_isolates+=1

    histograma_gral.histograma(list_num_segments_per_user,"./Results/Distribution_num_segments_per_user.dat")



    for item in  list_pairs_slope_time_length:       
        print >> file2, item[0],item[1]
    file2.close()





    for item in  list_pairs_tau_deltaW:        
        print >> file3, item[0],item[1]
    file3.close()




 
    print >> file4, "Summary results cutting time series:\n\n"
    
    print >> file4,"Number of users:",len(list_distinct_users), "(with at least 20 weigh-ins)"
    print >> file4,"Number of segments:", num_lin_segments+num_con_segments+num_exp_segments  #not including one-point segments   
    print >> file4,"Average number of segments per individual:",num_segments/float(len(list_distinct_users))
    print >> file4,"Number of one-point segments:",num_isolates
    print >> file4, "Number segments by type:"
    print >> file4, "    Linear: ",num_lin_segments
    print >> file4, "    Constant: ",num_con_segments
    print >> file4, "    Exponential: ",num_exp_segments,"\n"
    print >> file4,"Regarding the goodness of the fits, DW average score:"
    print >> file4, "    Linear: ",numpy.mean(list_quality_values_lin)
    print >> file4, "    Constant: ",numpy.mean(list_quality_values_con)
    print >> file4, "    Exponential: ",numpy.mean(list_quality_values_exp)

    file4.close()


    print len(list_quality_values_lin), list_quality_values_lin
    print len(list_quality_values_con), list_quality_values_con
    print len(list_quality_values_exp), list_quality_values_exp


    histograma_bines_gral.histograma_bins(list_quality_values_lin,10,"./Results/Distribution_DW_scores_lin_segments.dat")
    histograma_bines_gral.histograma_bins(list_quality_values_con,10,"./Results/Distribution_DW_scores_const_segments.dat")
    histograma_bines_gral.histograma_bins(list_quality_values_exp,10,"./Results/Distribution_DW_scores_exp_segments.dat")



    print "\n done!"


#########################
          
if __name__== "__main__":
   # if len(sys.argv) > 2:
       
        main()
#    else:
 #       print "usage: python whatever.py path/network_file1_R6s_info.gml  path/network_file2_kshell_info.gml "

   
    
     

##############################################
