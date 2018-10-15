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




    file=open("number_segments_acording_to_frequencies.dat",'r')   # i read the file with the number of segments in each time serie
    list_lines_file=file.readlines()
    dicc_number_segments={}

    for line in list_lines_file:
        list=line.split(" ")
        key=str(list[0])   #index file
        value=int(list[1])   # corresponding number of segments
        dicc_number_segments[key]=value
   
    #print dicc_number_segments




   


# Text for the gnuplot script:
  
    header="reset ; set term post enhanced color dashed 8 ; set output 'Multiplot_time_series_indiv_frequencies_segments_meaningful_A_test.eps' ;NX=1; NY=2 ; SX=1; SY=0.5 ; set size SX*NX,SY*NY ;set multiplot; "

    file="1"
    num_segments=dicc_number_segments[file]

   
    for index in range(num_segments):

        print index

        figure_partial="set size SX,SY; set origin 0,0.5 ; set pointsize 0.2; set yrange [-15:10]; set nokey; set ylabel '% weight change' ;set xlabel '';  p 'weigh_in_time_serie_days1_top50_frequencies_t_points_segments10_threshold.dat' u 1:3  index "+str(index)+"  with points ls "+str(index+1)

        figure_partial2=";set size SX,SY; set origin 0,0 ; set pointsize 0.2; set yrange [-15:10]; set nokey; set ylabel '% weight change' ;set xlabel '';  p 'weigh_in_time_serie_days1_top50_t_points_residuals.dat'  index "+str(index)+"  with points ls "+str(index+1)




        figure=figure_partial+figure_partial2

  

    #figure2=";set size SX,SY; set origin 0,0.6 ; set pointsize 0.2; set yrange [-15:10]; set nokey; set ylabel '% weight change' ;set xlabel "";  p 'temporal_series/most_weigh_ins/weigh_in_time_serie_days2_top50_frequencies_t_points_segments10_threshold.dat' u 1:3  index 0  with points ls 1 ,'temporal_series/most_weigh_ins/weigh_in_time_serie_days2_top50_frequencies_t_points_segments10_threshold.dat' u 1:3  index 1  with points ls 2    ;"

    ending=";set nomultiplot; reset "




    output_script="test_gnuplot.gpt"
    file = open(output_script,'wt')
    print >> file, header,figure, ending
    file.close()

   

    p = sp.Popen(["gnuplot","test_gnuplot.gpt"])

   # salida=p.communicate()  #es una tupla en la q guarda lo que sale 
   # print salida
   




############################################
          
if __name__== "__main__":
   
    main()

    try:
        import psyco
    except ImportError: pass

   

##############################################

 

