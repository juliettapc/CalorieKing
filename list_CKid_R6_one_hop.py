#! /usr/bin/env python

"""
Created by Julietta PC on April 2011.
Given a .gml file for a network, I get a list of  CK ids (strings of letters and numbers) and connectivity for the R6s, and one-hop R6s neighbors.



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


    name0="5_points_network_2010/data/list_CKids_R6s_k.dat"
    file0=open(name0, 'wt')   
    file0.close()
    

    name1="5_points_network_2010/data/list_CKids_one_hop_from_R6s_k.dat"
    file1=open(name1, 'wt')   
    file1.close()


    name2="5_points_network_2010/data/list_CKids_GC_NON_R6_NON_one_hop_from_R6s_k.dat"
    file2=open(name2, 'wt')   
    file2.close()


    name3="5_points_network_2010/data/list_CKids_nonGC_k.dat"
    file3=open(name3, 'wt')   
    file3.close()






    database = "calorie_king_social_networking_2010"  #the old data was:  calorie_king_social_networking
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"


    db= Connection(server, database, user, passwd)  # open the DB




               
    graph_name="5_points_network_2010/data/friend_graph_all.gml"
    G = nx.read_gml(graph_name)

    
    components=nx.connected_component_subgraphs(G)     
    GC=components[0]




    GC_list=[]
    for i in GC.nodes():      
        GC_list.append(i)

  



    nonGC_list=[]
    for i in G.nodes():
        if i not in GC_list:
            nonGC_list.append(i)



    list_one_hop_CKids=[]
    list_R6s_CKids=[]



    file0=open(name0, 'at')   # i hunt the R6s:
    for node in G.nodes():
        try:
            if G.node[node]['role']=='R6':  
                
                label=G.node[node]['label']              
                
                
                result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
                
                ck_id=result1[0]['ck_id']  # i get the R6's  ck_id

                list_R6s_CKids.append(ck_id)
                
                #print ck_id
                print >> file0,ck_id, len(G.neighbors(node))
                

        except KeyError: pass  # to skip nodes not belonging to the GC (cos dont have a role)


    file0.close()




    list_R6=[]   #list of nodes (not labels, not ckids!)
    list_one_hop_R6=[]    

    dicc_one_hop_CKids={}


    for node in G.nodes():   # i hunt the one-hop-from-R6s nodes:
        try:
            if G.node[node]['role']=='R6': 

                if node not in list_R6:
                    list_R6.append(node)

 
               
                label=G.node[node]['label']              
                              
                result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
                
                ck_id=result1[0]['ck_id']  # i get the R6's  ck_id

               
               # print "R6:", node, "Neighbors:",

                for neighbor in G.neighbors(node):
                   

                    if neighbor not in list_one_hop_R6:
                        list_one_hop_R6.append(neighbor)
                       
                    label=G.node[neighbor]['label']   

                    #print neighbor,
   
                    result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]

                    ck_id=result1[0]['ck_id']  # i get the R6's  neighbors  ck_id
                    
                    if (ck_id not in list_one_hop_CKids) and (ck_id not in list_R6s_CKids ):
                        
                        list_one_hop_CKids.append(ck_id)
                        dicc_one_hop_CKids[ck_id]=len(G.neighbors(neighbor))


               # print "\n"      
                



        except KeyError: pass  # to skip nodes not belonging to the GC (cos dont have a role)



    


    file1=open(name1, 'wt')   
    #for i in list_one_hop_CKids:                    
     #   print >> file1, i   
    for i in dicc_one_hop_CKids:                    
        print >> file1, i,dicc_one_hop_CKids[i]
    file1.close()







    dicc_GC_nonR6_non_one_hop_CKids={}
    list_GC_nonR6_non_one_hop_CKids=[]
 
    for node in GC_list: # i hunt the non  one-hop-from-R6  and non R6 nodes:

        if (node not in list_R6) and (node not in list_one_hop_R6):

            label=G.node[node]['label']      
            result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
            
            ck_id=result1[0]['ck_id']  # i get the R6's  ck_id

            if (ck_id not in list_GC_nonR6_non_one_hop_CKids):
                list_GC_nonR6_non_one_hop_CKids.append(ck_id)
                dicc_GC_nonR6_non_one_hop_CKids[ck_id]=len(G.neighbors(node))



    file2=open(name2, 'wt')   
    #for i in list_GC_nonR6_non_one_hop_CKids:                    
     #   print >> file2, i             
    for i in dicc_GC_nonR6_non_one_hop_CKids:                    
        print >> file2, i , dicc_GC_nonR6_non_one_hop_CKids[i]           

    file2.close()




    dicc_nonGC_CKids={}
    nonGC_list_CKids=[]

    for node in nonGC_list: # i hunt the nonGC nodes:

        label=G.node[node]['label']      
        result1=db.query("select ck_id from users where (id='"+str(label)+"')") #list of dict: [{'ck_id':  }]
            
        ck_id=result1[0]['ck_id']  # i get the R6's  ck_id

        if (ck_id not in nonGC_list_CKids):
            nonGC_list_CKids.append(ck_id)
            dicc_nonGC_CKids[ck_id]=len(G.neighbors(node))





    file3=open(name3, 'wt')   
  #  for i in nonGC_list_CKids:                    
   #     print >> file3, i    
    for i in dicc_nonGC_CKids:                    
        print >> file3, i , dicc_nonGC_CKids[i]
    file3.close()






    print  "GC:",len (GC_list)
    print "   one_hop:",len(dicc_one_hop_CKids)
    print "   R6:", len(list_R6s_CKids)
    print "   nonR6+non_one_hop:",len(dicc_GC_nonR6_non_one_hop_CKids)   
    print "nonGC:",len(dicc_nonGC_CKids)


#########################
      
        



if __name__== "__main__":
   
    main()
