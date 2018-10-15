
#! /usr/bin/env python

"""
Created by Julia Poncela of January 2013

Get some statistics on time series cutting from the database:
average number of segments, type of segments, gaps,...



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
import operator
from PlotGrace import plot_matrix  # i use a function from the module
                                      # and just modify some of the default options

 
def main ():

    min_wi=20  #Filter1:  min number of weigh ins >=
  #  min_timespan=0       # Filter2: min length of the serie


    max_num_users_for_testing=2000   # this is just while i test the code!!
        


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



   
    query="""select * from users"""    
    result1 = db.query(query)  # is a list of dict.

    num_users=len(result1)

    dir="../Results/"
          


    list_diff_states=[]
    list_all_transitions=[]
    tot_num_transitions=0.
    num_useful_users=0

    cont_users=0        
    for r1 in result1:   #loop over users to get their number_of_weigh-ins
         ## r1 is a dict.:  {'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6', 'age': 52L, 'state': u'', 'height': 64L, 'join_date': datetime.datetime(2009, 11, 27, 10, 41, 5), 'is_staff': u'public', 'most_recent_weight': 142.0, 'initial_weight': 144.0, 'id': 1L}




   #   if cont_users <=max_num_users_for_testing:   #COMMENT THIS LINE FOR THE FINAL RUN!!!





        ck_id=r1['ck_id']
        id=r1['id']

        print cont_users,ck_id
        cont_users+=1
           

        

        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       
       
        r1['num_wi']=len(result2)  # i add another key-value to the dict. -->> with this i ALSO modify the list of dict. result!!!

       
        first=result2[0]['on_day']
        last=result2[-1]['on_day']
        time_span_days=(last-first).days+1
      

        if r1['num_wi']>=min_wi   :#and   int(time_span_days) >= min_timespan:                 
               
            dict_start_day_type_segment={}
                                           

            query3="select * from weigh_in_cuts  where (ck_id ='"+str(ck_id)+"') order by start_day"
            result3 = db.query(query3)  # is a list of dict.

                  

            for r3 in result3:  # each line is a dict, each line is a segment
                      
                fit_type=str(r3['fit_type'])
                state=fit_type

                start_day=int(r3['start_day'])
                stop_day=int(r3['stop_day'])
                start_weight=float(r3['start_weight'])
                stop_weight=float(r3['stop_weight'])
                
              
               
               
                if fit_type != "isolated":   # i get the dict states_startig days                   



                    param1=float(r3['param1'])
                    try:
                        param2=float(r3['param2'] )# cos  constant dont have a value for this
                    except: pass
                    
                    try:  # cos lin and constant dont have a value for this
                        param3=float(r3['param3'])
                    except: pass
                    


                    if fit_type == "exponent":                  
                        if param3 <0.: 
                            if param2 >0.:
                                state = fit_type+"_desc"
                                dict_start_day_type_segment[start_day]=state
                            else:
                                state = fit_type+"_asc"
                                dict_start_day_type_segment[start_day]=state
                        else:
                            print "we shouldnt have positive taus!", ck_id

                    elif fit_type == "linear":  
                        if param2 <0.:
                            state = fit_type+"_desc"
                            if param2 >-0.001:   # if very small slope, it is actually constant (this around 5% per two month)
                                state = "constant"
                            
                        else:
                            state = fit_type+"_asc"
                            if param2 <0.001:
                                state = "constant"

                        dict_start_day_type_segment[start_day]=state

                    else:   # constant
                        
                        dict_start_day_type_segment[start_day]=state
                       

                   

               
            if len(dict_start_day_type_segment)>0:    # user with at least one useful segment                           
                    num_useful_users+=1

                    query4="SELECT * FROM frequency_gaps where (ck_id ='"+str(ck_id)+"') order by start_day"   #gap info
                    result4 = db.query(query4)  # is a list of dict.                
                    
                    for r4 in result4:
                       
                        start_day=int(r4['start_day'])
                        stop_day=int(r4['stop_day'])
                        start_weight=float(r4['start_weight'])
                        stop_weight=float(r4['stop_weight'])
                                                
                        
                        dict_start_day_type_segment[start_day]="gap"
                       

                    list_tuples_sorted_dict = sorted(dict_start_day_type_segment.iteritems(), key=operator.itemgetter(0))  # the index of itermgetter is by which i order the list of tuples that was the dictionary
                    print  ck_id,

                   

                    ######### once i get all gaps, i merge consecutive gaps into just one:
                    print " states before merging gaps:", list_tuples_sorted_dict,len(list_tuples_sorted_dict)

                    flag_first_gap_index=0
                    list_items_to_remove=[]                  
                    for item in list_tuples_sorted_dict:       
                       # print item                 
                        if item[1]=='gap':   
                            if flag_first_gap_index==0:
                                flag_first_gap_index=1                                
                            else:
                                list_items_to_remove.append(item)
                                flag_first_gap_index=1                                


                        else:                          
                            flag_first_gap_index=0  #i dont want to remove the first gap right after a segment

                    
                    if   len(list_items_to_remove)>0:   # IT DIDT WORK TO REMOVE THEM AS I GO OVER THE LIST IN THE PREVIOS LOOP
                      #  print  "list items to remove:",list_items_to_remove
                        
                        for item in list_items_to_remove:
                            list_tuples_sorted_dict.remove(item)
 
                       # print "states after merging gaps:", list_tuples_sorted_dict,"\n"
                       # raw_input()





                    if len(list_tuples_sorted_dict) == 1: # if only one state --> diagonal term for the matrix
                        
                        state=list_tuples_sorted_dict[0][1] 
                        
                        if  state not in list_diff_states:  # for the transition matrix
                            list_diff_states.append(state)
                                                        
                        lista=[]
                        lista.append(state)
                        lista.append(state)
                        list_all_transitions.append(lista)
                        tot_num_transitions+=1.0
                        
               
                    else :    # if more than one trend 

                        cont=0   
                        for item in list_tuples_sorted_dict:                            
                            state=item[1]  
                            if  state not in list_diff_states:  # for the transition matrix
                                list_diff_states.append(state)                             
                                
                                
                                
                            if cont>0:                               
                                new_state=state
                                lista=[]
                                lista.append(old_state)
                                lista.append(new_state)
                                list_all_transitions.append(lista)
                                tot_num_transitions+=1.0
                                
                            old_state=state # i update for the next transition         
                            cont+=1



    ################# end loop over users



    list_diff_states=sorted(list_diff_states)    # this is the order of the trends for the transition matrix

    print "#num of diff states:", len(list_diff_states), "namely:",list_diff_states 

    print "#num useful users:", num_useful_users

    print "num transitions:",len(list_all_transitions)#,"  list transitions:",list_all_transitions ,"\n"  #ej.: [['exp_1.0_1.0_2.0', 'lin_3.0_1.0'], ['lin_3.0_1.0', 'lin_2.0_1.0'], ['exp_2.0_1.0_3.0', 'exp_2.0_2.0_1.0'], ...]


  
    matrix=[]     # raw count of transitions
    norm_matrix=[]  # normalized count of transitios by the tot number of them
    for i in range(len(list_diff_states)):
        matrix.append([0.000]*len(list_diff_states))   #ojo!!!!!!!!!!!!!!! si la creo: matrix.append(list), con list=[0.]*len(list_diff_states), al modificar unos elementos, modificare otros sin querer!!!!!!!!!!!!!!!!!!!
        norm_matrix.append([0.000]*len(list_diff_states))



 

    for  transition in list_all_transitions:
       # print "\n\n looking for:", transition[0],transition[1]
        for i in range(len(list_diff_states)):           
            old_state=list_diff_states[i]
            for j in range(len(list_diff_states)):
              
                new_state=list_diff_states[j]
                #print  old_state, new_state 
               
                if transition[0]== old_state  and transition[1]== new_state  :
                    matrix[i][j]+=1.000
                    norm_matrix[i][j]+=1.000
                  
                   


    for i in range(len(list_diff_states)):                     
        for j in range(len(list_diff_states)):
            norm_matrix[i][j]=norm_matrix[i][j]/tot_num_transitions



    file_name1=dir+"numerical_values_transiton_probability_matrix.dat" 
    file1=open(file_name1,'wt')

    for i in range(len(list_diff_states)):
        if "exp" in list_diff_states[i]:
            pass
            #print list_diff_states[i],"\t",
        else:
            pass#print list_diff_states[i],"\t\t",
        for j in range(len(list_diff_states)):            
           # print round(matrix[i][j]/tot_num_transitions,3),"             ",
            print >> file1,round(matrix[j][i]/tot_num_transitions,3),    # so the order row/columns matches with the .agr representation
            
       # print "\n"
        print >> file1,"\n"
    file1.close()
       
    print "printed out matrix textfile:",dir+"transiton_probability_matrix_test.dat" 







    #### PLOTGRACE IMPLEMENTATION ###     
    # Draw the matrix

    plot_matrix(matrix, dir+"transition_prob_matrix.agr",
                xticklabels = list_diff_states,
                yticklabels = list_diff_states,
                xticklabelangle = 90,
                colorscheme='YlOrRd',
                #logcolorbar=True,
                xlabel="Initial State", 
                ylabel="Final State",
                reversecolorscheme = False,                
                mincolor=(255,255,255),
                title="Transition Probabilities")   #########Axis for the matrix plot are X: initial state,   Y: final state.

    print "printed out matrix plot:",dir+"transition_prob_matrix.agr"




    plot_matrix(norm_matrix, dir+"transition_prob_matrix_norm.agr",
                xticklabels = list_diff_states,
                yticklabels = list_diff_states,
                xticklabelangle = 90,
                colorscheme='YlOrRd',
                #logcolorbar=True,
                xlabel="Initial State", 
                ylabel="Final State",
                reversecolorscheme = False,                
                mincolor=(255,255,255),
                title="Transition Probabilities")   #########Axis for the matrix plot are X: initial state,   Y: final state.

    print "printed out matrix plot:",dir+"transition_prob_matrix_norm.agr"





"""

Available keyword arguments for the plot_matrix function
    and their default values:

                force_square = False,
                boxes = None,
                boxstyle = 1,
                boxthickness = .2,
                boxcolor = 1,
                horizontal_borders = None,
                vertical_borders = None,
                colorscheme="PuOr",
                reversecolorscheme=False, 
                mincolor = None,
                maxcolor = None,
                special_value_colors = {},
                minmax=None,
                halfsize=None,
                xylimits=None,
                title="", subtitle="", colorbarlabel="",
                xlabel="", ylabel="",
                colorbarticksformat = None,
                colorbarticksprecision = None,
                logcolorbar=False,
                xlabelformatpattern = '%s',
                ylabelformatpattern = '%s',
                xticksformat = None,
                xticksprecision = None,
                yticksformat = None,
                yticksprecision = None,
                xticklabels = None,
                yticklabels = None,
                ticklabelcharsize = None,
                xticklabelangle = None,
                yticklabelangle = None,
                cutoff_high = None,
                cutoff_low = None,
                cutoff_to_symmetrical_colorbar = False,
                whitegraph = False
    
"""

   


#########################
          
if __name__== "__main__":
    main()
     

##############################################
