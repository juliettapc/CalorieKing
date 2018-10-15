#! /usr/bin/env python

import csv
import networkx as nx
import numpy
import sys

def main():



    name1="./network_all_users/master_csv_gender_pay_info.csv"           
    file1=open(name1, 'wt')   



   
    print >> file1,'id','ck_id','join_date','initial_weight','most_recent_weight','height','age','weighins','initial_bmi','final_bmi','percentage_weight_change','weight_change','time_in_system','outcome20','outcome50','p_50','act_20','wi_20','p_friend','R6_overlap','degree','friend_avg','activity','gender','paying_info'



   

    original_file= csv.reader(open("./network_all_users/master_csv.csv", 'rb'), delimiter=',')#, quotechar='|')

   
    dict_dict_master={}

    cont1=0
    for row in original_file:
        if cont1>0:           
          
            label=row[1]
            dict_one_user={}

            dict_one_user['id']=int(row[0])
            dict_one_user['ck_id']=str(row[1])
            dict_one_user['join_date']=row[2]
            dict_one_user['initial_weight']=row[3]
            dict_one_user['most_recent_weight']=row[4]
            dict_one_user['height']=row[5]
            dict_one_user['age']=row[6]
            dict_one_user['weighins']=row[7]
            dict_one_user['initial_bmi']=row[8]
            dict_one_user['final_bmi']=row[9]
            dict_one_user['percentage_weight_change']=row[10]
            dict_one_user['weight_change']=row[11]
            dict_one_user['time_in_system']=row[12]
            dict_one_user['outcome20']=row[13]
            dict_one_user['outcome50']=row[14]
            dict_one_user['p_50']=row[15]
            dict_one_user['act_20']=row[16]
            dict_one_user['wi_20']=row[17]
            dict_one_user['p_friend']=row[18]
            dict_one_user['R6_overlap']=row[19]           
            dict_one_user['degree']=row[20]

            if int(dict_one_user['degree']) == 0:
                dict_one_user['friend_avg']="NA"
            else:
                dict_one_user['friend_avg']=row[21]

            dict_one_user['activity']=row[22]
                 
            
      


            dict_dict_master[label]=dict_one_user
        cont1+=1




    file_name2="./data_2009_2010_generated_in2013_includes_gender_paying/paid.txt"
    file2=open(file_name2,'r')
    list_lines_file=file2.readlines()        
        

    dict_user_paying={}
            
    for line in list_lines_file:     # read paying info from file
        
        list_one_line=line.split(",")   

        ck_id=  str(list_one_line[0])
        paying_info=list_one_line[1].strip("\r\n") #remove them together! (this is how the jump is coded in certain op. systems)

        dict_user_paying[ck_id]=paying_info




  
    file_name3="data_2009_2010_generated_in2013_includes_gender_paying/users.txt"
    file3=open(file_name3,'r')
    list_lines_file3=file3.readlines()                    

    dict_user_gender={}
            
    for line in list_lines_file3:      # read gender info from file
        
        list_one_line=line.split(",")   

        ck_id= str(list_one_line[0])
        gender=list_one_line[8].strip("\r\n")   #remove them together! (this is how the jump is coded in certain op. systems)

        dict_user_gender[ck_id]=gender





    for item in dict_dict_master:   # loop over the KEYS of the dict   (== over the ck_ids)
     
       # print dict_dict_master[item]['ck_id']
        #print item

        print >> file1, dict_dict_master[item]['id'],dict_dict_master[item]['ck_id'],dict_dict_master[item]['join_date'],dict_dict_master[item]['initial_weight'],dict_dict_master[item]['most_recent_weight'],dict_dict_master[item]['height'],dict_dict_master[item]['age'],dict_dict_master[item]['weighins'],dict_dict_master[item]['initial_bmi'],dict_dict_master[item]['final_bmi'],dict_dict_master[item]['percentage_weight_change'],dict_dict_master[item]['weight_change'],dict_dict_master[item]['time_in_system'],dict_dict_master[item]['outcome20'],dict_dict_master[item]['outcome50'],dict_dict_master[item]['p_50'],dict_dict_master[item]['act_20'],dict_dict_master[item]['wi_20'],dict_dict_master[item]['p_friend'],dict_dict_master[item]['R6_overlap'],dict_dict_master[item]['degree'],dict_dict_master[item]['friend_avg'],dict_dict_master[item]['activity'],dict_user_gender[item],dict_user_paying[item]
  

    file1.close()

    print "written combined master file:", name1
       
        

################################################

          
if __name__ == '__main__':
#    if len(sys.argv) > 2:
 #       master_csv = sys.argv[1]
  #      strength_links_csv = sys.argv[2]
       

        main()
   # else:
    #    print "usage: python  whatever.py   path/master.csv  path/strength_links.csv"
 
     

##############################################
