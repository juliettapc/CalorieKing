#! /usr/bin/env python

import csv
import networkx as nx
import numpy
import sys
import operator
from scipy import stats
import ols   # script to do multi variable linear regressions
from database import *   #package to handle databases
import pickle
import matplotlib.pyplot as plt



def main():




    weigh_ins=2   #filter
    group_study_BMI_over=25   # the users i study have at least this bmi
    bmi_group=1   # the obese and overweight are separated into 10 bmi groups
    


    coeff2_filename="./analysis_time_bins_bmi_groups/coeff_model2_group"+str(bmi_group)+".dat"
    file_coeff2=open(coeff2_filename, 'wt')  

    coeff3_filename="./analysis_time_bins_bmi_groups/coeff_model3_group"+str(bmi_group)+".dat"
    file_coeff3=open(coeff3_filename, 'wt')  



    ymin=-25   # ranges for the figure
    ymax=20

    xmin=3 
    xmax=37



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 



    create_dict_weigh_in_history="NO"   # if YES, i create a pickle for the weight history of all users, if NO, i just read and existing one.


    pickle_name="./save_dict_users_weight_history.p"



    if create_dict_weigh_in_history=="YES":####### I access the DB to get the weigh_in history of all users, and put the info in a dict in a pickle
  #(only the first time, then i just read that pickle)

        print "\nGenerating the weigh_in history dictionary for all users..."

        query1="""select * from users"""    
        result1 = db.query(query1)  # is a list of dict.       
       
        dict_all_users_weight_history={}
        cont=0
        for r1 in result1:            
                       
            ck_id=r1['ck_id']
            
            print cont
            query2="select  * from weigh_in_history where ck_id ='"+str(ck_id)+"' order by on_day asc"
            result2= db.query(query2)   
            
            
            dict_individual_weight_history={}
            for r2 in result2:
                weigh_in_day=r2['on_day']
                weight=r2['weight']
                
                delta_days=int((weigh_in_day-result2[0]['on_day']).days)
                dict_individual_weight_history[delta_days]=weight
                    
        
            dict_all_users_weight_history[ck_id]=dict_individual_weight_history
            cont+=1


        
        pickle.dump(dict_all_users_weight_history, open(pickle_name, 'wb'))
        print "written pickle:", pickle_name
       

    else:

        dict_all_users_weight_history=pickle.load(open(pickle_name, 'rb'))




    name_model1="./analysis_time_bins_bmi_groups/model1_weight_change_vs_t_group"+str(bmi_group)+".txt"
    file1_model=open(name_model1, 'wt')  

    name_model2="./analysis_time_bins_bmi_groups/model2_weight_change_and_wins_vs_t_group"+str(bmi_group)+".txt"
    file2_model=open(name_model2, 'wt')  

    name_model3="./analysis_time_bins_bmi_groups/model3_weight_change_and_wins_and_R6s_vs_t_group"+str(bmi_group)+".txt"
    file3_model=open(name_model3, 'wt')  




 


    name1="./network_all_users/master_csv_gender_pay_info.csv"       
    original_file= csv.reader(open(name1, 'rb'), delimiter=' ')#, quotechar='|')

   
    dict_dict_master={}

    cont1=0
    for row in original_file:
       
        if cont1>0:     # exclude the headers      
          
            label=row[1]
            dict_one_user={}

#  id ck_id join_date initial_weight most_recent_weight height age weighins initial_bmi final_bmi percentage_weight_change weight_change time_in_system outcome20 outcome50 p_50 act_20 wi_20 p_friend R6_overlap degree friend_avg activity gender paying_info

            dict_one_user['id']=int(row[0])
            dict_one_user['ck_id']=str(row[1])

            dict_one_user['join_date']=row[2]
            dict_one_user['join_time']=row[3]# ojoooooo! lo guarde solo separado con espacios!!!   

            dict_one_user['initial_weight']=float(row[4])
            dict_one_user['most_recent_weight']=float(row[5])
            dict_one_user['height']=float(row[6])
            dict_one_user['age']=float(row[7])
            dict_one_user['weighins']=float(row[8])
            dict_one_user['initial_bmi']=float(row[9])
            dict_one_user['final_bmi']=float(row[10])
            dict_one_user['percentage_weight_change']=float(row[11])
            dict_one_user['weight_change']=float(row[12])
            dict_one_user['time_in_system']=float(row[13])
            try:
                dict_one_user['outcome20']=float(row[14])
            except ValueError:
                dict_one_user['outcome20']=row[14]

            try:
                    dict_one_user['outcome50']=float(row[15])
            except ValueError:
                dict_one_user['outcome50']=row[15]

            dict_one_user['p_50']=float(row[16])
            dict_one_user['act_20']=float(row[17])
            dict_one_user['wi_20']=float(row[18])
            dict_one_user['p_friend']=float(row[19])
            dict_one_user['R6_overlap']=float(row[20])           
            dict_one_user['degree']=float(row[21])
            dict_one_user['friend_avg']=float(row[22])
            dict_one_user['activity']=float(row[23])            
            dict_one_user['gender']=row[24]                        
            dict_one_user['paying_info']=row[25]
                 
           

            dict_dict_master[label]=dict_one_user
        cont1+=1




        
    dic_users_2wins={}    ######### i create a dictionary only for those users with wins>=2
    for clave in  dict_dict_master:             
        if dict_dict_master[clave]['weighins']>=weigh_ins:          
            dic_users_2wins[clave]=dict_dict_master[clave]
        


    dic_users_2wins_BMI_over25={}   ######## and then i select only the obese & overweight
    for clave in  dic_users_2wins:             
        if dic_users_2wins[clave]['initial_bmi']>=group_study_BMI_over:    
            dic_users_2wins_BMI_over25[clave]=dic_users_2wins[clave]




    ######## i sort obese and overweight users by i_bmi
    list_sorted_dict_users_2wins_BMI_over25=sorted(dic_users_2wins_BMI_over25.items(),key=lambda x: x[1]['initial_bmi'])#,reverse=True)

   # for item in list_sorted_dict_users_2wins_BMI_over25:   #just to double check
    #   print item[1]['ck_id'],item[1]['initial_bmi']
   

    print "\n\nTotal # users:",len(dict_dict_master),"\nUsers with weigh_ins >=2:", len(dic_users_2wins),"\nUsers with weigh_ins >=2 and BMI>=25:", len(dic_users_2wins_BMI_over25)




    ##### ###### i create 10 groups of sorted users according to i_bmi
    size_dict=float(len(dic_users_2wins_BMI_over25))

    ten_percent_users=size_dict/10.+1
    first_user_of_group_index=int(ten_percent_users)-1

    first_user_of_group_index=0   
    print "\nGroup first_user_index i_bmi:"
    for i in range(10):        
        print i+1, "    ",first_user_of_group_index, "    ",list_sorted_dict_users_2wins_BMI_over25[first_user_of_group_index][1]['initial_bmi']
        
        if bmi_group == i+1:
            first_i_bmi = list_sorted_dict_users_2wins_BMI_over25[first_user_of_group_index][1]['initial_bmi']

            if bmi_group < 10:
                last_i_bmi = list_sorted_dict_users_2wins_BMI_over25[first_user_of_group_index+int(ten_percent_users)][1]['initial_bmi']
            else:
                last_i_bmi = list_sorted_dict_users_2wins_BMI_over25[-1][1]['initial_bmi']


        first_user_of_group_index+=int(ten_percent_users)


    print first_i_bmi,last_i_bmi

#Group user_index i_bmi:
#1      0      25.006404321
#2      2259      26.3912824389
#3      4518      27.6311413454
#4      6777      28.9719313878
#5      9036      30.3406795225
#6      11295      31.7931588613
#7      13554      33.4695496925
#8      15813      35.5050505051
#9      18072      38.2584844277
#10      20331      42.4295857988



    print   "\ni pick bmi group:",bmi_group,"i_bmi from:",first_i_bmi,"to:",last_i_bmi,"\n"


    if bmi_group==1:
        initial_index=0
        final_index=2259

    elif bmi_group==2:
        initial_index=2259
        final_index=4518

    elif bmi_group==3:
        initial_index=4518
        final_index=6777

    elif bmi_group==4:
        initial_index=6777
        final_index=9036

    elif bmi_group==5:
        initial_index=9036
        final_index=11295

    elif bmi_group==6:
        initial_index=11295
        final_index=13554

    elif bmi_group==7:
        initial_index=13554
        final_index=15813

    elif bmi_group==8:
        initial_index=15813
        final_index=18072

    elif bmi_group==9:
        initial_index=18072
        final_index=20331

    elif bmi_group==10:
        initial_index=20331
        final_index=22586   #final number of users 22586
    else:
        print "wrong bmi group"
        exit()



    ############### i create a dict with all the info about the users from the selected group
    dict_users_2wins_BMI_over25_group_selected={}
    for i in range(initial_index,final_index):   
        label=list_sorted_dict_users_2wins_BMI_over25[i][0]
        if len(label)==0:
            raw_input()
        dict_users_2wins_BMI_over25_group_selected[label]=list_sorted_dict_users_2wins_BMI_over25[i][1]
       
      
    num_users_group=len(dict_users_2wins_BMI_over25_group_selected)

    ################ i create the time bins
    list_time_bins=[5,10,20,40,80,160,320]
    dict_dict_users_time_bins={}
    for item in list_time_bins:
        dict_dict_users_time_bins[item]={}  # for each bin i will have a dict with all users in it

   
    max_time_system=0.

    for clave  in dict_users_2wins_BMI_over25_group_selected:   ########### i create a dictionary of dictionaries for each time bin
        time_system=dict_users_2wins_BMI_over25_group_selected[clave]['time_in_system']

        for item in list_time_bins:
            if time_system >= item:
                dict_dict_users_time_bins[item][clave]=dict_users_2wins_BMI_over25_group_selected[clave]


        if time_system>=max_time_system:
            max_time_system=time_system

    print "\n\nmax time in the system for bmi group",bmi_group, "is:",max_time_system,"days"

   

    sorted_dict_dict_users_time_bins = sorted(dict_dict_users_time_bins.iteritems(), key=operator.itemgetter(0))#, reverse=True)   # the index in itemgetter is to sort 0: by key, 1: by value

  #  for element in sorted_dict_dict_users_time_bins:
   #     print element[0],len(element[1])
    #    for e in element[1]:
     #       print e,dict_dict_master[e]['time_in_system']

      #  raw_input()

    ############### i get the points for each bin and for each model    
    x_positions=[]   # the position of the time bins
    list_lists_ypositions_model1=[]   # the points in each bin (for the three models)
    list_lists_ypositions_model2=[]
    list_lists_ypositions_model3=[]
 
    for time_bin_set  in sorted_dict_dict_users_time_bins:  # loop over time bins  (sorted).  sorted_dict_dict_users_time_binsis a list of tuples: time_bin, dict_users_in_that_bin
      # if time_bin_set[0]<45: #  this is just to test individually the diff bins

        list_ypositions_model1=[]
        list_ypositions_model2=[]
        list_ypositions_model3=[]

        x_positions.append(time_bin_set[0])  # for the boxplot

        print "time bin:",time_bin_set[0]

        list_weight_changes=[]
        list_num_weighins=[]       
        list_num_R6s=[]
        list_of_lists_pairs_num_weighins_and_R6s=[]
                                        
        for user_key in time_bin_set[1]:    #    loop over users in that time bin    time_bin_set[1]    is a dict of dictionaries, including all users present in that bin
            
            list_sorted_weight_in_history_user = sorted(dict_all_users_weight_history[user_key].iteritems(), key=operator.itemgetter(0))     # the index in itemgetter is para ordenar por 0:key o 1:value

         
            initial_weight=list_sorted_weight_in_history_user[0][1]  # the very first value of the whole time series
            final_weight=list_sorted_weight_in_history_user[0][1]   # WITHIN the time bin
                    

            num_weigh_ins=0
            for pair in list_sorted_weight_in_history_user:   # each pair is: day_index, weight

                if pair[0]<=time_bin_set[0]:
                    num_weigh_ins+=1
                    final_weight=pair[1]
                               

            percentage_weight_change=(final_weight-initial_weight)/initial_weight*100.  

           
           # print user_key, "# w-ins in the bin:",num_weigh_ins, "   initial weight:",initial_weight, "   final weight:",final_weight, "   pwc:",percentage_weight_change, "   tot number w-ins:",len(list_sorted_weight_in_history_user)
            

                  
            list_weight_changes.append(percentage_weight_change) # for model2
            list_num_weighins.append(num_weigh_ins)


            num_R6s=time_bin_set[1][user_key]['R6_overlap']  # for model3          
            list_num_R6s.append(num_R6s)


            list_values_user=[]   

            list_values_user.append(num_weigh_ins)  
            list_values_user.append(num_R6s)
            list_of_lists_pairs_num_weighins_and_R6s.append(list_values_user)  #because the array is defined like [[x1, x2, x3],[x1, x2, x3],[x1, x2, x3],...]
       

        #########For Model1:  % weight change vs time bin
        print "\n\nModel1"
        print >> file1_model, time_bin_set[0],numpy.mean(list_weight_changes), numpy.std(list_weight_changes),len(time_bin_set[1])
       
        print  "time_bin   avg_weight_change  SD  #users_in_it\n"
        print time_bin_set[0],numpy.mean(list_weight_changes), numpy.std(list_weight_changes),len(time_bin_set[1])
        


        #########For Model2:  % weight change and w-ins vs time bin
        print "\n\nModel2"
        print "summary of the multivariable linear regression for bin t<=",time_bin_set[0]#, mymodel2.summary()  
        file2_model=open(name_model2, 'at')  
        print >> file2_model, "\n\nsummary of the multivariable linear regression for bin t<=",time_bin_set[0]  
        file2_model.close()

           
        x_model2=numpy.array(list_num_weighins)
        y_model2=numpy.array(list_weight_changes)
       

        mymodel2 = ols.ols(y_model2,x_model2,'%weight_change',['#w_ins'])        
        names, coeff, sd, tstat, pvalue=mymodel2.summary_to_file(name_model2)
        print "coeff etc from the results (model2):",names, coeff, sd, tstat, pvalue

        constant2=coeff[0]       
        alpha2=coeff[1]

        sd_constant2=sd[0]
        sd_alpha2=sd[1]
          
        print >> file_coeff2, time_bin_set[0],constant2,sd_constant2,alpha2,sd_alpha2

        #########For Model3:  % weight change, w-ins and #R6s vs time bin
        print "\n\nModel3"
        print "summary of the multivariable linear regression for bin t<=",time_bin_set[0]#, mymodel3.summary()  
        file3_model=open(name_model3, 'at')  
        print >> file3_model, "\n\nsummary of the multivariable linear regression for bin t<=",time_bin_set[0]  
        file3_model.close()



        y_model3=numpy.array(list_weight_changes)       
        x_model3=numpy.array(list_of_lists_pairs_num_weighins_and_R6s)

        print len(x_model3),len(y_model3),len(y_model2),len(list_weight_changes)  # number of users in that bin 

        mymodel3 = ols.ols(y_model3,x_model3,'%weight_change',['#w_ins','#R6s'])        
        names, coeff, sd, tstat, pvalue=mymodel3.summary_to_file(name_model3)
        print "coeff etc from the results (model3):",names, coeff, sd, tstat, pvalue

        constant3=coeff[0]
        alpha3=coeff[1]
        beta3=coeff[2]

        sd_constant3=sd[0]
        sd_alpha3=sd[1]
        sd_beta3=sd[2]


        print >> file_coeff3, time_bin_set[0],constant3,sd_constant3,alpha3,sd_alpha3,beta3,sd_beta3
         

        for i in range(len(list_weight_changes)):

            list_ypositions_model1.append(list_weight_changes[i])            
            list_ypositions_model2.append(list_weight_changes[i]-alpha2*list_num_weighins[i]-constant2)
            list_ypositions_model3.append(list_weight_changes[i]-alpha3*list_num_weighins[i]-beta3*list_num_R6s[i]-constant3)



        list_lists_ypositions_model1.append(list_ypositions_model1)
        list_lists_ypositions_model2.append(list_ypositions_model2)
        list_lists_ypositions_model3.append(list_ypositions_model3)
      
# try to print : mymodel2.t, mymodel2.se etc from:  self.x_varnm, self.b, self.se, self.t, self.p



  #  print numpy.mean(list_lists_ypositions_model1[1]), numpy.mean(list_lists_ypositions_model2[1]), numpy.mean(list_lists_ypositions_model3[1])  # average value for a particular bin and the three models


        
    file1_model.close()    # files with summary of the regressions
    file2_model.close()
    file3_model.close()


    print "\n\nwritten summary file:",name_model1
    print "written summary file:",name_model2
    print "written summary file:",name_model3

   
  #  x_positions1=[3,8,18,38,78,158,318]
   # x_positions2=[5,10,20,40,80,160,320]
    #x_positions3=[7,12,22,42,82,162,322]

    x_positions1=[4,9,14,19,24,29,34]
    x_positions2=[5,10,15,20,25,30,35]
    x_positions3=[6,11,16,21,26,31,36]


    print "\n\nwritten coeff. file:",coeff2_filename
    print "\n\nwritten coeff. file:",coeff3_filename

    file_coeff2.close()   # files with the coeff of the models vs bins
    file_coeff3.close()



    ###################  i create the figure

    fig = plt.figure(figsize=(10,6))
    fig.canvas.set_window_title('Group'+str(bmi_group))  # name for the window
    ax1 = fig.add_subplot(111)
 #   plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)  the figure will occupy less space than the actual window



    models="123"   #to plot one/several models in the same figure


    if '1' in models:

    #### several series in the same figure
        bp1=plt.boxplot(list_lists_ypositions_model1,positions=x_positions1,notch=1, sym='', whis=2)  #  'gD' for a diff symbol for the outlayers  
        plt.setp(bp1['boxes'], color='black')
        plt.setp(bp1['whiskers'], color='black')
        
  #  plt.setp(bp1['fliers'], color='black', marker='+')  for the color of the outliers
          # sym='' no outliers
          # sym='+' for diff colors + and - outlayers
          # sym='-' for a vertical line connecting all outlayers in same box
          # sym='gD' for a diff symbol for the outlayers     
          # notch=1 for a notch around the median, =0 no notch
          # wisker lengh modified with whis=...  (units of SD??)

   
    if '2' in models:
        bp2=plt.boxplot(list_lists_ypositions_model2,positions=x_positions2,notch=1, sym='',whis=2)  #  'gD' for a diff symbol for the outlayers    
        plt.setp(bp2['boxes'], color='blue')
        plt.setp(bp2['whiskers'], color='blue')

  
    if '3' in models:
        bp3=plt.boxplot(list_lists_ypositions_model3,positions=x_positions3,notch=1, sym='',whis=2)  #  'gD' for a diff symbol for the outlayers     
        plt.setp(bp3['boxes'], color='green')
        plt.setp(bp3['whiskers'], color='green')
        

    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.8)   # show a grid

    
    list_xtick_names = ['t=5','t=10','t=20','t=40','t=80','t=160','t=320']
    xtickNames = plt.setp(ax1, xticklabels=list_xtick_names)
    plt.setp(xtickNames, rotation=0, fontsize=14)
    #    ax1.set_ylabel('Weight change ')


    #####text for the set sizes:
    x_text=0.05
    y_text=0.9
    for i in range(len(list_lists_ypositions_model1)):
        print i, len(list_lists_ypositions_model1[i])
    
        ax1.text(x_text,y_text,  'N='+str(len(list_lists_ypositions_model1[i])),va='top',transform=ax1.transAxes, fontsize=10)
        x_text+=1./len(list_lists_ypositions_model1)


   
 #   ax1.legend( ('Model1', 'Model2', 'Model3'), loc='lower left')   # the colors dont match WHY???

    ax1.set_ylim(ymin,ymax)  # y range
    ax1.set_xlim(xmin, xmax)    # x range


    a="%.1f" % first_i_bmi # i get just 1 decimal
    b="%.1f" % last_i_bmi 
    

    figure_title= 'group '+str(bmi_group)+", bmi: "+a+"-"+b+", N="+str(num_users_group)+ " users"
    ax1.set_title(figure_title, fontsize=20)
    ax1.set_xlabel('time bins', fontsize=20)
  
   
    figure_name="./analysis_time_bins_bmi_groups/Weight_change_in_bins_models123_bmi_group"+str(bmi_group)+".png"
    plt.savefig(figure_name)
    print "created figure:",figure_name

    plt.show()


################################################

          
if __name__ == '__main__':
#    if len(sys.argv) > 2:
 #       master_csv = sys.argv[1]
  #      strength_links_csv = sys.argv[2]
       

        main()
   # else:
    #    print "usage: python  whatever.py   path/master.csv  path/strength_links.csv"
 
     

##############################################
