#! /usr/bin/env python

"""
Created by Julia Poncela of February 2011

Create the block-model-like network for the forums of CK, 
where a node (size: number of distinct posters) is a thread and a (weighted) link 
exists between two of them if there is a common poster.


"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import date
import networkx as nx


database = "calorie_king_social_networking"
server="tarraco.chem-eng.northwestern.edu"
user="calorieking" 
passwd="n1ckuDB!"


db= Connection(server, database, user, passwd)  #abro la base de datos


G=nx.Graph()




#def forums (self, duration=None):

master_query="""select distinct fp.thread_id, fp.ck_id from forum_posts as fp"""

queries_to_run =[master_query]
    
for query in queries_to_run:
    result = db.query(query) #[{'thread_id': ,'ck_id': },{'thread_id': ,'ck_id': },{... },...]
    

    thread_list_of_dicc=[] #list of diccionaries [{'thread_id': , 'node_label': , 'members': [],'size': , 'num_posts': }, ...]

    threads=[] #list of keys
    cont=0   #number of threads

    for r in result:
        thread=r['thread_id']
        dicc={}    
        


#OJO! QUITAR LA SEGUNDA CONDICION EN LA VERSION DEFINITIVA!!

        if thread not in threads and len(threads) <= 500:  # if this thread hasnt been counted yet
                
         
            threads.append(thread)

            print len(threads)
             

            dicc['thread_id']=thread
            dicc['node_label']=int(cont)
            


           #count the number of distinct posters in a particular  thread
            result1=db.query("select distinct ck_id, thread_id  from forum_posts as fp where (thread_id ='"+str(thread)+"')") 



            size=len(result1) #number of distinct posters in that thread = size of the node
            dicc['size']=int(size)



            members=[]  # uids of the distinct posters of this thread

            for r1 in result1:

                poster=r1['ck_id']  #convert from ck_id to uid:

                result2=db.query("select id from users where (ck_id ='"+str(poster)+"')") #list of dicc

                try:
                    members.append(result2[0]['id']) #uid of the poster on this thread

                except IndexError: pass # just in case it is a ghost user

 
            dicc['members']=members
            



            result3=db.query("select ck_id, thread_id  from forum_posts as fp where (thread_id ='"+str(thread)+"')")             
            num_posts=len(result3)  # total number of posts in this thread

            dicc['num_posts']=int(num_posts)
                

            
           

            thread_list_of_dicc.append(dicc)

            #print thread_list_of_dicc



            # i add the nodes (with its atributes) to the system:

            G.add_node(cont) #thats the index of the node
            G.node[cont]['node_label']=dicc['node_label']
            G.node[cont]['size']=dicc['size']
            G.node[cont]['members']=dicc['members']
            G.node[cont]['num_posts']=dicc['num_posts']

        

            cont=cont+1



# now i add the links:

# thread_list_of_dicc  is list of diccionaries: [{'thread_id': , 'node_label': , 'members': [],'size': , 'num_posts': }, {}, ...]

    print "creando los links:"    



    #  i create the posible 2element combinatios of dictionaries:

    combination_threads=itertools.combinations(thread_list_of_dicc,2) 
    
   
    counting=0

    for i in combination_threads:# i is a tuple of dictionaries         
        
        print counting
        counting=counting+1

        g=i[0]   #  take separatly the two dictionaries
        j=i[1]

            
        node1=g['node_label']
        node2=j['node_label']
                #print node1, node2
             
               

 # i compare the two  threads, looking for common posters
        for m in g['members']: # loop over the uids of a given thread
            if m in j['members']:                        
                if (node1, node2) not in G.edges():
                            #print 'common uid:',m,'add link:',node1,node2
                    G.add_edge(node1, node2) 
                    G.edge[node1][node2]['weight']=1
                else:
                    G.edge[node1][node2]['weight']=G.edge[node1][node2]['weight']+1

                        #print G.edges(data=True)



    nx.write_gml(G,"Forums_graph_speed_up.gml")
