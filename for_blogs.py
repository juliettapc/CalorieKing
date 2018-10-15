

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




# blogs where only owner-poster share a link:

#def query_blogs_all_to_all (self, duration=None):


def perm(seq):
    
    combination = []
    
    for i in range(len(seq)):
        for j in range(i,len(seq)):
            
            if seq[i]==seq[j]:
                pass
            else:
                combination.append((seq[i],seq[j]))
    
    #print "combination", combination
    return combination

if __name__=="__main__":
    pass    






master_query="""select distinct bc.poster_id, bc.owner_id from blog_comments as bc, users as u where (bc.poster_id = u.ck_id)"""

queries_to_run =[master_query]
    
for query in queries_to_run:
    result = db.query(query) #[{'poster_id': ,'owner_id': },{'poster_id': ,'owner_id': },{'poster_id': ,'owner_id': },...]


    owner_list=[]
    for r in result:
        owner=result[0]['owner_id']

        if owner not in owner_list:
            owner_list.append(owner)
             
            print str(owner)
            result1=db.query("select distinct bc.poster_id from blog_comments as bc where bc.owner_id ='"+str(owner)+"'")  # i select all distint poster of a same owner: list of dict: [{'poster_id': },{'poster_id':  },{'poster_id': },...]
            print result1

            members=[]  # nodes that will connect all-to-all
            members.append(owner)

            for r1 in result1:
                poster=r1['poster_id']
                members.append(poster)

        print members





        edges=perm(members)
        G=nx.Graph()
        G.add_edges_from(edges)






exit()


##########################################



# blogs where only owner-poster share a link:

#def query_blogs_couples (self, duration=None):


master_query="""select distinct bc.poster_id, bc.owner_id from blog_comments as bc, users as u where (bc.poster_id = u.ck_id)"""

queries_to_run =[master_query]
    
for query in queries_to_run:
    result = db.query(query) #[{'poster_id': ,'owner_id': },{'poster_id': ,'owner_id': },{'poster_id': ,'owner_id': },...]


    edges=[]
    for r in result:
        source=r['poster_id']
        destination=r['owner_id']  #convert from ck_id to uid:

        result1=db.query("select id from users where (ck_id ='"+str(source)+"')")
        result2=db.query("select id from users where (ck_id ='"+str(destination)+"')")

        try: #just in case any of them is a ghost user                         
            couple=(result1[0]['id'],result2[0]['id']) #these lists only have one element,
                 # at the most, and it is  a dictionary with 'id' as only key      

            edges.append(couple)            

        except IndexError: pass

G=nx.Graph()
G.add_edges_from(edges)
    
print len(G.nodes()),len(G.edges()) #=295, 655






##########################################

#private messages:
#def query_private_messages (self, duration=None):

master_query="""select distinct pm.src_id, pm.dest_id from private_messages as pm, users as u where (pm.src_id = u.ck_id)"""

queries_to_run =[master_query]
    
for query in queries_to_run:
    result = db.query(query) #[{'src_id': ,'dest_id': },{'src_id': ,'dest_id': },{'src_id': ,'dest_id': },...]

    edges=[]
    for r in result:
        source=r['src_id']
        destination=r['dest_id']

        result1=db.query("select id from users where (ck_id ='"+str(source)+"')")
        result2=db.query("select id from users where (ck_id ='"+str(destination)+"')")

        try: #just in case any of them is a ghost user                         
            couple=(result1[0]['id'],result2[0]['id'])  

            edges.append(couple)            

        except IndexError: pass

G.add_edges_from(edges)
    
print len(G.nodes()),len(G.edges()) #=939, 1484



##########################################
