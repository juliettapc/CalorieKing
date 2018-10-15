#!/usr/bin/env python
import numpy as np
import scipy as sp
import pylab as pl
from scipy.optimize.minpack import curve_fit


file_name="./analysis_time_bins_bmi_groups/survival_curve_all.txt"
            
file=open(file_name,'r')
list_lines_file=file.readlines()

cont_lines=1


list_x=[]
list_y=[]
for line in list_lines_file:               
    list_one_line=line.split(" ")        

    list_x.append(float(list_one_line[0]))
    list_y.append(float(list_one_line[3]))


     
x = np.array(list_x)
y = np.array(list_y)


smoothx = np.linspace(x[0], x[-1], 20)

#guess_a, guess_b, guess_c = 4000, -0.005, 100
guess_a, guess_b, guess_c = 1., -1/180., 0.



guess = [guess_a, guess_b, guess_c]

exp_decay = lambda x, A, t, y0: A * np.exp(x * t) + y0

params, cov = curve_fit(exp_decay, x, y, p0=guess)

A, t, y0 = params

print "A = %s\nt = %s\ny0 = %s\n" % (A, t, y0)

pl.clf()
best_fit = lambda x: A * np.exp(t * x) + y0


pl.plot(x, y, 'b.')
pl.plot(smoothx, best_fit(smoothx), 'r-')
pl.show()
