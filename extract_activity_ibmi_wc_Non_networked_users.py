#! /usr/bin/env python




import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import *
import math
from pylab import *
import numpy
from scipy import stats



def main ():


 
    database = "calorie_king_social_networking_2010"  #the old data was:  calorie_king_social_networking
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"





    directory="method3/networks/"  
    filename="engaged_adh_non_networked_users_values_weigh_change_activity_ibmi.csv" 
    file = open(directory+filename,'wt')
    print >> file, "pwc","act","ibmi","time_in_system.days"


    file.close()








    db= Connection(server, database, user, passwd)  #i open the database


    query1="""select  dest,src  from friends"""   
    result1 = db.query(query1) #list of dict: [{'dest': '', 'src': '  '},{'dest': '  ', 'src': '  '},{... },...]

    list_friends=[]
    for r in result1:
        if r['src'] not in list_friends:
            list_friends.append(r['src'])

        if r['dest'] not in list_friends:
            list_friends.append(r['dest'])

        




    id_cont=0
    list_engaged_adh_non_networked_users=[]

    query2="""select * from activity_combined"""
    result2 = db.query(query2) #list of dict: [{'ck_id': '', 'activity_date': '  ', 'activity_flag': '   '},{'ck_id': '', 'activity_date': '  ', 'activity_flag': '   '},...]

    for r in result2:
        if r['ck_id'] not in list_friends:  # only NON-NETWORKED people

            calking_id=r['ck_id']

            query3="select *  from activity_combined  where (ck_id ='"+str(calking_id)+"')  order by activity_date asc"
            result3=db.query(query3)  #[{'ck_id': 'calking_id','activity_date': '', 'activity_flag': '   '},,{... },...]
           



            time_in_system=result3[-1]['activity_date']-result3[0]['activity_date']# type: timedelta         

            activity=len(result3)
            
           

            if int(time_in_system.days)>100:  # only select engaged users

                weigh_ins=0

                for dicc in result3:  # i count the # weigh-ins of this engaged user

                    if  dicc['activity_flag']=='WI':
                        weigh_ins+=1

                if weigh_ins>=5:
          
                    query4="select ck_id, initial_weight, most_recent_weight, height  from users  where (ck_id ='"+str(calking_id)+"')"
                    result4=db.query(query4) 


                   
                    initial_BMI=float(result4[0]['initial_weight'])*703.0/float(result4[0]['height']*result4[0]['height'])



                    if initial_BMI>25.0:
                        weight_change=float(result4[0]['most_recent_weight'])-float(result4[0]['initial_weight'])
                    
                    
                        percentage_weight_change=weight_change*100.0/float(result4[0]['initial_weight'])


                        print id_cont
 t
                        list_engaged_adh_non_networked_users.append(calking_id)
                  

                        file = open(directory+filename,'at')
                        print >> file, percentage_weight_change,activity,initial_BMI,time_in_system.days
                        file.close()
                        
                        id_cont+=1

    print "# engaged adh non_networked users:",len(list_engaged_adh_non_networked_users)
#########################
      
        



if __name__== "__main__":

    main()   

    try:
        import psyco
    except ImportError: pass
