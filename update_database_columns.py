#! /usr/bin/env python

import MySQLdb
import sys
from glob import glob
import re

first = lambda x:x[0]
def make_table(db, table_name, fields):
	field_string = []
	for f in fields:
		field_string.append(first(f.keys())+" "+first(f.values()))
	create_string = "CREATE TABLE "+ table_name + " (" + ", ".join(field_string)+ ")"
	print create_string
	try:
		db.execute(create_string)
	except Exception:
		pass
	
def load_table(db, table_name, filename, sep=","):
	load_string = "LOAD DATA LOCAL INFILE '" + filename + "' INTO TABLE " + table_name +\
	" FIELDS TERMINATED BY '"+sep+"' LINES TERMINATED BY '\\n'"
	print load_string
	db.execute(load_string)

if __name__ == "__main__":
	SERVER = "tarraco.chem-eng.northwestern.edu"
	DATABASE = "calorie_king_social_networking_2010"
	USER = "calorieking"
	PASSWD = "n1ckuDB!"
	data_folder = sys.argv[1]
	data_files = glob(data_folder+"*.txt")
	
	user_fields = [{"ck_id": "CHAR(36)"}, {"join_date":"DATETIME"}, {"initial_weight":"FLOAT"},\
	 {"most_recent_weight":"FLOAT"}, {"height":"INT"}, {"age":"INT"}, {"state":"CHAR(36)"},\
	{"is_staff":"CHAR(36)"}]
	daily_steps_fields = [{"on_day":"DATETIME"},{"ck_id":"CHAR(36)"},{"steps":"INT"}]
	blog_fields = [{"at_time":"DATETIME"},{"post_date":"DATE"},{"poster":"CHAR(36)"},{"owner":"CHAR(36)"}]
	diary_fields = [{"ck_id":"CHAR(36)"},{"visibility":"CHAR(36)"}]
	favorite_blog_fields = [{"ck_id":"CHAR(36)"},{"num_blogs":"INT"},{"num_favorites":"INT"}]
	ignore_fields = [{"src":"CHAR(36)"},{"dest":"CHAR(36)"}]
	friend_fields = [{"src":"CHAR(36)"},{"dest":"CHAR(36)"}]
	lesson_fields = [{"at_time":"DATETIME"},{"content_id":"CHAR(36)"},{"poster_id":"CHAR(36)"}]
	group_fields = [{"forum_id":"CHAR(36)"},{"ck_id":"CHAR(36)"}]
	pm_fields = [{"at_time":"DATETIME"},{"src_id":"CHAR(36)"},{"dest_id":"CHAR(36)"}]
	forum_fields = [{"forum_id":"CHAR(36)"},{"user_created":"CHAR(36)"}]
	post_fields = [{"at_time":"DATETIME"},{"thread_id":"CHAR(36)"},{"forum_id":"CHAR(36)"},{"ck_id":"CHAR(36)"}]
	comment_fields = [{"at_time":"DATETIME"},{"poster_id":"CHAR(36)"},{"owner_id":"CHAR(36)"}]
	weigh_in_fields = [{"on_day":"DATE"},{"ck_id":"CHAR(36)"},{"weight":"FLOAT"}]
	membership_fields = [{"ck_id":"CHAR(36)"},{"on_day":"DATE"},{"type":"CHAR(36)"}]
	
	tables = {'daily_steps': {"loc":data_folder+'daily_steps.txt', "field":daily_steps_fields},\
	 'blog_comments': {"loc":data_folder+'blog_comments.txt',"field":blog_fields},\
	 'users': {"loc":data_folder+'users.txt', "field":user_fields},\
	 'public_diary': {"loc": data_folder+'public_diary.txt',"field":diary_fields},\
	 'favorite_blogs':{"loc": data_folder+'favourite_blogs_threads.txt',"field":favorite_blog_fields},\
	 'ignores': {"loc":data_folder+'ignore_list.txt',"field":ignore_fields},\
	 'friends': {"loc":data_folder+'friends_list.txt',"field":friend_fields},\
	 'lesson_comments': {"loc":data_folder+'program_lesson_comments.txt',"field":lesson_fields},\
	 'public_groups': {"loc":data_folder+'public_group_memberships.txt',"field":group_fields},\
	 'private_messages': {"loc":data_folder+'private_messages.txt',"field":pm_fields},\
	 'forums': {"loc":data_folder+'forums.txt',"field":forum_fields},\
	 'forum_posts': {"loc":data_folder+'forum_posts.txt',"field":post_fields},\
	 'homepage_comment': {"loc":data_folder+'user_homepage_comments.txt',"field":comment_fields},\
	 'weigh_in_history': {"loc":data_folder+'weighin_history.txt',"field":weigh_in_fields},\
	 'membership_periods': {"loc":data_folder+'membership_periods.txt',"field":membership_fields}}
	

	
	db = MySQLdb.Connect(host=SERVER, db=DATABASE, user=USER, passwd=PASSWD)
	cursor = db.cursor()
	for t in tables:
		make_table(cursor, t, tables[t]['field'])
		db.commit()
		load_table(cursor, t, tables[t]['loc'])
		db.commit()

			