#!/usr/bin/env python
# encoding: utf-8
"""
initial_activity_rate.py

Created by Rufaro Mukogo on 2011-07-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script generates a distribution of the activity of two populations of users within the first n days in the system. 
This script was written in support of the figure which shows that we have two popultaions with different decay 
constants: "high attrition" and "low attrition"

"""

import sys
import os
from database import *
import datetime
import time
from time import strptime
from datetime import *
from dateutil.relativedelta import *
from empirical_cdf_class import *
import pylab
from look_up_table import *

look_up = look_up_table()

class initial_activity:

    def __init__(self,infile, outdir, filename, cut_off, server="tarraco.chem-eng.northwestern.edu",\
            database = "calorie_king_social_networking_2010",\
            user="calorieking", passwd="n1ckuDB!"):
        
        self.uids = [x.strip("").split(",")[1] for x in open(str(infile)).readlines()[1:]]
        
        self.uids = map(lambda x: x.strip('""'), self.uids)
        self.uids = map(str, self.uids)

        print len(self.uids)

        self.db = Connection(server, database, user, passwd)      
        self.infile = infile
        self.outdir = outdir
        self.filename = filename
        self.cut_off = cut_off
        self.count = False


    def get_candidates(self):
        """function returns a tuple (ck_id,join_date + cutoff)"""
        
        candidates = []
        for uid in self.uids:
            try:
                result = self.db.query("SELECT ck_id,id,join_date FROM users WHERE ck_id='"+str(uid)+"'")
                #print len(result)
                d = datetime(*strptime(str(result[0]['join_date']), "%Y-%m-%d %H:%M:%S")[0:6]) + relativedelta(days =\
                self.cut_off)
                e = datetime(*strptime(str(result[0]['join_date']), "%Y-%m-%d %H:%M:%S")[0:6])
            
                delta = 0.001
                assert  abs((e-d).days) <= (self.cut_off + delta), 'Bad delta -- %f' % (e-d)
                
            except IndexError: pass

            candidates.append((result[0]['ck_id'],result[0]['join_date'],str(d),look_up["time_in_system"][int(float(result[0]['id']))]))
            #print "dates", d       
        print "check candidates", len(candidates)

        return candidates
    def get_activity_count(self,n):
        """function to count the activity of a user in the first n days in the system"""
        
        uid = n[0]
        cutoff_date = n[2]
        join_date = n[1]
        

        if not self.count:


            act_days = self.db.query("SELECT COUNT(DISTINCT activity_date) FROM activity_combined where\
            ck_id='"+str(uid)+"'AND activity_date < '"+str(cutoff_date)+"' AND activity_date\
            >='"+str(join_date)+"'")

            key = act_days[0].keys()[0]
            t = int(act_days[0][key])

        else:

            act_count = self.db.query("SELECT COUNT(*) FROM activity_combined where\
              ck_id='"+str(uid)+"'AND activity_date < '"+str(cutoff_date)+"' AND activity_date\
              >='"+str(join_date)+"'")

            key = act_count[0].keys()[0]
            t   = int(act_count[0][key])


        return t  

        
    def main(self): 
        candidates = self.get_candidates()
        activity_counts = []
        f = open("./method3_50/interim/counts_for_"+str(self.filename)+".csv","w")
        print>>f, ",".join(map(str,["activity_count","ck_id","join_date","cutoff_date",\
        "time in system"]))

        for n in candidates:
            t = self.get_activity_count(n)
            print>>f, ",".join(map(str,(t,n[0],n[1],n[2],n[3])))
            activity_counts.append(t)
        
        f.close()
        
        plotcdf = EmpiricalCDF(activity_counts, self.outdir,self.filename,y_axis = "cumulative\
        distribution density",x_axis = "activity (n)")
        data = plotcdf.cdf_data()
        plotcdf.cdf_plotting()
        
        g = open("./method3_50/interim/"+str(self.filename)+"_plot_data.dat","w")

        for n in data:
            print>>g, " ".join(map(str,n))

        g.close()
        
        print "max actvity in %d days for %s: %g" %(self.cut_off,self.filename, max(activity_counts)) 

if __name__=="__main__":
    
    try:
        import psycho
        psycho.full()
    except ImportError:
        pass

    if len(sys.argv) > 1:
        infile = sys.argv[1]
        
    if len(sys.argv) > 2:
        outdir = sys.argv[2]

    if len(sys.argv) > 3:
        filename = sys.argv[3]

    if len(sys.argv) > 4:
        cut_off = sys.argv[4]
    else:
        cut_off = 50
        
    obj = initial_activity(infile, outdir, filename, cut_off)
    obj.main()
