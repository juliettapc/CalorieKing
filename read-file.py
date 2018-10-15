#!/usr/bin/env python2.6
import sys;
import os;
import string
from optparse import *
import re
import exceptions
import glob
from types import *
from numpy import *
from random import *

#####################################################

filename = 'candidate_activity_with_2/total_activity_for_all_user_2_threshold.dat'
a_file = open(filename,'r')
data = a_file.readlines()
a_file.close()

for line in data:
   
  if "ck_id" in line:
    continue
  line = line.rstrip()
 
  fields = line.split(',')

  print int(fields[1]), "\t", int(fields[2])
