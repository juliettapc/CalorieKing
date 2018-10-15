
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


 
def main ():

    min_wi=20  #Filter1:  min number of weigh ins >=
    min_timespan=0       # Filter2: min length of the serie




    max_num_users_for_testing=1000   # this is just while i test the code!!
   
  
   



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



   
    query="""select * from users""" 

   
    result1 = db.query(query)  # is a list of dict.

    num_users=len(result1)

    dir="/home/staff/julia/at_Northwestern/calorieking/time_series/temporal_series/most_weigh_ins/"     #   to save the datafiles for the time series
        
        
      #  result4 = db.query(''' SELECT on_day, weight FROM weigh_in_history WHERE ck_id LIKE %s  ORDER BY on_day''', ck_id + '%')#THIS QUERY IS JUST TO TEST IT OUT!!
  # is a list of dict.


       



    list_num_segments_per_user=[]
    list_num_gaps_per_user=[]


    num_segments=0
    num_lin_segments=0
    num_const_segments=0
    num_exp_segments=0
    num_isolated=0
    num_gaps=0

    num_users_with_enough_wi=0
    num_users_with_valid_segments=0
    num_users_with_gaps=0

    list_lengths=[]
    list_lin_lengths=[]
    list_const_lengths=[]
    list_exp_lengths=[]

    list_gap_lengths=[]

   
    list_gap_alternation_values=[]
    list_seg_alternation_values=[]


    cont=0        
    for r1 in result1:   #loop over users to get their number_of_weigh-ins



 #     if cont <=max_num_users_for_testing:   #COMMENT THIS LINE FOR THE FINAL RUN!!!



        print cont
        cont+=1

     
        ## r1 is a dict.:  {'ck_id': u'bd84dbe2-dd6e-4125-b006-239442df2ff6', 'age': 52L, 'state': u'', 'height': 64L, 'join_date': datetime.datetime(2009, 11, 27, 10, 41, 5), 'is_staff': u'public', 'most_recent_weight': 142.0, 'initial_weight': 144.0, 'id': 1L}

        ck_id=r1['ck_id']
        id=r1['id']
        

        query2="select  * from weigh_in_history where (ck_id ='"+str(ck_id)+"')  order by on_day asc"
        result2 = db.query(query2)
       
       


        r1['num_wi']=len(result2)  # i add another key-value to the dict. -->> with this i ALSO modify the list of dict. result!!!

       
        first=result2[0]['on_day']
        last=result2[-1]['on_day']
        time_span_days=(last-first).days+1
      

        if r1['num_wi']>=min_wi   :#and   int(time_span_days) >= min_timespan:                 
               
            dict_start_day_type_segment={}
            segment_index_current_user=0

            num_users_with_enough_wi+=1
             
          




            output_file2=dir+"Time_series_user_id"+str(id)+".dat"
            file2 = open(output_file2,'wt')                                       
           
               
            for r2 in result2:
                weigh_in_day=r2['on_day']
                weight=float(r2['weight'])
                print >> file2, (weigh_in_day-first).days+1,weight
            file2.close()

            print "written file:",dir+"Time_series_user_id"+str(id)+".dat"


           
                   

            query3="select * from weigh_in_cuts  where (ck_id ='"+str(ck_id)+"') order by start_day"
            result3 = db.query(query3)  # is a list of dict.

          

        

            for r3 in result3:  # each line is a dict, each line is a segment
       

                segment_index_current_user+=1
                fit_type=str(r3['fit_type'])
                start_day=int(r3['start_day'])
                stop_day=int(r3['stop_day'])
                start_weight=float(r3['start_weight'])
                stop_weight=float(r3['stop_weight'])
                
          
               

                if fit_type != "isolated":      
                    dict_start_day_type_segment[start_day]=fit_type
                    list_lengths.append(stop_day-start_day+1)




                if fit_type == "isolated":      
                    num_isolated+=1

                elif fit_type == "linear":  
                    num_lin_segments+=1
                    list_lin_lengths.append(stop_day-start_day+1)

                elif fit_type == "constant":  
                    num_const_segments+=1
                    list_const_lengths.append(stop_day-start_day+1)
               
                elif fit_type == "exponent":  
                    num_exp_segments+=1
                    list_exp_lengths.append(stop_day-start_day+1)

             #   else:
              #      print "other fit type", ck_id, fit_type
               #     raw_input()



           
           
            if len(dict_start_day_type_segment)>0:    # user with at least one useful segment

                num_users_with_valid_segments+=1
                list_num_segments_per_user.append(len(dict_start_day_type_segment)) # excluding isolated  (not including gaps, either)
           

                query4="SELECT * FROM frequency_gaps where (ck_id ='"+str(ck_id)+"') order by start_day"   #gap info
                result4 = db.query(query4)  # is a list of dict.

                
                list_num_gaps_per_user.append(len(result4))
                num_gaps+=len(result4)
                num_users_with_gaps+=1
           
                for r4 in result4:
                    segment_index_current_user+=1
                    
                    start_day=int(r4['start_day'])
                    stop_day=int(r4['stop_day'])
                    start_weight=float(r4['start_weight'])
                    stop_weight=float(r4['stop_weight'])
                    
                    list_gap_lengths.append(stop_day-start_day+1)
                    
                    dict_start_day_type_segment[start_day]="gap"


                list_tuples_sorted_dict = sorted(dict_start_day_type_segment.iteritems(), key=operator.itemgetter(0))  # the index of itermgetter is by which i order the list of tuples that was the dictionary
                print  id,"  ",ck_id

                alternation_segs=[]
                alternation_gaps=[]
                i=0
                if len(list_tuples_sorted_dict)>1:  # if there is only one behavior, no alternation calculations
                    for item in list_tuples_sorted_dict:
             
                        print item[0], item[1]
                        type_segment=item[1]
                        if i >0:
                            if old_type_segment == type_segment:
                                if type_segment == "gap":
                                    alternation_gaps.append(0.)
                                else:
                                    alternation_segs.append(0.)
                            else:                       
                                alternation_gaps.append(1.)  

                      
                                alternation_segs.append(1.)
                        i+=1        
                        old_type_segment=type_segment

                    print "  average gap alternation:",numpy.mean(alternation_gaps)," number of cuts:",len(alternation_gaps)
                    print "  average segment alternation:",numpy.mean(alternation_segs)," number of cuts:",len(alternation_segs)

                    
                    if len(alternation_gaps)>0:
                        list_gap_alternation_values.append(numpy.mean(alternation_gaps))
                    else:
                        print "empty alternation gap list"
                       
                    if len(alternation_segs)>0:
                        list_seg_alternation_values.append(numpy.mean(alternation_segs))
                    else:
                        print "empty alternation segment list"
                       


                else:
                    print "      single segment user"
                print "# users with enough wi:",num_users_with_enough_wi, "  # users with valid segments: ",num_users_with_valid_segments
                print "\n"


#list_sorted_dict=[(u'Weiss', 5.0), (u'Wunderink', 5.0), (u'Keller', 4.0), (u'Go', 3.0), (u'Cuttica', 3.0), (u'Rosario', 2.0), (u'Radigan', 2.0), (u'Smith', 2.0), (u'RosenbergN', 2.0), (u'Gillespie', 1.0), (u'Osher', 1.0), (u'Mutlu', 1.0), (u'Dematte', 1.0), (u'Hawkins', 1.0), (u'Gates', 1.0)]
                
      


    filename4="../Results/More_summary_statistics_cutting_time_series.dat"
    file4=open(filename4,'wt')
    print >> file4, "\n\nSummary results cutting time series  (applying dynamics programing first for frequencies, and thento get the fits for the different trends):\n\n"
    
    print >> file4,"Total number of users:",num_users
    print >> file4,"    Number users with at least 20 weigh-ins:", num_users_with_enough_wi
    print >> file4,"         and with at least one valid segment:",num_users_with_valid_segments,"(all statistics on this dataset)\n"

    print >> file4,"Total number of segments:", sum(list_num_segments_per_user), ", of average length:",  numpy.mean(list_lengths),"days"
    print >> file4,"Average number of segments per individual:",numpy.mean(list_num_segments_per_user),"\n"

    print >> file4,"Number of one-point segments:",num_isolated
    print >> file4, "Number segments by type:"
    print >> file4, "    Linear: ",num_lin_segments, ", of average length:",  numpy.mean(list_lin_lengths ),"days"
    print >> file4, "    Constant: ",num_const_segments, ", of average length:",  numpy.mean(list_const_lengths ),"days"
    print >> file4, "    Exponential: ",num_exp_segments, ", of average length:",  numpy.mean(list_exp_lengths ),"days","\n"

    print >> file4, "Total number of gaps:",num_gaps
    print >> file4,"Average number of gaps per individual:",numpy.mean(list_num_gaps_per_user),', of average length:',numpy.mean(list_gap_lengths),"days (number of users with at least one gap:",num_users_with_gaps,")\n"

    print >> file4,"Average gap alternation:",numpy.mean(list_gap_alternation_values)
    print >> file4,"Average segment alternation:",numpy.mean(list_seg_alternation_values),"\n"

               
    file4.close()





    print "   printed out file: ",filename4


#########################
          
if __name__== "__main__":
   # if len(sys.argv) > 2:
       
        main()
#    else:
 #       print "usage: python whatever.py path/network_file1_R6s_info.gml  path/network_file2_kshell_info.gml "

   
    
     

##############################################
