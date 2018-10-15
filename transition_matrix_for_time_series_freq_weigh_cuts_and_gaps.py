#! /usr/bin/env python

"""
Created by Julia Poncela on March 2012

It queries the DB for the info about diff. behaviors in the time series, in terms of trend, frequency and gaps, and it calculates the transition probability matrix from every state to every state, by counting the number of times each transition occurs accros all time series.


"""


import sys
import os
from datetime import *
from database import *   #codigo para manejar bases de datos
import math
import numpy
from scipy import stats



def main ():

  

    max_coef_exp=1000
    max_coef_slope=5   # +- that %pwc in one day!!


    tot_num_transitions=0   # across all users
    list_diff_states=[]     # for the transition matrix
    list_all_transitions=[] # for the transition matrix
   
  

    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 



    query="""select * from users""" 
    result1 = db.query(query)  # is a list of dictionaries



    contador_time_series=0
    contador=0
   
    for r1 in result1:   #loop over users
        contador+=1
       
        ck_id=r1['ck_id']
       

        

        list_start_end_dates_one_user=[] #without considering the gaps

        list_states_one_user=[]   #without considering the gaps (just diff. behaviors)
       

        dicc_states_one_user={} # the key is the initial_day, the value is the type of trend  or gap
        temp_dicc_states={}

        try:  #only for the users with an entry in that time_series related table: one of the (filtered) time series

             ######################################
             # for the info about different trends# (for a given, fixed user)
             ######################################

            contador_time_series+=1
            print "\n\n\n",contador, ck_id



            query2="select  * from weigh_in_cuts where (ck_id ='"+str(ck_id)+"')  order by start_day asc"
            result2 = db.query(query2)
        

             #result2: [{'fit_type': u'exp', 'stop_idx': 4L, 'ck_id': u'a48eba6e-51ad-42bc-b367-a24bb6504f0a', 'id': 68008L, 'cost': 0.5, 'param3': -0.60660499999999995, 'param2': 3.4280400000000002, 'param1': -3.1829299999999998, 'start_idx': 0L}, {'fit_type': u'lin', 'stop_idx': 16L, 'ck_id': u'a48eba6e-51ad-42bc-b367-a24bb6504f0a', 'id': 68007L, 'cost': 0.5, 'param3': None, 'param2': 0.015299699999999999, 'param1': -4.1967499999999998, 'start_idx': 5L}]


            num_trends=len(result2)

           
              
            for r2 in result2: 

                start_stop_days=[]   # for that particular segment

                starting_day=int(r2['start_day'])
                ending_day=int(r2['stop_day'])                 
                trend=r2['fit_type']
                param1=r2['param1']
                param2=r2['param2']
                param3=r2['param3']



                start_stop_days.append(starting_day)
                start_stop_days.append(ending_day)

               
                list_start_end_dates_one_user.append(start_stop_days)

              


                if trend == "exp":                                  
                    #i dont really care about the interception
                    coef1_exp=param1
                    coef2_exp=param2
                    coef3_exp=param3       ################################
                                           # lin: intersection + X*slope  #
                                           #exponential: A+B*exp(lambda*t)#
                                           ################################
                    
                    
                    if coef1_exp <= max_coef_exp and coef1_exp >= -max_coef_exp :   # to avoid weird fits
                        if coef2_exp <= max_coef_exp and coef2_exp >= -max_coef_exp : 
                            if coef3_exp <= max_coef_exp and coef3_exp >= -max_coef_exp : 


                                if coef2_exp <0  and coef3_exp >0:   # i only care about exp increase/decrease
                                    state="exp_down"
                                elif coef2_exp >0  and coef3_exp <0:   
                                    state="exp_down"
                                elif coef2_exp >0  and coef3_exp >0:   
                                    state="exp_up"
                                elif coef2_exp <0  and coef3_exp <0:   
                                    state="exp_up"

                               # elif coef2_exp==0.0 or coef2_exp== -0.0:
                                #    state="flat"
                                else:
                                    print ck_id, coef2_exp, coef3_exp,"not one of the two exp types"
                                    raw_input()
    


                                
                               
                    else:          
                        print "values for the fit coef. too weird!", param1,param2,param3, ck_id
            
                elif trend == "lin":                    
                                     # i dont really care about the interception
                    coef2_lin=param2
                    

                   
                    if coef2_lin <= max_coef_slope and coef2_lin >= -max_coef_slope :   # to avoid weird fits
                        
                        if coef2_lin <0:   # i only care about linear increase/decrease
                            state="lin_down" 

                            if coef2_lin >  -0.0001:
                                state="flat"

                        elif coef2_lin==0.0:
                            state="flat"
                        else:                                
                            state="lin_up"
                            if coef2_lin < 0.0001:
                                state="flat"
                             
               

                list_states_one_user.append(state)
                temp_dicc_states[starting_day]=state   # i save the pair starting_day, trend for that user 
                if state not in list_diff_states: 
                    list_diff_states.append(state)
                        
                   

            ####################### end loop over result2  (info diff trends)


        except MySQLdb.Error: pass     #for the users without an entry in that time_series related table: not one of the (filtered) time series







          ##########################
          # for the gap info       # (for the same given, fixed user  ck_id)
          ##########################

           
        query3="select  * from gaps_by_frequency where (ck_id ='"+str(ck_id)+"')  order by start_day asc"
        result3 = db.query(query3)
        
             #result3: [{'file_index': 1408, 'ck_id': 8647c765-e37e-4024-92da-be838b792379, 'start_date':2009-05-07 00:00:00, 'end_date':2009-06-08 00:00:00, 'start_day': 108, 'end_day': 140, 'days_gap': 32, 'zscore_gap': 3.83125},{'file_index': 1408, 'ck_id': 8647c765-e37e-4024-92da-be838b792379, 'start_date':2009-08-04 00:00:00, 'end_date':2009-09-30 00:00:00, 'start_day': 197, 'end_day': 254, 'days_gap': 57, 'zscore_gap': 7.1496} ]


        num_gaps=len(result3)

       


        if num_gaps>0:
               
               

                for r3 in result3: 
                    
                    file_index=r3['file_index']

                    starting_gap=int(r3['start_day'])
                    ending_gap=int(r3['end_day'])                      
                    trend="gap"                    
                    zscore_gap=r3['zscore_gap']    # threshold to consider a gap statistically sifnificant  zs>=3  (imposed like that in: analyze_frequency_gaps_in_time_series_frequencies_EDIT_DB.py)



                    if trend not in list_diff_states: 
                        list_diff_states.append(trend)
                
                    cont=-1  #to go over list_states_one_user
                    for segment in list_start_end_dates_one_user:   #  the list is sorted chronologically
                        cont+=1

                        start_behavior=segment[0]
                        end_behavior=segment[1]

                        if (starting_gap <= end_behavior)  and (ending_gap >= start_behavior):  # if there is a gap
                                                                                                # in the middle of a behavior
                            num_trends+=2
                               ## i cut the trend in two segments, with a gap in between
                            new_segment1=[start_behavior,starting_gap]
                            new_segment2=[starting_gap,ending_gap]
                            new_segment3=[ending_gap,end_behavior]




                            temp_dicc_states[start_behavior]=list_states_one_user[cont]
                            temp_dicc_states[starting_gap]=trend
                            temp_dicc_states[ending_gap]=list_states_one_user[cont]
 
                            
                            #print "gap cutting in the middle of a single behavior:",new_segment1,new_segment2,new_segment3, ck_id
                            


                  


                    for i in range(len(list_start_end_dates_one_user)):    # i check whether there is a gap in between DIFF behaviors
                        try:                          

                            old_ending=list_start_end_dates_one_user[i][1]
                            new_beginnig=list_start_end_dates_one_user[i+1][0]


                            if (starting_gap >= old_ending)  and (ending_gap <= new_beginnig):
                             
                               # print "gap in the middle of two diff. behaviors:",list_states_one_user[i],trend,list_states_one_user[i+1]
                               


                                temp_dicc_states[starting_gap]=trend
                                temp_dicc_states[ending_gap]=list_states_one_user[i+1]

                              


                        except IndexError: pass
                            #print "no room for any more gaps,",len(list_start_end_dates_one_user),i






                    # create a final list of all states, and then go for state in list_states: and copy code from aux, line 70 on






                    

        
                # end loop over result3   (gap info)



        else:  #if the gap info doesnt change the number of trends (NO gaps)
            pass
               


        for key in temp_dicc_states.keys():   # i make a copy of the dicc, to be the final one
            dicc_states_one_user[key]=temp_dicc_states[key]
           
       


# i account for all possible states and transsitions between states:
       
        if len(dicc_states_one_user)>1:   # several trends for the time series

            cont=0
            for  key in sorted(dicc_states_one_user.keys()):  # i print out the result of combining weigh_in cuts and gaps:
                print key,dicc_states_one_user[key] 
                state=dicc_states_one_user[key] 
                if state not in list_diff_states:
                    list_diff_states.append(state)


                list=[]
                if cont==0: # for the first state
                    state1=dicc_states_one_user[key] 
                else:  # for all the rest of states in the sorted dictionary
                    state2=dicc_states_one_user[key] 
                    list.append(state1)
                    list.append(state2)
                    list_all_transitions.append(list)
                    
                    state1=state2
                cont+=1


        elif len(dicc_states_one_user)==1:    # one single trend for the time series
            list=[]
            for key in dicc_states_one_user:
                list.append(dicc_states_one_user[key])
                list.append(dicc_states_one_user[key])
                print key,dicc_states_one_user[key] 
                if state not in list_diff_states:
                    list_diff_states.append(state)

            list_all_transitions.append(list)

        #print  list_all_transitions  

#       if num_gaps>0:                               
  #          raw_input()

      
         

     ################################# end loop over result1  (loop over users)  






#  i   create the empty transition matrix

    list_diff_states=sorted(list_diff_states)    # this is the order of the trends for the transition matrix

    matrix=[]
    for i in range(len(list_diff_states)):
        matrix.append([0.000]*len(list_diff_states))   #ojo!!!!!!!!!!!!!!! si la creo: matrix.append(list), con list=[0.]*len(list_diff_states), al modificar unos elementos, modificare otros sin querer!!!!!!!!!!!!!!!!!!!





    print "num transitions:",len(list_all_transitions), "diff. states:",list_diff_states

    
    for  transition in list_all_transitions:      
        for i in range(len(list_diff_states)):           
            old_state=list_diff_states[i]
            for j in range(len(list_diff_states)):
              
                new_state=list_diff_states[j]                
               
                if transition[0]== old_state  and transition[1]== new_state  :
                    matrix[i][j]+=1.000
                   



    file_name1="temporal_series/transiton_probability_matrix_test_with_gap_info.dat" 
    file1=open(file_name1,'wt')

    for i in range(len(list_diff_states)):       
        for j in range(len(list_diff_states)):                      
            print >> file1,round(matrix[i][j]/float(len(list_all_transitions)),3),
                  
        print >> file1,"\n"
    file1.close()



    #### PLOTGRACE IMPLEMENTATION ###
    # Draw the matrix


    from PlotGrace import plot_matrix  # i use a function from the module
                                      # and just modify some of the default options

    plot_matrix(matrix,"temporal_series/transition_prob_matrix_with_gaps.agr",
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
