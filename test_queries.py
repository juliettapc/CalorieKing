from database import *

def main(server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
    database = "calorie_king_social_networking_2010"
    db = Connection(server, database, user, passwd)
    
    friends = []
    
    
    for uid in uids:
    
        try:
            r = db.query("SELECT * from friends AS f WHERE f.ck_id ='"str(uid)+"'")
        except IndexError:
            pass
        
        friends.append(r)
        
    print "results", map(len,friends)
    
if __name__=="__main__":
    main()


