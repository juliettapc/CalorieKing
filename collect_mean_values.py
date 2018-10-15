#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-01-11.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

A generic reduction script which reads a pre-computed value from mean_chk and compares it to the mean of all values passed to it via stdin.
The result is the mean, standard deviation, and a z-score representing the significance of the measure in mean_chk.

"""

import sys
import os
import math

'''A generator for processing a list of floats separated by newline.'''
def read_input(file):
    for line in file:
        if len(line.strip()) > 0:
            yield map(float, line.rstrip().split())

def main():
    data = read_input(sys.stdin)
    
    giant_mean, external_mean = (open("mean_chk").readline()).strip().split()
    giant_mean = float(giant_mean)
    external_mean = float(external_mean)
    mean = abs(giant_mean)-abs(external_mean)
    
    m = 0.0
    m2 = 0.0
    data = list(data)
    n = float(sum(1 for e in data))

    #Z = (bar(X) - mu)/ sigma
    m = sum(abs(e[0])-abs(e[1]) for e in data)
    mu = m/n
    sigma = 0.0
    for e in data:
        sigma += ((abs(e[0])-abs(e[1])) - mu)**2
        
    sigma /= n
    sigma = math.sqrt(sigma)
    z_lower = (sigma/math.sqrt(n))
    if z_lower > 0.0:
        standardized_z = mu/z_lower
    else:
        standardized_z = 0.0
    if sigma > 0.0:
        z = (mean - mu)/sigma
    elif (mean - mu) < 1e-7:
        z = 0.0
    else:
        z = 5.0
    print "Mean " + str(mean)
    print "Mu " + str(mu)
    print "Sigma " + str(sigma)
    print "Zscore " + str(z)


if __name__ == '__main__':
    main()

