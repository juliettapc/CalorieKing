#! /usr/bin/env python

"""
Created by Julia Poncela on March 2011



It doesnt take any arguments.

"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import *
import math
from pylab import *
import numpy
import networkx as nx


def main ():



    name0="5_points_network_2010/data/percentage_activity_R6s.dat"
    file0=open(name0, 'wt')   
    file0.close()
    

    name1="5_points_network_2010/data/cum_percentage_activity_R6s.dat"
    file1=open(name1, 'wt')   
    file1.close()
   

    name2="5_points_network_2010/data/cum_percentage_activity_neighbors_R6s.dat"
    file2=open(name2, 'wt')   
    file2.close()
   




 
    database = "calorie_king_social_networking_2010"  #the old data was:  calorie_king_social_networking
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"


    db= Connection(server, database, user, passwd)  #abro la base de datos




    graph_name="5_points_network_2010/data/friend_graph_all.gml"
    G = nx.read_gml(graph_name)





    list_number_BC=[]  # to accumulate over the 10 R6s
    list_number_WI=[]
    list_number_PM=[]
    list_number_FP=[]
    list_number_HP=[]
    list_number_LC=[]


  

    cont=0 
    for node in G.nodes():
        try:
            if G.node[node]['role']=='R6':  
                cont=cont+1
                label=G.node[node]['label']              
                
                R6_label=G.node[node]['label']   


                #  analysis for the R6:

                result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
                
                ck_id=result1[0]['ck_id']  # i get the R6's  ck_id



               

                result2=db.query("select * from activity_combined where (ck_id='"+str(ck_id)+"')") #list of dict: [{'ck_id':  ,'activity_date': , 'activity_flag':  },{'ck_id':  ,'activity_date': , 'activity_flag':  },{... },...]  # i get the R6's activities


                number_BC=0.0
                number_WI=0.0
                number_PM=0.0
                number_FP=0.0
                number_HP=0.0
                number_LC=0.0

                
                print G.node[node]['label'],len(result2),len(G.neighbors(node))


                for row in result2:
                    if row['activity_flag']=='BC':
                        number_BC=number_BC+1
                    elif row['activity_flag']=='WI':
                        number_WI=number_WI+1
                    elif row['activity_flag']=='PM':
                        number_PM=number_PM+1
                    elif row['activity_flag']=='FP':
                        number_FP=number_FP+1
                    elif row['activity_flag']=='HP':
                        number_HP=number_HP+1
                    elif row['activity_flag']=='LC':
                        number_LC=number_LC+1



                total_act=number_BC+number_WI+number_PM+number_FP+number_HP+number_LC
                number_BC=number_BC/total_act
                number_WI=number_WI/total_act
                number_PM=number_PM/total_act
                number_FP=number_FP/total_act
                number_HP=number_HP/total_act
                number_LC=number_LC/total_act


                
                list_cum=[number_BC,number_WI,number_PM,number_FP,number_HP,number_LC]



                list_number_BC.append(number_BC)
                list_number_WI.append(number_WI)
                list_number_PM.append(number_PM)
                list_number_FP.append(number_FP)
                list_number_HP.append(number_HP)
                list_number_LC.append(number_LC)
    



               
                file0=open(name0, 'at')
                print >> file0,cont, label,"BC:",number_BC," WI:",number_WI," PM:",number_PM," FP:",number_FP," HP:",number_HP," LC:",number_LC, "tot:",total_act
                file0.close()
                


                sum=0.0
                file1=open(name1, 'at')
                print >> file1,"\n",cont, label,
                for i in range(len(list_cum)):
                    sum=sum+list_cum[i]                  
                    print >> file1,sum,                
                file1.close()







                #################################
                # now analysis for the neighbors of the R6:
  
                list_number_BC_neighb=[] # to accumulate over all neighbors of the all 10 R6s
                list_number_WI_neighb=[]
                list_number_PM_neighb=[]
                list_number_FP_neighb=[]
                list_number_HP_neighb=[]
                list_number_LC_neighb=[]
    


               
                for neighbor in G.neighbors(node):

                    label=G.node[neighbor]['label']                                           
                    result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
                
                    ck_id=result1[0]['ck_id']  # i get the neighbor's  ck_id               
                    result2=db.query("select * from activity_combined where (ck_id='"+str(ck_id)+"')") #list of dict: [{'ck_id':  ,'activity_date': , 'activity_flag':  },{'ck_id':  ,'activity_date': , 'activity_flag':  },{... },...]  # i get the R6's activities




                    number_BC=0.0
                    number_WI=0.0
                    number_PM=0.0
                    number_FP=0.0
                    number_HP=0.0
                    number_LC=0.0


                    for row in result2:
                        if row['activity_flag']=='BC':
                            number_BC=number_BC+1
                        elif row['activity_flag']=='WI':
                            number_WI=number_WI+1
                        elif row['activity_flag']=='PM':
                            number_PM=number_PM+1
                        elif row['activity_flag']=='FP':
                            number_FP=number_FP+1
                        elif row['activity_flag']=='HP':
                            number_HP=number_HP+1
                        elif row['activity_flag']=='LC':
                            number_LC=number_LC+1



                    total_act=number_BC+number_WI+number_PM+number_FP+number_HP+number_LC
                    number_BC=number_BC/total_act
                    number_WI=number_WI/total_act
                    number_PM=number_PM/total_act
                    number_FP=number_FP/total_act
                    number_HP=number_HP/total_act
                    number_LC=number_LC/total_act #fractions of activity for a single neighbor of a given R6
                    



                    list_number_BC_neighb.append(number_BC) # accumulate over all neighbors of an R6
                    list_number_WI_neighb.append(number_WI)
                    list_number_PM_neighb.append(number_PM)
                    list_number_FP_neighb.append(number_FP)
                    list_number_HP_neighb.append(number_HP)
                    list_number_LC_neighb.append(number_LC)
    




                
                list_cum=[numpy.mean(list_number_BC_neighb),numpy.mean(list_number_WI_neighb),numpy.mean(list_number_PM_neighb),numpy.mean(list_number_FP_neighb),numpy.mean(list_number_HP_neighb),numpy.mean(list_number_LC_neighb)]   # average over all neighbors of a given R6

                   

                sum=0.0
                file2=open(name2, 'at')
                print >> file2,"\n",cont, R6_label,
                for i in range(len(list_cum)):
                    sum=sum+list_cum[i]                   
                    print >> file2,sum,                
                                       
                print >> file2,len(G.neighbors(node))
                file2.close()
                               
        except KeyError: pass  # to skip nodes not belonging to the GC (cos dont have a role)







#average over the R6s:

    file0=open(name0, 'at')
    print >> file0,"\n\n", "BC:",numpy.mean(list_number_BC),numpy.std(list_number_BC), "WI:",numpy.mean(list_number_WI),numpy.std(list_number_WI), "PM:",numpy.mean(list_number_PM),numpy.std(list_number_PM), "FP:",numpy.mean(list_number_FP),numpy.std(list_number_FP), "HP:",numpy.mean(list_number_HP),numpy.std(list_number_HP), "LC:",numpy.mean(list_number_LC),numpy.std(list_number_LC)
    file0.close()
    



#########################
      
        



if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass
