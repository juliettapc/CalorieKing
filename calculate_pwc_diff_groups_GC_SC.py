#!/usr/bin/env python



"""
Created by Julia Poncela on November 2011.

Given a network and the corresponding csv file for networked & non-networked people,
it caluculates the average pwc  and standard deviation for different sets: all, non-networked, networked, GC, SmallClusters
and also the fraction of people in each set that reaches the -5% wc

"""

import sys
import os
import networkx as nx
import numpy
import csv



def main(graph_name):
  
    H = nx.read_gml(graph_name)

    print "initial network size:",len(H.nodes())


    for node in H.nodes():    # remove selploops 
        if node in H.neighbors(node):
            H.remove_edge(node,node)
            


    for node in H.nodes():   # and isolated users as a result of the previous step
        if len(H.neighbors(node))==0:
             H.remove_node(node)
             #print "node",node, "is going down"


   
             
    print "size after removing selfloops:",len(H.nodes())


    GC= nx.connected_component_subgraphs(H)[0]


  


    list_pwc=[]
    list_pwc_GC=[]
    list_pwc_SC=[]

    list_act_network=[]
    list_act_GC=[]
    list_act_SC=[]


    network_5percent=0
    GC_5percent=0
    SC_5percent=0

    for n in H.nodes():

        if H.node[n]["percentage_weight_change"]>-100 and H.node[n]["percentage_weight_change"]<100:  # i remove outlayers
            if H.node[n]["initial_bmi"]>15 and H.node[n]["initial_bmi"]<80 :#  and ( H.node[n]["initial_bmi"]>30 ):   # (and only consider obese)
                if H.node[n]["final_bmi"]>15 and H.node[n]["final_bmi"]<80:



                    if H.node[n]["weigh_ins"]>=2:  # the only restriction is to be able to calculate pwc
                        pwc=float( H.node[n]["percentage_weight_change"])           
                        list_pwc.append(pwc)                        
                        
                        list_act_network.append(float( H.node[n]["activity"]) )


                        if float( H.node[n]["percentage_weight_change"]) < -5:
                            network_5percent+=1
                            

                        if n in GC.nodes():   #GC
                            pwc_GC=float( H.node[n]["percentage_weight_change"])           
                            list_pwc_GC.append(pwc_GC)


                            list_act_GC.append(float( H.node[n]["activity"]) )


                            if float( H.node[n]["percentage_weight_change"]) < -5:
                                GC_5percent+=1

                        else:  #SC
                            pwc_SC=float( H.node[n]["percentage_weight_change"])           
                            list_pwc_SC.append(pwc_SC) 

                            list_act_SC.append(float( H.node[n]["activity"]) )

 
                            if float( H.node[n]["percentage_weight_change"]) < -5:
                                SC_5percent+=1
             

               





    input_name="/home/staff/julia/at_Northwestern/calorieking/calorie_king_hg/network_no_bias/master_csv.csv"  
    resultado= csv.reader(open(input_name, 'rb'), delimiter=',')#, quotechar='"')

#id,ck_id,join_date,initial_weight,most_recent_weight,height,age,weighins,initial_bmi,final_bmi,percentage_weight_change,weight_change,time_in_system,outcome20,outcome50,p_50,act_20,wi_20,p_friend,R6_overlap,degree,friend_avg,activity


    list_pwc_all_2points=[]
    list_pwc_all_2points_no_friends=[]

    list_act_2points=[]
    list_act_2points_no_friends=[]

    all_2points_5percent=0
    all_2points_no_friends_5percent=0

    cont_lines=0
    for row in resultado:        
        if cont_lines>0:

            if float(row[7])>=2:  #at least two points

                if float(row[8])>15 and float(row[8])<80 :#  and ( float(row[8])>30  ):    #i remove outlayers  (and only consider obese)
                    if float(row[9])>15 and float(row[9])<80 :  
                        if float(row[10])>-100 and float(row[10])<100 :  

                            pwc=float(row[10])
                            list_pwc_all_2points.append(pwc) 

                            list_act_2points.append(float(row[22]))

                            if float(row[10]) < -5:
                                all_2points_5percent+=1

                            if  float(row[20])==0:  #no friends
                                list_pwc_all_2points_no_friends.append(pwc)

                                list_act_2points_no_friends.append(float(row[22]))


                                if float(row[10]) < -5:
                                    all_2points_no_friends_5percent+=1



        cont_lines+=1   


    #print  "\n\nonly for obese:"


    print  "pwc network:", numpy.mean(list_pwc),"+ - :",numpy.std(list_pwc), "(size:", len(list_pwc),"users, and", network_5percent/float(len(list_pwc))*100, "achieved <-5% wc )"
    print  "pwc GC:", numpy.mean(list_pwc_GC),"+ - :",numpy.std(list_pwc_GC), "(size:", len(list_pwc_GC),"users, and", GC_5percent/float(len(list_pwc_GC))*100, "achieved <-5% wc )"
    print  "pwc SC:", numpy.mean(list_pwc_SC),"+ - :",numpy.std(list_pwc_SC), "(size:", len(list_pwc_SC),"users, and", SC_5percent/float(len(list_pwc_SC))*100, "achieved <-5% wc )"

    print  "pwc all (2points):", numpy.mean(list_pwc_all_2points),"+ - :",numpy.std(list_pwc_all_2points), "(size:", len(list_pwc_all_2points),"users, and", all_2points_5percent/float(len(list_pwc_all_2points))*100, "achieved <-5% wc )"
    print  "pwc all (2points, NO friends):", numpy.mean(list_pwc_all_2points_no_friends),"+ - :",numpy.std(list_pwc_all_2points_no_friends), "(size:", len(list_pwc_all_2points_no_friends),"users, and", all_2points_no_friends_5percent/float(len(list_pwc_all_2points_no_friends))*100, "achieved <-5% wc )\n\n"





    print "activity networked users:",numpy.mean(list_act_network),"+ - :",numpy.std(list_act_network)
    print "activity GC users:",numpy.mean(list_act_GC),"+ - :",numpy.std(list_act_GC)
    print "activity SC users:",numpy.mean(list_act_SC),"+ - :",numpy.std(list_act_SC)
    print "activity all users:",numpy.mean(list_act_2points),"+ - :",numpy.std(list_act_2points)
    print "activity isolated users:",numpy.mean(list_act_2points_no_friends),"+ - :",numpy.std(list_act_2points_no_friends)










    file=open("network_no_bias/results_pcw_different_sets_GC_SC_so_on.dat",'at')

    print >> file,  "\n\npwc network:", numpy.mean(list_pwc),"+ - :",numpy.std(list_pwc), "(size:", len(list_pwc),"users, and", network_5percent/float(len(list_pwc))*100, "achieved <-5% wc )\n"
    print >> file,  "pwc GC:", numpy.mean(list_pwc_GC),"+ - :",numpy.std(list_pwc_GC), "(size:", len(list_pwc_GC),"users, and", GC_5percent/float(len(list_pwc_GC))*100, "achieved <-5% wc )\n"
    print >> file, "pwc SC:", numpy.mean(list_pwc_SC),"+ - :",numpy.std(list_pwc_SC), "(size:", len(list_pwc_SC),"users, and", SC_5percent/float(len(list_pwc_SC))*100, "achieved <-5% wc )\n"

    print >> file, "pwc all (2points):", numpy.mean(list_pwc_all_2points),"+ - :",numpy.std(list_pwc_all_2points), "(size:", len(list_pwc_all_2points),"users, and", all_2points_5percent/float(len(list_pwc_all_2points))*100, "achieved <-5% wc )\n"
    print >> file, "pwc all (2points, NO friends):", numpy.mean(list_pwc_all_2points_no_friends),"+ - :",numpy.std(list_pwc_all_2points_no_friends), "(size:", len(list_pwc_all_2points_no_friends),"users, and", all_2points_no_friends_5percent/float(len(list_pwc_all_2points_no_friends))*100, "achieved <-5% wc )\n\n"




    print >> file, "activity networked users:",numpy.mean(list_act_network),"+ - :",numpy.std(list_act_network),"\n"
    print >> file, "activity GC users:",numpy.mean(list_act_GC),"+ - :",numpy.std(list_act_GC),"\n"
    print >> file, "activity SC users:",numpy.mean(list_act_SC),"+ - :",numpy.std(list_act_SC),"\n"
    print >> file, "activity all users:",numpy.mean(list_act_2points),"+ - :",numpy.std(list_act_2points),"\n"
    print >> file, "activity isolated users:",numpy.mean(list_act_2points_no_friends),"+ - :",numpy.std(list_act_2points_no_friends),"\n"




    file.close()
            


####################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python program.py path/network_file.gml"
