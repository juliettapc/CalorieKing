#! /usr/bin/env python

import sys, os, subprocess, shlex, random

def main():
	os.system('chmod a+rwx randomizing_commID_routine.py')
	for i in range(0):
		p = subprocess.Popen(['./randomizing_commID_routine.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = p.communicate()
		sts = p.wait()
		print output


if __name__ == "__main__":
	main()
	

