#! /usr/bin/env python

from database import *
import sys
import os

class DBConnection(object):
    
    def __init__(self, database, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = database
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class CKUser(object):
	
	def __init__(self, user_id, ck_id, height, initial_weight, number_of_weigh_ins, latest_weight):
		self.user_id = user_id
		self.ck_id = ck_id
		self.height = height
		self.number_of_weigh_ins = number_of_weigh_ins
		self.initial_weight = initial_weight
		self.initial_bmi = self.bmi(self.height, self.initial_weight)
		self.weight_change = latest_weight - initial_weight
		self.bmi_change = self.bmi(self.height, latest_weight) - self.initial_bmi
		
	def __str__(self):
		return ",".join(map(str,[self.user_id, self.ck_id, self.height, self.number_of_weigh_ins, self.weight_change, self.bmi_change]))
			
	def bmi(self, height, weight):
		return (weight*703.0)/(height**2)

def main(database):
	db = DBConnection(database)
	
	#for each user assemble a table:
	#id, ck_id, weigh_ins, weight_change, bmi_change, age
	
	table = []
	users = db.query("SELECT * FROM users")
	f = open("all_weigh_ins.dat", "w")
	print >> f, ",".join(["id", "ck_id", "height", "weigh_ins", "weight_change", "bmi_change"])
 	for user in users:
		user_id = int(user["id"])
		ck_id = user["ck_id"]
		height = user["height"]
		initial_weight = int(user["initial_weight"])
		#find the number of weigh_ins
		wi_query = db.query("SELECT COUNT(*) FROM weigh_in_history WHERE ck_id = '"+ck_id+"'")
		num_weigh_ins = int(wi_query[0]["COUNT(*)"])
		#find the most recent weigh_in
		#SELECT * FROM `weigh_in_history` WHERE `ck_id` = "bd84dbe2-dd6e-4125-b006-239442df2ff6" ORDER BY on_day DESC LIMIT 1;
		latest_wi_query = db.query("SELECT * FROM weigh_in_history WHERE ck_id = '"+ck_id+"' ORDER BY on_day DESC LIMIT 1")
		latest_weight = int(latest_wi_query[0]["weight"])
		u = CKUser(user_id, ck_id, height, initial_weight, num_weigh_ins, latest_weight)
		print >> f, u
	f.close()

		
		

if __name__ == "__main__":
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
	database_name = sys.argv[1]	
	main(database_name)