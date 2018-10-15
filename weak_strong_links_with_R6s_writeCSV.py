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
              
        list_network_ids.append(int(H1.node[node]['label']))# this actually corresponds to the id from the users table in the DB
        dicc_label_node[int(H1.node[node]['label'])]=node
      
        if (H1.node[node]['role'] =="R6"):
            list_R6_labels.append(int(H1.node[node]['label']))# this actually corresponds to the id from the users table in the DB


    #print "# R6s:",len(list_R6_labels)
    
    print len(dicc_label_node)

    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"

    db= Connection(server, database, user, passwd) 


    query1="""select * from users"""    
    result1 = db.query(query1)  # is a list of dict.



    name1="GINI_coef_friendships_strenght_friendship_with_R6s.csv"           
    file=open(name1, 'wt')   
    print >> file,'label','ck_id','gini_friendships','gini_to_friends','gini_from_friends','sum_strength_with_R6s','sum_strength_to_R6s','sum_strength_from_R6s','tot_mess','tot_sent','tot_received'



 


    dicc_ck_label={}
    for r1 in result1:   #first i build a dicc ck_id vs. label        
      ck_id=r1['ck_id']      
      label=int(r1['id'])  # this corresponds to the 'label' in the gml files
      dicc_ck_label[ck_id]=label

      try:
          node=dicc_label_node[label]
          H1.node[node]['ck_id']=ck_id        
      except KeyError: pass

   



    num_users=0.
    for r1 in result1:   #loop over users 
      num_users+=1.
     
      print int(num_users)
      ck_id=r1['ck_id']
      label=int(r1['id'])  # this corresponds to the 'label' in the gml files
      try:
          node=dicc_label_node[label]
      except KeyError: pass

      query2="select  * from friends where (src ='"+str(ck_id)+"')or (dest ='"+str(ck_id)+"') "
      result2= db.query(query2)          
      degree=len(result2)           




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
      
      list_weighted_to_friends_R6s=[]  
      list_weighted_from_friends_R6s=[]
      list_weighted_tot_messg_friends_R6s=[]
  
      list_weighted_to_friends_R6s_norm=[]  
      list_weighted_from_friends_R6s_norm=[]
      list_weighted_tot_messg_friends_R6s_norm=[]




      query3="select  * from private_messages where (src_id ='"+str(ck_id)+"') "  
      result3= db.query(query3)
      tot_sent=float(len(result3))
      
      query4="select  * from private_messages where  (dest_id ='"+str(ck_id)+"') "   
      result4= db.query(query4)
      tot_received=float(len(result4))
      
      query5="select  * from private_messages where (src_id ='"+str(ck_id)+"')or (dest_id ='"+str(ck_id)+"') "   # all messages
      result5= db.query(query5)
      num_tot_messg=float(len(result5))
      

      # if num_users <=500:    # JUST TO TEST THE CODE

      if label in list_network_ids:  # if the user is in the network, i check how many messages they send each other
             
          print "\n\nnode label",label,ck_id,"has degree:",H1.degree(node),"from DB",degree

         

   
          for f in H1.neighbors(node):
             
              messg_to_one_friend=0.    #looking at a particular friend
              messg_from_one_friend=0.
              messg_one_friend=0.

      
              from_R6s=0.
              to_R6s=0.
              with_R6s=0.


              flag_R6_friend=0
              flag_to_R6=0
              flag_from_R6=0

              for r5 in result5:
                
                  if r5['src_id']== ck_id   and   r5['dest_id']== H1.node[f]['ck_id']:                      
                      num_messg_to_friends+=1.
                      num_messg_friends+=1.
                      flag_sent=1

                      messg_to_one_friend+=1.
                      messg_one_friend+=1.

                      if H1.node[f]['role']=='R6':
                          if H1.node[node]['R6_overlap'] >0:
                              to_R6s+=1.                              
                              with_R6s+=1.  
                              flag_R6_friend=1
                              flag_to_R6=1
                            


   

                  elif r5['dest_id']== ck_id   and   r5['src_id']== H1.node[f]['ck_id']:                      
                      num_messg_from_friends+=1.
                      num_messg_friends+=1.
                      flag_received=1

                      messg_from_one_friend+=1.
                      messg_one_friend+=1.

                      if H1.node[f]['role']=='R6':
                          if H1.node[node]['R6_overlap'] >0:
                              from_R6s+=1.                                   
                              with_R6s+=1.     
                              flag_R6_friend=1                              
                              flag_from_R6=1


           
              list_weighted_to_friends.append(messg_to_one_friend)    # weight of each friendship    (not normalized)          
              list_weighted_from_friends.append(messg_from_one_friend)                                     
              list_weighted_tot_messg_friends.append(messg_one_friend) 



             
              if flag_to_R6!=0:
                  list_weighted_to_friends_R6s.append(to_R6s) 
                 
              if flag_from_R6!=0:
                  list_weighted_from_friends_R6s.append(from_R6s) 
                  
              if flag_R6_friend !=0:
                  list_weighted_tot_messg_friends_R6s.append(with_R6s)
  



          for item in list_weighted_tot_messg_friends:    # normalization
              if sum(list_weighted_tot_messg_friends)>0:
                  list_weighted_tot_messg_friends_norm.append(item/sum(list_weighted_tot_messg_friends))

          for item in list_weighted_to_friends:
              if sum(list_weighted_to_friends)>0:
                  list_weighted_to_friends_norm.append(item/sum(list_weighted_to_friends))

          for item in list_weighted_from_friends:
               if sum(list_weighted_from_friends)>0:
                   list_weighted_from_friends_norm.append(item/sum(list_weighted_from_friends))



          for item in list_weighted_tot_messg_friends_R6s:    # normalization
              if sum(list_weighted_tot_messg_friends)>0:
                  list_weighted_tot_messg_friends_R6s_norm.append(item/sum(list_weighted_tot_messg_friends))

          for item in list_weighted_to_friends_R6s:
              if sum(list_weighted_to_friends)>0:
                  list_weighted_to_friends_R6s_norm.append(item/sum(list_weighted_to_friends))

          for item in list_weighted_from_friends_R6s:
               if sum(list_weighted_from_friends)>0:
                   list_weighted_from_friends_R6s_norm.append(item/sum(list_weighted_from_friends))





     # i calculate how skewed friendships for a given user are:
          if len(list_weighted_to_friends) >0 and sum(list_weighted_to_friends)>0:
              Gini_to_friends=GINI_coef.calculate_GINI(list_weighted_to_friends)            
          else:
              Gini_to_friends='NA'

          if len(list_weighted_from_friends) >0 and sum(list_weighted_from_friends)>0:
              Gini_from_friends=GINI_coef.calculate_GINI(list_weighted_from_friends)  
          else:                   
              Gini_from_friends='NA'

          if len(list_weighted_tot_messg_friends) >0 and sum(list_weighted_tot_messg_friends)>0:
              Gini_friends=GINI_coef.calculate_GINI(list_weighted_tot_messg_friends)
          else:
              Gini_friends='NA'
        




          print >> file,label,ck_id,Gini_friends,Gini_to_friends,Gini_from_friends,sum(list_weighted_tot_messg_friends_R6s_norm),sum(list_weighted_to_friends_R6s_norm),sum(list_weighted_from_friends_R6s_norm),num_tot_messg,tot_sent,tot_received

          print label,ck_id,"tot:",Gini_friends,list_weighted_tot_messg_friends_norm,sum(list_weighted_tot_messg_friends),"\n  to:",Gini_to_friends,list_weighted_to_friends_norm,sum(list_weighted_to_friends),"\n  from:",Gini_from_friends,list_weighted_from_friends_norm,sum(list_weighted_from_friends),"\n  with R6s","(R6overlap",H1.node[node]['R6_overlap'],"):",list_weighted_tot_messg_friends_R6s_norm,sum(list_weighted_tot_messg_friends_R6s_norm),"to:",list_weighted_to_friends_R6s_norm,sum(list_weighted_to_friends_R6s_norm),"from:",list_weighted_from_friends_R6s_norm,sum(list_weighted_from_friends_R6s_norm)
         # if H1.node[node]['R6_overlap'] !=0:
          #    raw_input()


            
      else :  #if not networked node (or not GC)
          print >> file,label,ck_id,'NA','NA','NA','NA','NA','NA',num_tot_messg,tot_sent,tot_received



################################################

          
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename1 = sys.argv[1]
       

        main(graph_filename1)
    else:
        print "usage: python  whatever.py   path/network_file2_R6s_info.gml  "
 
     

##############################################
