from database import *

import itertools

def main(server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
    database = "calorie_king_social_networking_2010"
    db = Connection(server, database, user, passwd)
    
    friends = []
    
    uids = [x.strip().split(",")[1] for x in\
    open("./method3_50/csv/test_adherent_non_engaged_networking.csv").readlines()]

    
    uids = map(lambda x: x.strip('""'), uids)

    print "uids", uids                       
    
    for uid in uids:
    
        try:
            r = db.query("SELECT * from friends WHERE src ='"+str(uid)+"' OR dest='"+str(uid)+"' ")
        except IndexError:
            pass
        
        friends.append(r)
   
    ids = map(len, friends)
   
    print "number of ppl with friends", len(ids)

    id_index = [i for i,e in enumerate(ids) if e!=0]
    
    proper_ids = []

    for i in id_index:
        proper_ids.append(uids[i])

    print "number of users that are adherent, but not engaged", len(proper_ids)

    bad_nodes = []

    for uid in proper_ids:
    
        try:
            r = db.query("SELECT id from users WHERE ck_id ='"+str(uid)+"'")
        except IndexError:
            pass
     
        bad_nodes.append(r)
   

    print "bad nodes", len(bad_nodes) 

if __name__=="__main__":
    main()


