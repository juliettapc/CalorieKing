"""
candidate_activity2.py

Created by Rufaro Mukogo on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script generates activity logs based on forum and blog posts for all users in the CK database.

"""

import sys
import os
from database import *
from datetime import date

TIME_FORMAT='%Y-%m-%d'

def get_activity_in_uids(num_points, db, restrict):
    #get all uids
    result = db.query("SELECT id, ck_id FROM users")
    candidates = []
    for r in result:
        #get the number of weigh-in points
        if restrict:
            weight_count = db.query("SELECT COUNT(*) FROM weigh_in_history where ck_id='"+str(r['ck_id'])+"' AND on_day >= '2009-01-01'")
        else:
            weight_count = db.query("SELECT COUNT(*) FROM weigh_in_history where ck_id='"+str(r['ck_id'])+"'")
        weight_count = int(weight_count[0]['COUNT(*)'])
        
        
        if weight_count >= num_points:
            candidates.append(map(str, [r['id'], r['ck_id'], weight_count]))
    return candidates

def get_activity_history(uid, db, year_restrict=None):
	
    q = "SELECT activity_date FROM activity_log WHERE ck_id = '"+uid+"'"   
    
    activity_history = []
    result= db.query(q)

    for r in result:
        activity_history.append(",".join(map(str, [uid, r['activity_date']])))
        activity_history.sort()

    return activity_history
	
	
def main(num_points, year_restrict=None, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
    print "building time series with " + str(num_points) + " required datapoints"
    database = "calorie_king_social_networking"
    db = Connection(server, database, user, passwd)
    uids = get_activity_in_uids(num_points, db, year_restrict)
    #save candidates to disk for other tasks
    if year_restrict:
        f = open(str(year_restrict) + "_activity_in_candidates_with_"+str(num_points)+"_total_points.dat", "w")
    else:
        f = open("activity_in_candidates_with_"+str(num_points)+"_total_points.dat", "w")
    print >> f, '"id","ck_id","number_of_weigh_ins"'
    
    for uid in uids:
        print >> f, ",".join(uid)
    f.close()
    
    #get the activities for the candidates
    
    if year_restrict:
        try:
            os.mkdir("candidate_activity_with_"+str(num_points)+"_"+str(year_restrict))
        except OSError:
            pass
        dirname = "candidate_activity_with_"+str(num_points)+"_"+str(year_restrict)
    else:
        try:
            os.mkdir("candidate_activity_with_"+str(num_points))
        except OSError:
            pass
        dirname = "candidate_activity_with_"+str(num_points)
      
    for uid in uids:
        activity = get_activity_history(uid[1], db, year_restrict)
        
        f = open(dirname+"/activity_history_for_user_"+str(uid[0])+".dat", "w")
        
        print >> f, "%s\t\t\t, %s", (ck_id, date)
        
        for a in activity:
            print a, uid[1] 
            print >>f, a[0],a[1] 
        f.close()
       
if __name__ == '__main__':
    if len(sys.argv) > 1:
        number_of_weightpoints = int(sys.argv[1])
    else:
        number_of_weightpoints = 2
    restrict = None
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
        if year == 2009:
            restrict = 2009
            print "year restricted to 2009"
    
    main(num_points=number_of_weightpoints, year_restrict=restrict)
