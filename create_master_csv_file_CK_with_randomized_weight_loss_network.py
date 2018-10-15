#!/usr/bin/env python


'''
Code to read the CK master file with all info for the users, and randomized the value
of pwd at 4months and 6months for all networked users, and create Niter randome new values 

Created by Julia Poncela, on June 2014

'''


import numpy
import random






def main():
 




    Niter=100  # for the reshuffling of tht node identities




    ########### intput file
    filename0="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/data2009_2010/analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_p180_p120_within.txt"
    file0 = open(filename0,'r')
    list_lines_file=file0.readlines()
    
    ############
    

#  ck_id label_id weight_change_4months weight_change_6months pwc_4months pwc_6months num_wins_4months num_wins_6months num_activity_4months num_activity_6months initial_BMI gender age height paying_info join_date join_time time_in_system p_120 p_180 p_friends p_120_friends p_180_friends outcome20 act20 wi_20 num_friends avg_w_change_friends betweenness num_R6_friends k_shell_index max_clique_size role 


    dict_master_user_info={}
     
    list_ck_id=[] # so i preserve the order of the original master file (dictionaries dont have an ordering for the elements)
    list_networked_users=[]

    list_weights_4months_networked_people=[]
    list_weights_6months_networked_people=[]
    cont_lines=0
    for row in list_lines_file:

     if cont_lines >0:
        list_variables_one_row=row.split()        

        ck_id= list_variables_one_row[0]
        list_ck_id.append(ck_id)


        dict_master_user_info[ck_id]={}                      
        
        
        dict_master_user_info[ck_id]['label_id']= list_variables_one_row[1]
        dict_master_user_info[ck_id]['weight_change_4months']= list_variables_one_row[2]
        dict_master_user_info[ck_id]['weight_change_6months']= list_variables_one_row[3]
        dict_master_user_info[ck_id]['pwc_4months']= list_variables_one_row[4]
        dict_master_user_info[ck_id]['pwc_6months']= list_variables_one_row[5]
        dict_master_user_info[ck_id]['num_wins_4months']= list_variables_one_row[6]
        dict_master_user_info[ck_id]['num_wins_6months']= list_variables_one_row[7]
        dict_master_user_info[ck_id]['num_activity_4months']= list_variables_one_row[8]
        dict_master_user_info[ck_id]['num_activity_6months']= list_variables_one_row[9]
        dict_master_user_info[ck_id]['initial_BMI']= list_variables_one_row[10]
        dict_master_user_info[ck_id]['gender']= list_variables_one_row[11]
        dict_master_user_info[ck_id]['age']= list_variables_one_row[12]
        dict_master_user_info[ck_id]['height']= list_variables_one_row[13]
        dict_master_user_info[ck_id]['paying_info']= list_variables_one_row[14]
        dict_master_user_info[ck_id]['join_date']= list_variables_one_row[15]
        dict_master_user_info[ck_id]['join_time']= list_variables_one_row[16]
        dict_master_user_info[ck_id]['time_in_system']= list_variables_one_row[17]
        dict_master_user_info[ck_id]['p_120']= list_variables_one_row[18]
        dict_master_user_info[ck_id]['p_180']= list_variables_one_row[19]
        dict_master_user_info[ck_id]['p_friends']= list_variables_one_row[20]
        dict_master_user_info[ck_id]['p_120_friends']= list_variables_one_row[21]
        dict_master_user_info[ck_id]['p_180_friends']= list_variables_one_row[22]
        dict_master_user_info[ck_id]['outcome20']= list_variables_one_row[23]
        dict_master_user_info[ck_id]['act20']= list_variables_one_row[24]
        dict_master_user_info[ck_id]['wi_20']= list_variables_one_row[25]
        dict_master_user_info[ck_id]['num_friends']= list_variables_one_row[26]
        dict_master_user_info[ck_id]['avg_w_change_friends']= list_variables_one_row[27]
        dict_master_user_info[ck_id]['betweenness']= list_variables_one_row[28]
        dict_master_user_info[ck_id]['num_R6_friends']= list_variables_one_row[29]
        dict_master_user_info[ck_id]['k_shell_index']= list_variables_one_row[30]
        dict_master_user_info[ck_id]['max_clique_size']= list_variables_one_row[31]
        dict_master_user_info[ck_id]['role']= list_variables_one_row[32]
      
        #print  ck_id,dict_master_user_info[ck_id]['label_id'],  dict_master_user_info[ck_id]['weight_change_4months'], dict_master_user_info[ck_id]['weight_change_6months'],  dict_master_user_info[ck_id]['pwc_4months'],  dict_master_user_info[ck_id]['pwc_6months'], dict_master_user_info[ck_id]['num_wins_4months'], dict_master_user_info[ck_id]['num_wins_6months'],dict_master_user_info[ck_id]['num_activity_4months'],dict_master_user_info[ck_id]['num_activity_6months'],         dict_master_user_info[ck_id]['initial_BMI'],         dict_master_user_info[ck_id]['gender'],         dict_master_user_info[ck_id]['age'],        dict_master_user_info[ck_id]['height'],        dict_master_user_info[ck_id]['paying_info'],        dict_master_user_info[ck_id]['join_date'],        dict_master_user_info[ck_id]['join_time'],        dict_master_user_info[ck_id]['time_in_system'],        dict_master_user_info[ck_id]['p_120'],        dict_master_user_info[ck_id]['p_180'],        dict_master_user_info[ck_id]['p_friends'],        dict_master_user_info[ck_id]['p_120_friends'],        dict_master_user_info[ck_id]['p_180_friends'],        dict_master_user_info[ck_id]['outcome20'],        dict_master_user_info[ck_id]['act20'],        dict_master_user_info[ck_id]['wi_20'],        dict_master_user_info[ck_id]['num_friends'],        dict_master_user_info[ck_id]['avg_w_change_friends'],        dict_master_user_info[ck_id]['betweenness'],        dict_master_user_info[ck_id]['num_R6_friends'],        dict_master_user_info[ck_id]['k_shell_index'],        dict_master_user_info[ck_id]['max_clique_size'],        dict_master_user_info[ck_id]['role']

        try:
            if int(dict_master_user_info[ck_id]['num_friends']) >0:
                list_weights_4months_networked_people.append(float(dict_master_user_info[ck_id]['pwc_4months']))
                list_weights_6months_networked_people.append(float(dict_master_user_info[ck_id]['pwc_6months']))

                list_networked_users.append(ck_id)
        except ValueError:
            pass
   
        
     cont_lines +=1

    print len(list_weights_4months_networked_people), numpy.mean(list_weights_4months_networked_people), numpy.mean(list_weights_6months_networked_people)
 
    file0.close()






    ####### output master files  with weigh change randomized among networked people
    csv_file_rand="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/data2009_2010/analysis_time_bins_bmi_groups/master_files_randomized_weight_network/master_users_file_weight_change_first6months_p180_p120_within_randomized_weight_network_people.txt"
    file1 = open(csv_file_rand,'wt')
    print >> file1, "ck_id label_id weight_change_4months weight_change_6months pwc_4months pwc_6months num_wins_4months num_wins_6months num_activity_4months num_activity_6months initial_BMI gender age height paying_info join_date join_time time_in_system p_120 p_180 p_friends p_120_friends p_180_friends outcome20 act20 wi_20 num_friends avg_w_change_friends betweenness num_R6_friends k_shell_index max_clique_size role ",
    
    for i in range(Niter):
        print >> file1, "pwc_4months_randomized"+str(i),
    for i in range(Niter):
        print >> file1, "pwc_6months_randomized"+str(i),

    print >> file1, ""
    #########



  


    list_lists_randomized_values_pwc_4months=[]
    list_lists_randomized_values_pwc_6months=[]
    for i in range(Niter):
        new_list_randomized_pwc_4months=random.sample(list_weights_4months_networked_people,len(list_weights_4months_networked_people))  # create a randomized versions 
        new_list_randomized_pwc_6months=random.sample(list_weights_6months_networked_people,len(list_weights_6months_networked_people))  # (sample without replacement)

        list_lists_randomized_values_pwc_4months.append(new_list_randomized_pwc_4months)
        list_lists_randomized_values_pwc_6months.append(new_list_randomized_pwc_6months)



  
    cont_networked_users=0
    ############### i print out the final data file
    for index in range(len(list_ck_id)):  # loop over all users
        ck_id=list_ck_id[index]
                 
        print >> file1,ck_id,dict_master_user_info[ck_id]['label_id'], dict_master_user_info[ck_id]['weight_change_4months'], dict_master_user_info[ck_id]['weight_change_6months'],  dict_master_user_info[ck_id]['pwc_4months'],  dict_master_user_info[ck_id]['pwc_6months'], dict_master_user_info[ck_id]['num_wins_4months'], dict_master_user_info[ck_id]['num_wins_6months'],dict_master_user_info[ck_id]['num_activity_4months'],dict_master_user_info[ck_id]['num_activity_6months'],dict_master_user_info[ck_id]['initial_BMI'],dict_master_user_info[ck_id]['gender'],dict_master_user_info[ck_id]['age'],dict_master_user_info[ck_id]['height'],dict_master_user_info[ck_id]['paying_info'],dict_master_user_info[ck_id]['join_date'],dict_master_user_info[ck_id]['join_time'],dict_master_user_info[ck_id]['time_in_system'],dict_master_user_info[ck_id]['p_120'],dict_master_user_info[ck_id]['p_180'],dict_master_user_info[ck_id]['p_friends'],dict_master_user_info[ck_id]['p_120_friends'],dict_master_user_info[ck_id]['p_180_friends'],dict_master_user_info[ck_id]['outcome20'],dict_master_user_info[ck_id]['act20'],dict_master_user_info[ck_id]['wi_20'],dict_master_user_info[ck_id]['num_friends'],dict_master_user_info[ck_id]['avg_w_change_friends'],dict_master_user_info[ck_id]['betweenness'],dict_master_user_info[ck_id]['num_R6_friends'],dict_master_user_info[ck_id]['k_shell_index'],dict_master_user_info[ck_id]['max_clique_size'],dict_master_user_info[ck_id]['role'],
       
        if ck_id in list_networked_users:
     
            for i in range(Niter):
                print index, i,cont_networked_users
                print >> file1,list_lists_randomized_values_pwc_4months[i][cont_networked_users],
                print >> file1,list_lists_randomized_values_pwc_6months[i][cont_networked_users],
                
            cont_networked_users +=1


        else:
            for i in range(Niter):
                print  index, i,cont_networked_users
                print >> file1,dict_master_user_info[ck_id]['weight_change_4months'],   # for non-network people, there is no randomization
                print >> file1,dict_master_user_info[ck_id]['weight_change_6months'],
                
           

        print >> file1,""
       

    print "\n printed file:", csv_file_rand
    

        



##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename_network1 = sys.argv[1]
    #    filename_network_for_kshell = sys.argv[2]
   
     #   main(filename_network1,filename_network_for_kshell)
    #else:
     #   print "Usage: python script.py path/filename.gml  path/filename_for_kshell.gml"

    
    main()
