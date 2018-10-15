#! /usr/bin/env python

"""
Created by Julia Poncela of June 2012

Analyze the strength of the links with R6s, defined as #_messages/tot.

"""


import sys
import os
from datetime import *
import math
import numpy
from scipy import stats
from database import *   #package to handle databases
import networkx as nx
import random
import histograma_gral
import histograma_bines_gral
import GINI_coef

def main (graph_name_GC):


   
   
    H1 = nx.read_gml(graph_name_GC)   # just GC, but with Role info
    H1 = nx.connected_component_subgraphs(H1)[0] 


    print len(H1.nodes())

    

    list_R6_labels=[]
    dicc_label_node={}
    list_network_ids=[]
    for node in H1.nodes():
              
        if (H1.node[node]['role'] =="special_R6"):
            H1.node[node]['role'] ="R6"

        list_network_ids.append(int(H1.node[node]['label']))# this actually corresponds to the id from the users table in the DB
        dicc_label_node[int(H1.node[node]['label'])]=node
      
        if (H1.node[node]['role'] =="R6"):
            list_R6_labels.append(int(H1.node[node]['label']))# this actually corresponds to the id from the users table in the DB
      

    #print "# R6s:",len(list_R6_labels)
    
  #  print len(dicc_label_node)

    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    query1="""select * from users"""    
    result1 = db.query(query1)  # is a list of dict.



 
    file1 = open("num_messg_to_friends_vs_Gini.dat",'wt')
    file2 = open("num_messg_from_friends_vs_Gini.dat",'wt')
    file3 = open("num_messg_friends_vs_Gini.dat",'wt')

    file11 = open("num_messg_to_friends_vs_Gini_R6s.dat",'wt')
    file12 = open("num_messg_from_friends_vs_Gini_R6s.dat",'wt')
    file13 = open("num_messg_friends_vs_Gini_R6s.dat",'wt')

    file111 = open("num_messg_to_friends_vs_Gini_R6overlap.dat",'wt')
    file112 = open("num_messg_from_friends_vs_Gini_R6overlap.dat",'wt')
    file113 = open("num_messg_friends_vs_Gini_R6overlap.dat",'wt')


   

    dict_characteristics_users={}



    dicc_ck_label={}
    for r1 in result1:   #first i build a dicc ck_id vs. label        
      ck_id=r1['ck_id']      
      label=int(r1['id'])  # this corresponds to the 'label' in the gml files
      dicc_ck_label[ck_id]=label

      try:
          node=dicc_label_node[label]
          H1.node[node]['ck_id']=ck_id
        #  print "\n",H1.node[node]['ck_id'], label
      except KeyError: pass

    print len(dicc_ck_label)

    


    list_sent_from_not_friends=[]
    list_sent_to_not_friends=[]
    list_tot_sent=[]
    list_tot_received=[]

    list_to_friends=[]
    list_from_friends=[]      
    list_tot_messg_friends=[]

    list_GINI_weighted_to_friends=[]   # one value per USER
    list_GINI_weighted_from_friends=[]      
    list_GINI_weighted_tot_messg_friends=[]

    list_GINI_weighted_to_friends_R6s=[]   # one value per USER
    list_GINI_weighted_from_friends_R6s=[]      
    list_GINI_weighted_tot_messg_friends_R6s=[]

    list_GINI_weighted_to_friends_R6overlap=[]   # one value per USER
    list_GINI_weighted_from_friends_R6overlap=[]      
    list_GINI_weighted_tot_messg_friends_R6overlap=[]


    list_weights_friendships=[]

    list_weights_friendships_with_R6s=[]
    list_weights_friendships_to_R6s=[]
    list_weights_friendships_from_R6s=[]




    list_blog_posts=[]
    list_home_page=[]
    list_forum_posts=[]
    list_lesson_com=[]
    list_tot_public_mess=[]

    list_tot_activity=[]
    list_num_tot_messg=[]



    num_users=0.
    for r1 in result1:   #loop over users 
      num_users+=1.
     
      print int(num_users)
      ck_id=r1['ck_id']
      label=int(r1['id'])  # this corresponds to the 'label' in the gml files
      try:
          node=dicc_label_node[label]
      except KeyError: pass



  #    query3="select  * from private_messages where (src_id ='"+str(ck_id)+"') "  
   #   result3= db.query(query3)
    #  tot_sent=float(len(result3))
     
 






    #  query4="select  * from private_messages where  (dest_id ='"+str(ck_id)+"') "   
     # result4= db.query(query4)
      #tot_received=float(len(result4))
      

      query5="select  * from private_messages where (src_id ='"+str(ck_id)+"')or (dest_id ='"+str(ck_id)+"') "   # all messages
      result5= db.query(query5)
      num_tot_messg=float(len(result5))




      tot_sent=0
      tot_received=0
      for r5 in result5:
          if r5['src_id']==ck_id:
              tot_sent+=1
          elif r5['dest_id']==ck_id:
              tot_received+=1 
     


        
      query6="SELECT * FROM activity_combined where activity_flag != 'WI' and  activity_flag != 'PM' and ck_id='"+str(ck_id)+"'   "     
      result6= db.query(query6)
      tot_public_mess=len(result6)


      query7="SELECT * FROM activity_combined where activity_flag != 'WI' and ck_id='"+str(ck_id)+"'   "     
      result7= db.query(query7)
      tot_activity=len(result7)



    


      blog_posts=0
      home_page=0
      forum_posts=0
      lesson_com=0
      for r6 in result6:  # public messages:

          if r6['activity_flag']=='BC':
              blog_posts+=1
          elif r6['activity_flag']=='HP':
              home_page+=1
          elif r6['activity_flag']=='FP':
              forum_posts+=1
          elif r6['activity_flag']=='LC':
              lesson_com+=1             
    
      
      list_blog_posts.append(blog_posts)
      list_home_page.append(home_page)
      list_forum_posts.append(forum_posts)
      list_lesson_com.append(lesson_com)
      list_tot_public_mess.append(tot_public_mess)

      list_tot_activity.append(tot_activity)

      list_num_tot_messg.append(num_tot_messg)


    #  print ck_id,"tot public:", tot_public_mess, "blogs:",blog_posts, "home page:",home_page, "forum:",forum_posts, "lessons",lesson_com, "tot private:", num_tot_messg,"tot sent:",tot_sent,"tot_received:",tot_received,"tot act:",tot_activity
  


      query3="select  * from private_messages where (src_id ='"+str(ck_id)+"')  "  # there are messages sent by/to people not in the Users table, that is because they join the system prior 1-jan-2009, and are not part of the 47,000 users.
      result3= db.query(query3)
      num_sent=float(len(result3))
      list_tot_sent.append(num_sent)




      query4="select  * from private_messages where (dest_id ='"+str(ck_id)+"')  "
      result4= db.query(query4)
      num_received=float(len(result4))
      list_tot_received.append(float(num_received))



     # if num_users <=5000:    # JUST TO TEST THE CODE

      if label in list_network_ids:  # if the user is in the network, i check how many messages they send each other
          to_not_friends=0          
          from_not_friends=0          
          print "\n\nnode label",label,ck_id,"has degree:",H1.degree(node)

          query2="select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"') "
          result2= db.query(query2)          
          degree=len(result2)                         
      


          
         

          for r3 in result3:  # i count how many messages are sent to friends and non-friends

            ck_friend=r3['dest_id']                  
            if ck_friend in dicc_ck_label:  #  because some messages are NOT sent by users (join date prior jan.2009)   
               label_friend=dicc_ck_label[ck_friend]

               if label_friend in dicc_label_node:    
                  node_friend=dicc_label_node[label_friend]
                                 
                  flag_friend=0
                  node_sender=dicc_label_node[label]  # the user i am currently studying
                  for n in H1.neighbors(node_sender):
                      if n==node_friend:
                          flag_friend=1                      

                  if flag_friend==0:
                      to_not_friends+=1  
                     



          for r4 in result4:   # i count how many messages are from friends and non-friends

            ck_friend=str(r4['src_id'])
            if ck_friend in dicc_ck_label: # i double check, because some messages are NOT sent by users...(join date prior jan.2009)   
               label_friend=dicc_ck_label[ck_friend]

               if label_friend in dicc_label_node:  
                  node_friend=dicc_label_node[label_friend]
               

                  flag_friend=0
                  node_receiver=dicc_label_node[label]
                  for n in H1.neighbors(node_receiver):
                      if n==node_friend:
                          flag_friend=1

                  if flag_friend==0:
                      from_not_friends+=1
                    



          num_messg_friends=0.
          num_messg_to_friends=0.
          num_messg_from_friends=0.
          flag_sent=0
          flag_received=0

          list_weighted_to_friends=[] # one value per FRIEND of a given user
          list_weighted_from_friends=[]
          list_weighted_tot_messg_friends=[]

          list_weighted_to_friends_norm=[]   # one value per FRIEND of a given user, normalized by the tot number of messages that user sent
          list_weighted_from_friends_norm=[]
          list_weighted_tot_messg_friends_norm=[]

          list_weighted_to_friends_R6s_norm=[]   # one value per FRIEND of a given user, normalized by the tot number of messages that user sent
          list_weighted_from_friends_R6s_norm=[]
          list_weighted_tot_messg_friends_R6s_norm=[]



          for f in H1.neighbors(node):
             
              messg_to_one_friend=0.    #looking at a particular friend
              messg_from_one_friend=0.
              messg_one_friend=0.


              for r5 in result5:
                
                  if r5['src_id']== ck_id   and   r5['dest_id']== H1.node[f]['ck_id']:                      
                      num_messg_to_friends+=1.
                      num_messg_friends+=1.
                      flag_sent=1

                      messg_to_one_friend+=1.
                      messg_one_friend+=1.

                  elif r5['dest_id']== ck_id   and   r5['src_id']== H1.node[f]['ck_id']:                      
                      num_messg_from_friends+=1.
                      num_messg_friends+=1.
                      flag_received=1

                      messg_from_one_friend+=1.
                      messg_one_friend+=1.

           
              list_weighted_to_friends.append(messg_to_one_friend)    # weight of each friendship    (not normalized)          
              list_weighted_from_friends.append(messg_from_one_friend)                                     
              list_weighted_tot_messg_friends.append(messg_one_friend) 



              if H1.node[f]['role']=='R6':       #if the friend is an R6s                  
                  list_weights_friendships_to_R6s.append(messg_from_one_friend) 
                  list_weighted_to_friends_R6s_norm.append(messg_to_one_friend) 
                 
              if H1.node[node]['role']=='R6':                   
                  list_weights_friendships_from_R6s.append(messg_to_one_friend)
                  list_weighted_from_friends_R6s_norm.append(messg_from_one_friend) 
                  
              if H1.node[node]['role']=='R6' or H1.node[f]['role']=='R6':    
                  list_weights_friendships_with_R6s.append(messg_one_friend)
                  list_weighted_tot_messg_friends_R6s_norm.append(messg_one_friend)


          for item in list_weighted_tot_messg_friends:
              if sum(list_weighted_tot_messg_friends)>0:
                  list_weighted_tot_messg_friends_norm.append(item/sum(list_weighted_tot_messg_friends))

          for item in list_weighted_to_friends:
              if sum(list_weighted_to_friends)>0:
                  list_weighted_to_friends_norm.append(item/sum(list_weighted_to_friends))

          for item in list_weighted_from_friends:
               if sum(list_weighted_from_friends)>0:
                   list_weighted_from_friends_norm.append(item/sum(list_weighted_from_friends))



          for i in range(len(list_weighted_tot_messg_friends_R6s_norm)):   # how important is the communication with any R6 friend, compare to the tot # messag
              if sum(list_weighted_tot_messg_friends_R6s_norm)>0:
                  list_weighted_tot_messg_friends_R6s_norm[i]=list_weighted_tot_messg_friends_R6s_norm[i]/float(sum(list_weighted_tot_messg_friends_R6s_norm))

          for i in range(len(list_weighted_to_friends_R6s_norm)):
              if sum(list_weighted_to_friends_R6s_norm)>0:          
                  list_weighted_to_friends_R6s_norm[i]=list_weighted_to_friends_R6s_norm[i]/float(sum(list_weighted_to_friends_R6s_norm))

          for i in range(len(list_weighted_from_friends_R6s_norm)):
              if sum(list_weighted_from_friends_R6s_norm)>0:          
                  list_weighted_from_friends_R6s_norm[i]=list_weighted_from_friends_R6s_norm[i]/float(sum(list_weighted_from_friends_R6s_norm))
        


# no puedo normalizar over and over again los primero elementos muchas mas veces que los ultimos agnadidos!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          for i in range(len(list_weighted_tot_messg_friends)):   # how important is the communication with any R6 friend, compare to the tot # messag
                  list_weights_friendships_with_R6s.append(list_weighted_tot_messg_friends[i])

          for i in range(len(list_weighted_to_friends)):                   
                  list_weights_friendships_to_R6s.append(list_weighted_to_friends[i])

          for i in range(len(list_weighted_from_friends)):                      
                  list_weights_friendships_from_R6s.append(list_weighted_from_friends[i])
         


          list_to_friends.append(num_messg_to_friends) 
          list_from_friends.append(num_messg_from_friends)  
          list_tot_messg_friends.append(num_messg_friends)
          

        #  print "norm list weighted tot friendships:",list_weighted_tot_messg_friends_norm,"with R6s:",list_weights_friendships_with_R6s


     # i calculate how skewed friendships for a given user are:
          if len(list_weighted_to_friends) >0 and sum(list_weighted_to_friends)>0:
              Gini_to_friends=GINI_coef.calculate_GINI(list_weighted_to_friends)
              list_GINI_weighted_to_friends.append(Gini_to_friends)   # one value per USER

            #  print  ",to friends: ", list_weighted_to_friends, sum(list_weighted_to_friends),Gini_to_friends
              print >> file1,H1.degree(node), sum(list_weighted_to_friends), sum(list_weighted_to_friends)/float(H1.degree(node)),Gini_to_friends


              if (H1.node[node]['role'] =="R6"):
                  list_GINI_weighted_to_friends_R6s.append(Gini_to_friends)   
                  print >> file11,H1.degree(node), sum(list_weighted_to_friends),sum(list_weighted_to_friends)/float(H1.degree(node)),Gini_to_friends

              if (H1.node[node]['R6_overlap'] >0):
                  list_GINI_weighted_to_friends_R6overlap.append(Gini_to_friends)   
                  print >> file111,H1.degree(node), sum(list_weighted_to_friends),sum(list_weighted_to_friends)/float(H1.degree(node)),Gini_to_friends





          if len(list_weighted_from_friends) >0 and sum(list_weighted_from_friends)>0:
              Gini_from_friends=GINI_coef.calculate_GINI(list_weighted_from_friends)
              list_GINI_weighted_from_friends.append(Gini_from_friends) 
    
             # print  ",from friends: ", list_weighted_from_friends, sum(list_weighted_from_friends),Gini_from_friends
              print >> file2, H1.degree(node),  sum(list_weighted_from_friends), sum(list_weighted_from_friends)/float(H1.degree(node)),Gini_from_friends

              if (H1.node[node]['role'] =="R6"):
                 list_GINI_weighted_from_friends_R6s.append(Gini_from_friends)  
                 print >> file12, H1.degree(node),  sum(list_weighted_from_friends),  sum(list_weighted_from_friends)/float(H1.degree(node)),Gini_from_friends

              if (H1.node[node]['R6_overlap'] >0):
                 list_GINI_weighted_from_friends_R6overlap.append(Gini_from_friends)  
                 print >> file112, H1.degree(node),  sum(list_weighted_from_friends),  sum(list_weighted_from_friends)/float(H1.degree(node)),Gini_from_friends

          if len(list_weighted_tot_messg_friends) >0 and sum(list_weighted_from_friends)>0:
              Gini_friends=GINI_coef.calculate_GINI(list_weighted_tot_messg_friends)
              list_GINI_weighted_tot_messg_friends.append(Gini_friends)

            #  print  ",tot: ",list_weighted_tot_messg_friends , sum(list_weighted_tot_messg_friends),Gini_friends
              print >> file3, H1.degree(node), sum(list_weighted_tot_messg_friends), sum(list_weighted_tot_messg_friends)/float(H1.degree(node)),Gini_friends
        
              if (H1.node[node]['role'] =="R6"):
                   list_GINI_weighted_tot_messg_friends_R6s.append(Gini_friends)
                   print >> file13, H1.degree(node), sum(list_weighted_tot_messg_friends),sum(list_weighted_tot_messg_friends)/float(H1.degree(node)),Gini_friends
        
              if (H1.node[node]['R6_overlap'] >0):
                   list_GINI_weighted_tot_messg_friends_R6overlap.append(Gini_friends)
                   print >> file113, H1.degree(node), sum(list_weighted_tot_messg_friends),sum(list_weighted_tot_messg_friends)/float(H1.degree(node)),Gini_friends
        
                      
         
          if num_received != 0:
              list_sent_from_not_friends.append(float(from_not_friends))
          if num_sent != 0:
              list_sent_to_not_friends.append(float(to_not_friends))




    file1.close()
    file2.close()
    file3.close()

    print "average from_not_friends:", numpy.mean(list_sent_from_not_friends)
    print "average to_not_friends:", numpy.mean(list_sent_to_not_friends)
    
    print "average to_friends:", numpy.mean(list_to_friends)
    print "average from_friends:", numpy.mean(list_from_friends)
    print "average tot messg friends:", numpy.mean(list_tot_messg_friends)
    
    print "average tot sent:", numpy.mean(list_tot_sent)
    print "average tot received:", numpy.mean(list_tot_received)



  

    histograma_bines_gral.histograma_bins(list_GINI_weighted_to_friends,75, "Gini_weight_to_friends")   
    histograma_bines_gral.histograma_bins(list_GINI_weighted_from_friends,75, "Gini_weight_from_friends")   
    histograma_bines_gral.histograma_bins(list_GINI_weighted_tot_messg_friends,75, "Gini_weight_tot_friends")  


    histograma_bines_gral.histograma_bins(list_GINI_weighted_to_friends_R6s,75, "Gini_weight_to_friends_R6s") 
    histograma_bines_gral.histograma_bins(list_GINI_weighted_from_friends_R6s,75, "Gini_weight_from_friends_R6s")   
    histograma_bines_gral.histograma_bins(list_GINI_weighted_tot_messg_friends_R6s,75, "Gini_weight_tot_friends_R6s")  


    histograma_bines_gral.histograma_bins(list_GINI_weighted_to_friends_R6overlap,75, "Gini_weight_to_friends_R6overlap") 
    histograma_bines_gral.histograma_bins(list_GINI_weighted_from_friends_R6overlap,75, "Gini_weight_from_friends_R6overlap")   
    histograma_bines_gral.histograma_bins(list_GINI_weighted_tot_messg_friends_R6overlap,75, "Gini_weight_tot_friends_R6overlap")  





    histograma_gral.histograma(list_sent_from_not_friends, "not_from_friends")
    histograma_gral.histograma(list_sent_to_not_friends, "not_to_friends")

    histograma_gral.histograma(list_tot_sent, "tot_mess_sent")
    histograma_gral.histograma(list_tot_received, "tot_mess_received")
    histograma_gral.histograma(list_num_tot_messg, "num_tot_mess")


    histograma_gral.histograma(list_to_friends, "mess_to_friends")   #data, string_for_output_file_name
    histograma_gral.histograma(list_from_friends, "mess_from_friends")  
    histograma_gral.histograma(list_tot_messg_friends, "tot_mess_friends")   

    histograma_gral.histograma(list_blog_posts, "num_blog_posts")
    histograma_gral.histograma(list_home_page, "num_home_page_posts")
    histograma_gral.histograma(list_forum_posts, "num_forum_posts")
    histograma_gral.histograma(list_lesson_com, "num_lesson_com")
    histograma_gral.histograma(list_tot_public_mess, "num_tot_public_messages")

    histograma_gral.histograma(list_tot_activity, "num_tot_activity")
      
      
     
 
###############################################

          
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename1 = sys.argv[1]
       

        main(graph_filename1)
    else:
        print "usage: python  whatever.py   path/network_file2_R6s_info.gml  "
 
     

##############################################
