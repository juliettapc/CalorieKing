#! /usr/bin/env python

"""
Created by Julia Poncela of August 2012

It queries the DB to create quarter or semester networks, using a window of time, and the users ACTIVE during that time (not cummulative from one quarter to the next, as the previous versions of these networks: calorie_king_hg/5_points_network_2010/data)

"""

from database import *
import sys
import os
import networkx as nx
from transform_labels_to_nx import *
import histograma_gral
import numpy
import datetime

def main ():



    G= nx.Graph()  # i create an empty network object
    directory='./semester_quarter_window_networks/'



    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 


  #  initial_date=datetime.datetime(2009,01,01)      # time window to build the network of active users
   # final_date=datetime.datetime(2009,03,31)

   # initial_date=datetime.datetime(2009,04,01)      
    #final_date=datetime.datetime(2009,06,30)

  #  initial_date=datetime.datetime(2009,07,01)      
   # final_date=datetime.datetime(2009,10,01)

    #initial_date=datetime.datetime(2009,10,01)      
    #final_date=datetime.datetime(2009,12,31)

  #  initial_date=datetime.datetime(2010,01,01)      
   # final_date=datetime.datetime(2010,03,31)

  #  initial_date=datetime.datetime(2010,04,01)      
   # final_date=datetime.datetime(2010,06,30)

  #  initial_date=datetime.datetime(2010,07,01)      
   # final_date=datetime.datetime(2010,10,01)
    
#    initial_date=datetime.datetime(2010,10,01)      
 #   final_date=datetime.datetime(2010,12,31)
  

#----  

 #   initial_date=datetime.datetime(2009,01,01) 
  #  final_date=datetime.datetime(2009,06,30)


  #  initial_date=datetime.datetime(2009,07,01)  
   # final_date=datetime.datetime(2009,12,31)


#    initial_date=datetime.datetime(2010,01,01)   
 #   final_date=datetime.datetime(2010,06,30)


 #   initial_date=datetime.datetime(2010,07,01)    
  #  final_date=datetime.datetime(2010,12,31)

#-----

    initial_date=datetime.datetime(2009,01,01)      
    final_date=datetime.datetime(2010,12,31)
    


    period='all_NEW_LOGIC'



    print period,initial_date, final_date

 # OJOOOOOO!!! EN LA BASE DE DATOS HAY FECHAS EN DATETIME.DATE Y OTRAS EN DATETIME.DATETIME!!!
# convertir todas a datetime.datetime





# i only query the FRIENDS table (instead of the USERS table), because even if i repeat users, there are many more non-networked users so it is more efficient
    friends_query = """SELECT * FROM friends   """        #10065 rows
 #   friends_query = """SELECT f.* FROM friends AS f, users as u WHERE (f.src = u.ck_id or f.dest = u.ck_id) and u.is_staff='public' """      #17340  rows
    result1 = db.query(friends_query)  # is a list of dict.
  

#OJOOOOOOOOOOOO THE QUERY
#   friends_query = """SELECT f.* FROM friends AS f, users as u WHERE (f.src = u.ck_id AND f.dest = u.ck_id) and u.is_staff='public' """      # 29  rows, CORRESPONDING TO THE SELF LOOPS-->> THE ONE WITH OR, MIGHT NOT BE THE RIGHT ONE EITHER????


    num_friendships=0
    list_users=[]
    dict_ck_ids_labels={}
   
    
    for r1 in result1:    # loop over pairs of friends


    #  if num_users<=100: # THIS LINE IS JUST TO TEST THE CODE!!!!!!!!!!!!

        num_friendships+=1
        print num_friendships


        src=r1['src']
        dest=r1['dest']

        flag_friendship=1
      

         ##########
        # NODE1: #
        ##########
        query_activity_src = """SELECT * FROM activity_combined where ck_id = '"""+src+"""' order by activity_date asc"""  #always, the first activity of a user is WI
        result_activity_src=db.query(query_activity_src)
#        print src

        if len(result_activity_src)>0: # the users that are not in the USERS table, dont have any activity at all, either


          fecha_first=result_activity_src[0]['activity_date']
          first_date_src=datetime.datetime(fecha_first.year, fecha_first.month, fecha_first.day)

          fecha_last=result_activity_src[-1]['activity_date']
          last_date_src=datetime.datetime(fecha_last.year, fecha_last.month, fecha_last.day)
        

       
          if (last_date_src >= initial_date  and last_date_src <= final_date) or (first_date_src >= initial_date  and first_date_src <= final_date):  # condition for an active user

            if src  in list_users:   # if i have encountered this user before
               
              label_src=dict_ck_ids_labels[src]
            #  print label_src "old node"
            else:   # if new user
             
              query_user_src = """SELECT * from users where ck_id = '"""+src+"""'"""   # i need this, even for a non new user!!! so i can add the proper link 
              result_user_src=db.query(query_user_src)
            
              if len(result_user_src)  >0:    # because some friends are not in the users table! RECONSIDER DAN'S QUERY????????
                label_src=int(result_user_src[0]['id'])
                dict_ck_ids_labels[src]=label_src

                print "node:",label_src

                G.add_node(label_src)   # add node and its attributes to the network
                list_users.append(src)
               
                
                fecha=result_user_src[0]['join_date']
                join_date_src=datetime.datetime(fecha.year, fecha.month, fecha.day)
                absolute_initial_weight_src=float(result_user_src[0]['initial_weight'])
                height_src=float(result_user_src[0]['height'])
                age_src=int(result_user_src[0]['age'])
            
            
                num_WI_src=0
                num_BC_src=0
                num_PM_src=0
                num_FC_src=0
                num_LC_src=0
               
                tot_list_dates=[]
                list_dates_included=[]
                for r in result_activity_src:    # i only count the activity during the time window of the network!!!
                    fecha=r['activity_date']
                    activity_date_src=datetime.datetime(fecha.year, fecha.month, fecha.day)
                    tot_list_dates.append(activity_date_src)
                    if activity_date_src >= initial_date  and activity_date_src <= final_date:  # the activity happened during the time window
                        list_dates_included.append(activity_date_src)

                        if r['activity_flag']=='WI':
                            num_WI_src+=1                            
                        if r['activity_flag']=='BC':
                            num_BC_src+=1
                        if r['activity_flag']=='PM':
                            num_PM_src+=1
                        if r['activity_flag']=='FC':
                            num_FC_src+=1
                        if r['activity_flag']=='LC':
                            num_LC_src+=1

                activity_src= num_BC_src+num_BC_src+num_FC_src+num_LC_src


                query_weights_src = """SELECT * FROM weigh_in_history where ck_id = '"""+src+"""' order by on_day asc"""
                result_weights_src=db.query(query_weights_src)

               
                list_weights=[]               
                for rw in result_weights_src:                      
                    fecha=  rw['on_day']
                    weight_date_src=datetime.datetime(fecha.year, fecha.month, fecha.day)
                    if weight_date_src >= initial_date  and weight_date_src <= final_date:  # the weigh_in happened during the time window
                        list_weights.append(float(rw['weight']))



                # i ADD ATTRIBUTES TO THE NODE1

                G.node[label_src]['label']=label_src
                G.node[label_src]['age']=age_src
                G.node[label_src]['height']=height_src
                G.node[label_src]['weighins']=num_WI_src
                G.node[label_src]['activity']=activity_src
                G.node[label_src]['num_BC']=num_BC_src
                G.node[label_src]['num_PM']=num_PM_src
                G.node[label_src]['num_FC']=num_FC_src
                G.node[label_src]['nm_LC']=num_LC_src

              #  G.node[label_src]['first_activity_date']=list_dates_included[0]
               # G.node[label_src]['last_activity_date']=list_dates_included[-1]
               # G.node[label_src]['absolute_first_activity_date']=tot_list_dates[0]
               # G.node[label_src]['absolute_last_activity_date']=tot_list_dates[-1]
                G.node[label_src]['active_period']=(list_dates_included[-1]-list_dates_included[0]).days+1
                G.node[label_src]['total_active_period']=(tot_list_dates[-1]-tot_list_dates[0]).days+1
              
                if len(list_weights)>0:
                    G.node[label_src]['initial_weight']=list_weights[0]   # only from the beginning of this time window
                    G.node[label_src]['initial_bmi']=list_weights[0] *703/(height_src*height_src)
                    G.node[label_src]['final_bmi']=list_weights[-1]  *703/(height_src*height_src)          
                    G.node[label_src]['weight_change']=list_weights[-1]- list_weights[0]               
                    G.node[label_src]['percentage_weight_change']=(list_weights[-1]- list_weights[0])/list_weights[0]*100.0
                    
                    G.node[label_src]['absolute_initial_weight']=absolute_initial_weight_src  # from the beginning of this user's record
                    G.node[label_src]['absolute_initial_BMI']=absolute_initial_weight_src   *703/(height_src*height_src)        
                    G.node[label_src]['absolute_percentage_weight_change']=(list_weights[-1]- absolute_initial_weight_src )/absolute_initial_weight_src*100.0
                    

                else:   # if the user doesn't have any weigh-ins during the period
                    G.node[label_src]['initial_weight']='NA'
                    G.node[label_src]['initial_bmi']='NA'
                    G.node[label_src]['final_bmi']=    'NA'  
                    G.node[label_src]['weight_change']=  'NA'      
                    G.node[label_src]['percentage_weight_change']='NA'
                    
                    G.node[label_src]['absolute_initial_weight']=absolute_initial_weight_src  # from the beginning of this user's record
                    G.node[label_src]['absolute_initial_BMI']=absolute_initial_weight_src   *703/(height_src*height_src)        
                    G.node[label_src]['absolute_percentage_weight_change']='NA'
                    print src, "doesnt have any weigh-ins in that period!"

              else: # if the user is not in the USERS table, then there will be no link
                  flag_friendship=0
          else:  # if the user is not active during that period, then there will be no link
            flag_friendship=0
                      #print "user", src, "has all its activity out of the time window"
      
            

        else:  ## if the user is not in the ACTIVITY_COMBINED table, then there will be no link
             flag_friendship=0
                         

        ##########
        # NODE2: #
        ##########
        query_activity_dest = """SELECT * FROM activity_combined where ck_id = '"""+dest+"""' order by activity_date asc"""
        result_activity_dest=db.query(query_activity_dest)

       # print dest
        if len(result_activity_dest)>0:  # the users that are not in the USERS table, dont have any activity at all, either
        
          fecha_first=result_activity_dest[0]['activity_date']
          first_date_dest=datetime.datetime(fecha_first.year, fecha_first.month, fecha_first.day)
          fecha_last=result_activity_dest[-1]['activity_date']
          last_date_dest=datetime.datetime(fecha_last.year, fecha_last.month, fecha_last.day)

          if (last_date_dest >= initial_date  and last_date_dest <= final_date) or (first_date_dest >= initial_date  and first_date_dest <= final_date):  # condition for an active user


            if dest  in list_users:   # if i have encountered this user before
               
              label_dest=dict_ck_ids_labels[dest]
            else:   # if new user
             
              query_user_dest = """SELECT * from users where ck_id = '"""+dest+"""'"""   # i need this, even for a non new user!!! so i can add the proper link 
              result_user_dest=db.query(query_user_dest)
            
              if len(result_user_dest)  >0:    # because some friends are not in the users table! RECONSIDER DAN'S QUERY????????
                label_dest=int(result_user_dest[0]['id'])
                dict_ck_ids_labels[dest]=label_dest
                print "node:",label_dest

                G.add_node(label_dest)   # add node and its attributes to the network
                list_users.append(dest)
               

              
                
                fecha=result_user_dest[0]['join_date']
                join_date_dest=datetime.datetime(fecha.year, fecha.month, fecha.day)
                absolute_initial_weight_dest=float(result_user_dest[0]['initial_weight'])
                height_dest=float(result_user_dest[0]['height'])
                age_dest=int(result_user_dest[0]['age'])
            
            
                num_WI_dest=0
                num_BC_dest=0
                num_PM_dest=0
                num_FC_dest=0
                num_LC_dest=0

                tot_list_dates=[]
                list_dates_included=[]
                for r in result_activity_dest:    # i only count the activity during the time window of the network!!!
                    fecha=r['activity_date']
                    activity_date_dest=datetime.datetime(fecha.year, fecha.month, fecha.day)
                    tot_list_dates.append(activity_date_dest)
                    if activity_date_dest >= initial_date  and activity_date_dest <= final_date:  # the activity happened during the time window
                        list_dates_included.append(activity_date_dest)

                        if r['activity_flag']=='WI':
                            num_WI_dest+=1                            
                        if r['activity_flag']=='BC':
                            num_BC_dest+=1
                        if r['activity_flag']=='PM':
                            num_PM_dest+=1
                        if r['activity_flag']=='FC':
                            num_FC_dest+=1
                        if r['activity_flag']=='LC':
                            num_LC_dest+=1

                activity_dest= num_BC_dest+num_BC_dest+num_FC_dest+num_LC_dest




                query_weights_dest = """SELECT * FROM weigh_in_history where ck_id = '"""+dest+"""' order by on_day asc"""
                result_weights_dest=db.query(query_weights_dest)


                list_weights=[]                
                for rw in result_weights_dest: 

                    fecha=rw['on_day']                  
                    weight_date_dest=datetime.datetime(fecha.year, fecha.month, fecha.day)
                    if weight_date_dest >= initial_date  and weight_date_dest <= final_date:  # the weigh_in happened during the time window
                        list_weights.append(float(rw['weight']))



                # i ADD ATTRIBUTES TO THE NODE2

                G.node[label_dest]['label']=label_dest
                G.node[label_dest]['age']=age_dest
                G.node[label_dest]['height']=height_dest
                G.node[label_dest]['weighins']=num_WI_dest
                G.node[label_dest]['activity']=activity_dest
                G.node[label_dest]['num_BC']=num_BC_dest
                G.node[label_dest]['num_PM']=num_PM_dest
                G.node[label_dest]['num_FC']=num_FC_dest
                G.node[label_dest]['num_LC']=num_LC_dest
                       
                #G.node[label_dest]['first_activity_date']=list_dates_included[0]    *gml networks with date attributes wont work!!
                #G.node[label_dest]['last_activity_date']=list_dates_included[-1]
               # G.node[label_dest]['absolute_first_activity_date']=tot_list_dates[0]
               # G.node[label_dest]['absolute_last_activity_date']=tot_list_dates[-1]
                G.node[label_dest]['active_period']=(list_dates_included[-1]-list_dates_included[0]).days+1
                G.node[label_dest]['total_active_period']=(tot_list_dates[-1]-tot_list_dates[0]).days+1
              


                if len(list_weights)>0:
                    G.node[label_dest]['initial_weight']=list_weights[0]   # only from the beginning of this time window
                    G.node[label_dest]['initial_bmi']=list_weights[0] *703/(height_dest*height_dest)
                    G.node[label_dest]['final_bmi']=list_weights[-1]  *703/(height_dest*height_dest)          
                    G.node[label_dest]['weight_change']=list_weights[-1]- list_weights[0]               
                    G.node[label_dest]['percentage_weight_change']=(list_weights[-1]- list_weights[0])/list_weights[0]*100.0
                    
                    G.node[label_dest]['absolute_initial_weight']=absolute_initial_weight_dest  # from the beginning of this user's record
                    G.node[label_dest]['absolute_initial_BMI']=absolute_initial_weight_dest   *703/(height_dest*height_dest)        
                    G.node[label_dest]['absolute_percentage_weight_change']=(list_weights[-1]- absolute_initial_weight_dest )/absolute_initial_weight_dest*100.0
                    

                else:   # if the user doesn't have any weigh-ins during the period
                    G.node[label_dest]['initial_weight']='NA'
                    G.node[label_dest]['initial_bmi']='NA'
                    G.node[label_dest]['final_bmi']=    'NA'  
                    G.node[label_dest]['weight_change']=  'NA'      
                    G.node[label_dest]['percentage_weight_change']='NA'
                    
                    G.node[label_dest]['absolute_initial_weight']=absolute_initial_weight_dest  # from the beginning of this user's record
                    G.node[label_dest]['absolute_initial_BMI']=absolute_initial_weight_dest   *703/(height_dest*height_dest)        
                    G.node[label_dest]['absolute_percentage_weight_change']='NA'
                    print dest, "doesnt have any weigh-ins in that period!"

          


              else: # if the user is not in the USERS table, then there will be no link
                  flag_friendship=0

          else:  # if the user is not active during that period, then there will be no link
             flag_friendship=0
                        


        else:  ## if the user is not in the ACTIVITY_COMBINED table, then there will be no link
             flag_friendship=0
                         


        



        if flag_friendship==1:

            try:
                G.add_edge(label_src,label_dest)   #add link if both were active  

                print "  link:",label_src,label_dest

            except:
                print "problem linking" , src, dest
                raw_input()



    nx.write_gml(G,directory+"network_"+str(period)+"_window_from_"+str(initial_date.day)+"_"+str(initial_date.month)+"_"+str(initial_date.year)+"_to_"+str(final_date.day)+"_"+str(final_date.month)+"_"+str(final_date.year)+".gml")



    print period,initial_date,"to",final_date,":  tot # nodes:", len(G.nodes()), "tot # links:", len(G.edges())
#    q_string = master_query + " AND u.join_date >= " + v[0] + " AND u.join_date <= " + v[1] 










 #H=nx.read_gml(name) # create the network from the original input file  

 





 
###############################################

          
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename1 = sys.argv[1]
       

    main()
    #else:
     #   print "usage: python  whatever.py   path/network_file2_R6s_info.gml  "
 
 






###################################################
