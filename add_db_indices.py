#!/usr/bin/env python
# encoding: utf-8
"""
add_db_indices.py

Created by Daniel McClary on 2010-12-21.
Copyright (c) 2010 __Northwestern University. All rights reserved.

This short script simply adds auto-incrementing integer indeces to all tables in a database.

"""

import sys
import os
import string
from database import *

def get_table_names(db):
    tables = db.query("SHOW TABLES")
    table_names = []
    for t in tables:
        names = map(str, t.values())
        table_names.append(names[0])
    return table_names
    
def make_ids(db, table):
    #check to see if id exists
    result = db.query("DESCRIBE "+ table)
    has_id = False
    if result:
        for r in result:
            if r['Field'] == u'id':
                print "has id"
                has_id = True
    if not has_id:
        try:
            db.execute("ALTER TABLE "+table+" ADD COLUMN id INTEGER AUTO_INCREMENT UNIQUE KEY")
        except TypeError as e:
            print table
            print e
            pass
        
def identify_db(server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
    database = "calorie_king_social_networking_2010"
    db = Connection(server, database, user, passwd)
    tables = get_table_names(db)
    for t in tables:
        make_ids(db, t)

if __name__ == '__main__':
	identify_db()

