#! /usr/bin/env python

"""
Created by Julia Poncela on February 2011.

For now, just playing around with CK database: extracting and printing out
some info.

"""



import sys
import os
from database import *   #codigo para manejar bases de datos
from datetime import date


database = "calorie_king_social_networking"
server="tarraco.chem-eng.northwestern.edu"
user="calorieking" 
passwd="n1ckuDB!"


db= Connection(server, database, user, passwd)  #abro la base de datos


result = db.query("select poster_id, owner_id, post_date from blog_comments where owner_id ='84848f97-b173-494d-b613-46a68d7c8941'")




print result  # result es una lista de diccionarios, donde las keys siempre son los nombres de los campos, y hay un diccionario para cada fila de la tabla correspondiente obtenida para

print result[0] # primer diccionario de la lista

print result[0]['owner_id'] # el valor correspondiente a la key 'owner_id' en el primer diccionario de la lista



#####################################

translation_dicc={}


result = db.query("SELECT id, ck_id FROM users")

list_keys=result[0].keys()
print list_keys


for element in result:
    index1=list_keys[0]
    index2=list_keys[1]
    clave=element[index2]
    valor=int(element[index1])

    translation_dicc[clave]=valor
print translation_dicc
raw_input()

   







for element in ck_id_list_of_dicc: #recorro la lista
    caloriek_id=element['ck_id']
   
    num_weigh_ins=db.query("select count(*) from weigh_in_history where ck_id='"+caloriek_id+"'")

    if num_weigh_ins[0]['count(*)']>=5: # i select the >= 5point individuals

        print num_weigh_ins[0]['count(*)'], type(num_weigh_ins[0]['count(*)'])
        raw_input()






exit()

############################

result2 = db.query("select distinct(owner_id) from blog_comments ")




print result2  # tb es una lista de diccionarios, pero cada uno solo tiene una pareja key-value

exit()


print "imprimo los tres primeros elem de la lista\n"
print result[100]

print "result es del tipo:",type(result)
#print type(result[0])
#print len(result)


r=result[100]


weight_count = db.query("SELECT * FROM weigh_in_history where ck_id='"+str(r['ck_id'])+"'") # asi obtengo una lista de diccionarios. cada dicc corresponde a una ocasion en la que el usuario ha hecho alguna actividad. las keys son su id, la fecha, su peso, ...y los valores, id de cada uno. la longitud del objeto es el numero de veces que ha hecho algo el usuario. ASI NO ES COMO ESTABA EN EL ORIGINAL!



weight_count = db.query("SELECT COUNT(*) FROM weigh_in_history where ck_id='"+str(r['ck_id'])+"'") # asi obtengo una lista de diccionarios pero con un solo elemento. la key es 'COUNT(*)' y el valor es el numero de veces que ha tenido actividad el usuario. la longitud del objeto es uno. ORIGINAL


print "antes:",weight_count, "(tipo:",type(weight_count),")"
print "len",len(weight_count)


weight_count = int(weight_count[0]['COUNT(*)'])

print "weight_count es del tipo:",type(weight_count) #ahora es un entero


print "despues:",weight_count  # es el numero de veces que se ha pesado el usuario


candidates=[]

candidates.append(map(str, [r['id'], r['ck_id'], weight_count]))

uids=candidates[0]#uid es una lista pq candidate es una lista de listas

print uids

uid=uids[1]
print uid

#result= db.query("SELECT activity_date, activity_flag,on_day FROM activity_combined, weigh_in_history WHERE ck_id = '"+uid+"'")




