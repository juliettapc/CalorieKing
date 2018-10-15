"""
 Code friends list and their total activity
"""

import os
import sys
import subprocess
import glob
import math
import random
import datetime

a_file = open('friend_2_list.txt','r')
data = a_file.readlines()
a_file.close()


b_file = open('nodelist_activity_2.dat','r')
data1 = b_file.readlines()
b_file.close()

node1 = []
for line in data1:

   line = line.split()

   for row in data:

       row = row.split()

       if line[0] == row[0]:

         print row[0], line[1]


