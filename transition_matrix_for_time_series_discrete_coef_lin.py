
#! /usr/bin/env python

"""
Created by Julia Poncela of November 2011

Given a set of files with the different trends for the CK time series, it calculates the transition probability matrix from every state to every state , by counting the number of times each transition occurs accros time series.


"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats



def main ():

    num_files=8924   #8924

    max_coef_exp=1000
    max_coef_slope=5   # +- that %pwc in one day!!


    tot_num_transitions=00   # across all users
    list_diff_states=[]
    list_all_transitions=[]
   
    file_name_lin="temporal_series/most_weigh_ins/all_cuts/scatter_plot_parameters_lin.dat"
    file_lin=open(file_name_lin,'wt')

    file_name_exp="temporal_series/most_weigh_ins/all_cuts/scatter_plot_parameters_exp.dat"
    file_exp=open(file_name_exp,'wt')


    for index_file in range(num_files):
        index_file+=1

        try: 
                                                           
            file_name="temporal_series/most_weigh_ins/all_cuts/weigh_in_time_serie_days"+str(index_file)+"_filters.cuts"
            
        #file_name="temporal_series/most_weigh_ins/test_file_to_create_transition_matrix_"+str(index_file) 
            file=open(file_name,'r')
            list_lines_file=file.readlines()
            
            dir=file_name.split("weigh_in_")[0]
        

################################
# lin: intersection + X*slope  #
#exponential: A+B*exp(lambda*t)#
################################

            cont_lines=1
            
            for line in list_lines_file:           
                
                list_one_line=line.split(" ")        
                
                trend=list_one_line[0]     # i characterize the current trend:
            
                if trend == "exp":               
                    coef1_exp=round(float(list_one_line[1]),2)   # we dont care about the interception
                    coef2_exp=round(float(list_one_line[2]),2)
                    coef3_exp=round(float(list_one_line[3]),2)
                    
                    if coef1_exp <= max_coef_exp and coef1_exp >= -max_coef_exp : 
                        if coef2_exp <= max_coef_exp and coef2_exp >= -max_coef_exp : 
                            if coef3_exp <= max_coef_exp and coef3_exp >= -max_coef_exp : 


                                if coef2_exp <0:   # i only care about linear increase/decrease                                  
                                        new_coef2_exp=-1.0
                                else:                                   
                                    new_coef2_exp=1.0

                                    

                                if coef3_exp <0:  

                                    if coef3_exp <-100:
                                        new_coef3_exp=-100
                                    elif coef3_exp <-20:
                                        new_coef3_exp=-20
                                    elif coef3_exp <-5:
                                        new_coef3_exp=-5                                                       
                                    elif coef3_exp <-0.01:
                                        new_coef3_exp=-0.01  
                                    elif coef3_exp <-0.001:
                                        new_coef3_exp=-0.001  

                                    else:
                                        new_coef3_exp=0                                   
                                else:
                                    if coef3_exp >100:
                                        new_coef3_exp=100
                                    elif coef3_exp >20:
                                        new_coef3_exp=20
                                    elif coef3_exp >5:
                                        new_coef3_exp=5                                                                   
                                    elif coef3_exp >0.01:
                                        new_coef3_exp=0.01 
                                    elif coef3_exp >0.001:
                                        new_coef3_exp=0.001 

                                    else:
                                        new_coef3_exp=0             



                                length=float(list_one_line[4])
                                state=trend+"_"+str(new_coef2_exp)+"_"+str(new_coef3_exp)#+"_"+str(coef3_exp)
                                if state not in list_diff_states:
                                    list_diff_states.append(state)
                                    #print "exp",coef1_exp,coef2_exp,coef3_exp,length, state
                                    
                                print >> file_exp,coef1_exp,coef2_exp,coef3_exp
                    else:
                        print "bad exp_coef in file", index_file, coef1_exp, coef2_exp, coef3_exp
            
                elif trend == "lin":
                    coef1_lin=round(float(list_one_line[1]),2)   # we dont care about the interception
                    coef2_lin=round(float(list_one_line[2]),2)
                    length=float(list_one_line[3])

                   
                    if coef2_lin <= max_coef_slope and coef2_lin >= -max_coef_slope : 

                            if coef2_lin <0:                            
                                if coef2_lin <-0.1:
                                    new_coef2_lin=-0.1
                                elif coef2_lin <-0.05:
                                    new_coef2_lin=-0.05
                                elif coef2_lin <-0.01:
                                    new_coef2_lin=-0.01
                                elif coef2_lin <-0.005:
                                    new_coef2_lin=-0.005
                                elif coef2_lin <-0.001:
                                    new_coef2_lin=-0.001
                                elif coef2_lin <-0.00001:
                                    new_coef2_lin=-0.00001
                                else:
                                    new_coef2_lin=0
                            else:                               
                                if coef2_lin >0.1:
                                    new_coef2_lin=0.1
                                elif coef2_lin >0.05:
                                    new_coef2_lin=0.05
                                elif coef2_lin >0.01:
                                    new_coef2_lin=0.01
                                elif coef2_lin >0.005:
                                    new_coef2_lin=0.005
                                elif coef2_lin >0.001:
                                    new_coef2_lin=0.001
                                elif coef2_lin >0.00001:
                                    new_coef2_lin=0.00001
                                else:
                                    new_coef2_lin=0
                                
                           

                            state=trend+"_"+str(new_coef2_lin)#+"_"+str(coef2_lin)
                            if state not in list_diff_states:
                                list_diff_states.append(state)
                        
                               #print "lin",coef1_lin,coef2_lin,length
                            print >> file_lin,coef1_lin,coef2_lin

                    else:
                        print "bad lin_coef in file", index_file, coef1_lin, coef2_lin


                if  len(list_lines_file) == 1: # if only one line in the file --> only one state --> diagonal term for the matrix
                    list=[]
                    list.append(state)
                    list.append(state)
                    list_all_transitions.append(list)
                    tot_num_transitions+=1.0
                        
                else :    # if more than one trend in the file
                    if cont_lines==1:
                        old_state=state
                    else:
                        new_state=state
                        list=[]
                        list.append(old_state)
                        list.append(new_state)
                        list_all_transitions.append(list)
                        
                        old_state=state # i update for the next transition
                        tot_num_transitions+=1.0
                        
                

                cont_lines+=1 
        except IOError:
            print index_file, "file doesnt exist"

    list_diff_states=sorted(list_diff_states)    # this is the order of the trends for the transition matrix

    print "#num of diff states:", len(list_diff_states)#, "namely:",list_diff_states 
    
    file_lin.close()  #for the scatter plot of the parameters
    file_exp.close()




########################i create the empty transition matrix
    matrix=[]
    for i in range(len(list_diff_states)):
        matrix.append([0.000]*len(list_diff_states))   #ojo!!!!!!!!!!!!!!! si la creo: matrix.append(list), con list=[0.]*len(list_diff_states), al modificar unos elementos, modificare otros sin querer!!!!!!!!!!!!!!!!!!!

##################################




    print "num transitions:",len(list_all_transitions)#,"  list transitions:",list_all_transitions ,"\n"  #ej.: [['exp_1.0_1.0_2.0', 'lin_3.0_1.0'], ['lin_3.0_1.0', 'lin_2.0_1.0'], ['exp_2.0_1.0_3.0', 'exp_2.0_2.0_1.0'], ...]


    cont_exp_to_lin=0
    cont_lin_to_exp=0
    for  transition in list_all_transitions:
       # print "\n\n looking for:", transition[0],transition[1]
        for i in range(len(list_diff_states)):           
            old_state=list_diff_states[i]
            for j in range(len(list_diff_states)):
              
                new_state=list_diff_states[j]
                #print  old_state, new_state 
               
                if transition[0]== old_state  and transition[1]== new_state  :
                    matrix[i][j]+=1.000
                    #print "  ",transition, matrix[i][j]  #, list_diff_states[i], list_diff_states[j]  
                    if old_state == 'exp_1.0_-0.01' and new_state== 'lin_0.01':
                    #print  old_state, new_state 
                        cont_exp_to_lin+=1
                    elif old_state == 'lin_0.01' and new_state== 'exp_1.0_-0.01':
                    #print  old_state, new_state 
                        cont_lin_to_exp+=1
                        


    print "old_state == 'exp_1_-1' and new_state== 'lin_1':",cont_exp_to_lin,"old_state == 'lin_1' and new_state== 'exp_1_-1':",cont_lin_to_exp
  
    file_name1="temporal_series/most_weigh_ins/cuts/transiton_probability_matrix_test.dat" 
    file1=open(file_name1,'wt')




    #print "\n\ntransition matrix:\n"
    #print "\t\t\t",

   # for item in list_diff_states:   # print the header
    #    print item," ",

    #print  "\n"

    for i in range(len(list_diff_states)):
        if "exp" in list_diff_states[i]:
            pass
            #print list_diff_states[i],"\t",
        else:
            pass#print list_diff_states[i],"\t\t",
        for j in range(len(list_diff_states)):            
           # print round(matrix[i][j]/tot_num_transitions,3),"             ",
            print >> file1,round(matrix[i][j]/tot_num_transitions,3),
            
       # print "\n"
        print >> file1,"\n"
           



    file1.close()


   

    #### PLOTGRACE IMPLEMENTATION ###
    # Draw the matrix


    from PlotGrace import plot_matrix  # i use a function from the module
                                      # and just modify some of the default options

    plot_matrix(matrix, dir+"transition_prob_matrix.agr",
                xticklabels = list_diff_states,
                yticklabels = list_diff_states,
                xticklabelangle = 90,
                colorscheme='YlOrRd',
                #logcolorbar=True,               
                reversecolorscheme = False,                
                mincolor=(255,255,255),                
                title="Transition Probabilities")






#     mx = dictmatrix(0.)   #a diff. way of doing it: feeding it a dicc. of dicc. instead of a list of lists
    
#     for i in range(len(list_diff_states)):
#         rowlabel = list_diff_states[i]
#         for j in range(len(list_diff_states)):
#             collabel = list_diff_states[j]
#             value = matrix[i][j]
#             mx.put(rowlabel,collabel,value)

#     plot_matrix(mx, "transition_prob_matrix.agr",
#                 xticklabelangle = 90,
#                 colorscheme='YlOrRd',
#                 reversecolorscheme = True,
#                 title="Transition Probabilities")

        



#########################
          
if __name__== "__main__":

    main()
         
##########################
