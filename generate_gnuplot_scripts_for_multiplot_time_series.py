#! /usr/bin/env python

"""
Created by Julia Poncela of November 2011

It reads the CK time series and writes a gnuplot script to (multi)plot 10 at the time, and the calls gnuplot to do it every time.


It doesnt take any arguments.

"""


  
import sys
import os
import subprocess as sp

#p = sp.Popen(["python","hola.py"])

def main ():



# Text for the gnuplot script:
  
    header="reset ; set title 'Time evolution of the BMI (users with >=100 weigh-ins)' ; set nokey ;set xlabel 'time (index weigh-in #)' ; set ylabel 'BMI' ;"

    figure="p 'temporal_series/most_weigh_ins/weigh_in_time_serie_days2_top50_frequencies_t_points_segments10_threshold.dat' u 1:3  index 0  with points ls 1 ,'temporal_series/most_weigh_ins/weigh_in_time_serie_days2_top50_frequencies_t_points_segments10_threshold.dat' u 1:3  index 1  with points ls 2    ;"


    ending="set term post enhanced color dashed 15 ;  set output './temporal_series/most_weigh_ins/test_multiplot_from_python.eps' ; rep ; set output ; set term x11 ;reset "




    output_script="temporal_series/most_weigh_ins/test_gnuplot.gpt"
    file = open(output_script,'wt')
    print >> file, header,figure, ending
    file.close()

   

    p = sp.Popen(["gnuplot","temporal_series/most_weigh_ins/test_gnuplot.gpt"])

  




############################################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

