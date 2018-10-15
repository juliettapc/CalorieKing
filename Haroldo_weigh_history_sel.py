#! /usr/bin/env python

import sys
import os
from database import *
from datetime import *

def main ():

	database="calorie_king_social_networking_2010"  
	server="tarraco.chem-eng.northwestern.edu"
	user="calorieking" 
	passwd="n1ckuDB!"

	db=Connection(server, database, user, passwd) 

	query="""Select `weigh_in_cuts`.`id` , `weigh_in_cuts`.`ck_id`, `weigh_in_cuts`.`fit_type`, `weigh_in_cuts`.`start_idx`, `weigh_in_cuts`.`stop_idx`,
		`weigh_in_cuts`.`param1`,`weigh_in_cuts`.`param2`,`weigh_in_cuts`.`param3`
		From `weigh_in_cuts`
		Order by `weigh_in_cuts`.`ck_id`"""
	selfile=db.query(query)




	for row in selfile:
		query="SELECT weigh_in_history.ck_id, weigh_in_history.on_day,weigh_in_history.weight FROM weigh_in_history WHERE weigh_in_history.ck_id='" + row['ck_id'] + "' Order by weigh_in_history.on_day"
		res=db.query(query)


		first_day=row['start_day']
		last_day=row['stop_day']

		fist_date=res[0]['on_date']
		last_date=res[-1]['on_date']


		count=0	
		for his in res:
				

			day=his['on_day']
			if (day>=) and (count<row['stop_idx']):
				print str(row['id']) + "\t" + str(his['ck_id']) + "\t"+ str(his['on_day']) + "\t" + str(his['weight']) + "\t" + str(row['fit_type']) + "\t" + str(row['param1']) + "\t" + str(row['param2']) + "\t" + str(row['param3'])
			count=count+1

	#weigh_join_friend=db.query(query)

	#file=open("weigh_history.dat",'wt')

			#for results in weigh_join_friend:
			#ck_id=results['ck_id']
			#on_day=results['on_day']
			#weigh=results['weight']
	#print >> file, ck_id + "\t" + str(on_day) +"\t" + str(weigh)
		

if __name__== "__main__":
	main()
