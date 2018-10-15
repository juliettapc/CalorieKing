#!/usr/bin/env python
# encoding: utf-8
"""
candidate_users.py

Created by Daniel McClary on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script generates a csv of all users with n or more weigh-ins in the CK database.  When run with a year as the trailing argument,
the number of weigh-ins must occur in that year (only 2009 is currently supported). 
"""

import sys
import os
from database import *
import datetime
import time
from datetime import date

TIME_FORMAT='%Y-%m-%d'

def get_weigh_in_uids(num_points, db, restrict):
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

def get_activity_history(uid, db, inc_weigh_ins, year_restrict=None):
    
    if inc_weigh_ins:
        q = "SELECT act.activity_date, act.activity_flag FROM activity_combined as act WHERE ck_id = '"+uid+"'"   
    else: 
        q = "SELECT act.activity_date, act.activity_flag FROM activity_combined as act WHERE ck_id = '"+uid+"' and activity_flag <> 'WI'"   

    activity_history = []
    
    result = db.query(q)

    for r in result:
        activity_history.append(",".join(map(str, [uid, r['activity_date'],r['activity_flag']])))
        activity_history.sort()
    
    
    return activity_history

def get_weigh_in_history(uid, db, restrict):
    if restrict:
        q = "SELECT weight, on_day FROM weigh_in_history WHERE ck_id = '"+uid+"' AND on_day >= '2009-01-01' ORDER BY on_day ASC"
        q2 = "SELECT join_date FROM users WHERE ck_id = '"+uid+"'"
        
    else:
        q = "SELECT weight, on_day FROM weigh_in_history WHERE ck_id = '"+uid+"' ORDER BY on_day ASC"
        q2 = "SELECT join_date FROM users WHERE ck_id = '"+uid+"'"
        
    history = []
    join_dates = []
    result= db.query(q)
    result2 = db.query(q2) 

    for r in result:
        history.append(",".join(map(str, [r['weight'], r['on_day']])))
    
    for r2 in result2:
        join_dates.append(",".join(map(str, [r2['join_date']])))

    #print join_dates[-1]
        
    return history, join_dates

def demographic_history(uid, db, restrict):
    """query to extract height, state, and age if provided"""

    demos = db.query("SELECT u.age, u.height, u.state from users AS u WHERE ck_id ='"+str(uid)+"'")
    demographics = []

    for d in demos:
        try:
            demographics.append(",".join(map(str,[d['age'],d['height'],d['state']])))
        except IndexError:pass
    #print "demographics", demographics

    return demographics


def main(num_points, inc_weigh_ins, year_restrict=None)
     
    uids = get_weigh_in_uids(num_points, db, year_restrict)

    #save candidates to disk for other tasks
    if year_restrict:
        
        f = open("./"+str(num_points)+"_points_network_2010/data/"+str(year_restrict)+\
                "_weigh_in_candidates_with_"+str(num_points)+"_total_points.dat", "w")
    else:
        f = open("./"+str(num_points)+"_points_network_2010/data/weigh_in_candidates_with_"\
                +str(num_points)+"_total_points.dat", "w")

    print >> f, '"id","ck_id","number_of_weigh_ins"'
    
    for uid in uids:
        print >> f, ",".join(uid)
    f.close()
    
    #get the time-series with for the candidates
    if year_restrict:
        try:
            os.mkdir("./"+str(num_points)+"_points_network_2010/data/candidate_attributes_with_"+str(num_points)+"_"+str(year_restrict))
        except OSError:
            pass
        dirname = "./"+str(num_points)+"_points_network_2010/data/candidate_attributes_with_"+str(num_points)+"_"+str(year_restrict)
    else:
        try:
            os.mkdir("./"+str(num_points)+"_points_network_2010/data/candidate_attributes_with_"+str(num_points))
        except OSError:
            pass
        dirname = "./"+str(num_points)+"_points_network_2010/data/candidate_attributes_with_"+str(num_points)
            
    total_changes = []
    
    print "dirname", dirname

    for uid in uids:

        history, join_dates = get_weigh_in_history(uid[1], db, year_restrict)
        activity = get_activity_history(uid[1], db, inc_weigh_ins, year_restrict)
        demographics = demographic_history(uid[1], db, year_restrict)

        f = open(dirname+"/activity_history_for_user_"+str(uid[0])+".dat", "w")
        print >> f, '"activity","date"'
        
        for h in history:
            print >> f, h
        f.close()
        
        aggregate_change = float(history[-1].split(",")[0]) - float(history[0].split(",")[0])
        start_weight = float(history[0].split(",")[0])
        
        age = int(demographics[0].split(",")[0])
        height = int(demographics[0].split(",")[1])
        state = str(demographics[0].split(",")[2])
        initial_BMI = float(float(start_weight)*703.0)/float(height)**2
        final_BMI = float(float(history[-1].split(",")[0])*703.0)/float(height)**2

        join_time = time.strptime(join_dates[0].split()[0],TIME_FORMAT)
        starting_time = time.strptime(history[0].split(",")[1].split()[0], TIME_FORMAT)
        ending_time = time.strptime(history[-1].split(",")[1].split()[0], TIME_FORMAT)
        start_date = date(*starting_time[:3])

        end_date = date(*ending_time[:3])
        aggregate_duration = (end_date - start_date).days
        
        act_starting_time = time.strptime(activity[0].split(",")[1], TIME_FORMAT)
        act_ending_time = time.strptime(activity[-1].split(",")[1], TIME_FORMAT)
        act_start_date = date(*starting_time[:3])
        act_end_date = date(*ending_time[:3])
        
        join_date = date(*join_time[:3])
        time_in_sys = (act_end_date - join_date).days

        last_day = datetime.date(2011,2,23)

        try:
          n_weight_change = float(aggregate_change)/float(aggregate_duration)
        except ZeroDivisionError:
          n_weight_change =  "NA"

        aggregate_change_tuple = uid + [start_weight, aggregate_change, aggregate_duration,\
                                       n_weight_change,float(aggregate_change)*100/float(start_weight),\
                                        time_in_sys]+[height,age,initial_BMI,final_BMI,(final_BMI-initial_BMI),act_end_date,(last_day-act_end_date).days]
        
        total_changes.append(aggregate_change_tuple)
        
    g = open(dirname+"/"+str(num_points)+"_point_users_attribute_data_"+str(num_points)+"_points.dat", "w")
    
    print "dirname", dirname
    
    print>>g, '"id", "ck_id", "weigh_ins", "initial_weight", "weight_change",\
            "days","n_weight_change", "percentage_weight_change", "time_in_system", "height", "age", "initial_BMI", "final_BMI", "change_in_BMI","last_day_of_act", "days_since_last_act"'
    
    
    for t in total_changes:
        print >> g, ",".join(map(str, t))
    g.close()

if __name__ == '__main__':
    
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass
    
    if len(sys.argv) > 1:
        number_of_weightpoints = int(sys.argv[1])
    else:
        number_of_weightpoints = 10
    restrict = None
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
    else:
        restrict = None

    #    if year == 2009:
    #        restrict = 2009
    #        print "year restricted to 2009"
    
    main(num_points=number_of_weightpoints, inc_weigh_ins=True, year_restrict=None)

