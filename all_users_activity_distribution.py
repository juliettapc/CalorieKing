#! /usr/bin/env python


"""
all_users_activity_distrubition.py

Created by Rufaro Mukogo on 2010-12-21.
Copyright (c) 2010 __Northwestern University__. All rights reserved.

This script computes the distribution of all users activity (blog posts, messages, forum posts) in the CK database.

"""

import numpy
import sys
import os
import matplotlib
from matplotlib import pyplot as plt
from pylab import *
from build_friend_graph import *
from function_to_plot_histogram import *


def compute_activity(cut_off,lb,ub, path): 
   
    f = open(str(path)+'candidate_activity_with_'+str(cut_off)+'/total_activity_for_all_user_'+str(cut_off)+'_threshold.dat','r')
    print "lower and upper", lb,ub
    lines=f.readlines()[1:]

    activity = []
    
    for line in lines:
        datum = float(line.split(',')[2])
        activity.append(datum)

    activity = filter(lambda x: lb<=x<=ub, activity)
    #print activity

    return lines, activity

def return_ids_for_graph(lines,lb,ub):
    
    user_data = []
    for line in lines:
        datum = line
        user_data.append([line.split(',')[0],line.split(',')[1],line.split(',')[2]])
    
    data_scrubbed = []
         
    for datum in user_data:
        #print "lower and upper bounds 3", lb, ub 
        
        b=float(datum[2]) 

        if(b>=lb) and (b<=ub):   
            
            data_scrubbed.append(datum[0])
        
        else:
            pass
    #print "user_data_scrub", data_scrubbed

    return data_scrubbed

def main(cut_off,lb,ub, dir, path):
    
    lines,activity = compute_activity(cut_off,lb,ub,path)
    
    uids = return_ids_for_graph(lines,lb,ub)

    if ub >= 500:
        nbins =int(ub)
    else:
        nbins = 200

    #plot network
    ckg = CKGraph()
    G=ckg.build_undirected_graph(uids=uids)
    Gprime = G[0] 
    #nx.draw(Gprime)
    #plt.show()
    
    degree = Gprime.degree()
    degree_values = map(int,list(degree.values()))
    
    closeness = nx.closeness_centrality(Gprime)
    closeness_values = map(float,list(closeness.values()))
    
    betweenness = nx.betweenness_centrality(Gprime)
    betweenness_values = map(float,list(betweenness.values()))
    
    figure(1)
    nbins = [int(i) for i in xrange(1,max(degree_values)+1)]
    n, bins, patches=hist(degree_values,normed=0,bins=nbins, log=True)
   
    #print "binn values", bins
    #print "max degree" , max(degree_values)

    plt.xlabel('degree, k')
    plt.ylabel('N(k)')
    plt.title('degree distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax = gca()
    #ax.set_xscale("log")
    #ax.set_yscale("log")
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+"/plots/"+'degree_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub)+'.eps', dpi=100)
    
    data = zip(bins,n)
   
    
    f = open(str(dir)+"/data/degree_distribution_data.dat","w")

    nonzero_data = []
    for datum in data:
        if datum[1]>=1:
            print>>f, datum
            nonzero_data.append(datum)
        else:
            pass

    histogram_plotting(nonzero_data, dir+"data/", filename="degree_distribution_complete_network"+str(cut_off)+"_points",\
            x_axis="degree, k", y_axis="N(k)")

    figure(2) 
    plt.hist(betweenness_values, normed=0,bins=120, log=True)
    plt.xlabel('betweenness, b')
    plt.ylabel('N(b)')
    plt.title('betweenness distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax = gca()
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+'betweennness_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub)+'.eps', dpi=100)

    figure(3) 
    plt.xlabel('closeness, c')
    plt.hist(closeness_values,normed=0,bins=120, log=True)
    plt.ylabel('N(c)')
    plt.title('closeness distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax = gca()
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+'closeness_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub)+'.eps', dpi=100)

    figure(4)
    n, bins, patches = hist(activity,normed=0,bins=max(activity), log=True)
    plt.xlabel('activity, a')
    plt.ylabel('N(a)')
    plt.title('activity distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax=gca()
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+'activity_distribution_'+str(cut_off)+'_points_'+str(int(lb))+'_'+str(int(ub))+'.eps', dpi=100)
    #plt.show()
    
    print "activity bins", bins
    
    data_act = zip(bins,n)
    g = open(str(dir)+"/data/activity_distribution_data.dat","w")

    nonzero_act_data = []
    for datum in data_act:
        if datum[0]>0 and datum[1]>=1:
            print>>g, datum
            nonzero_act_data.append(datum)
        else:
            pass
    
    histogram_plotting(nonzero_act_data, dir+"/data/", filename="activity_distribution_complete_network"+str(cut_off)+"_points"\
            , x_axis="activity, a", y_axis="N(a)")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        number_of_weightpoints = int(sys.argv[1])
    else:
          number_of_weightpoints = 2
    if len(sys.argv) >3:
        lb = float(sys.argv[2])
        ub = float(sys.argv[3])
    else:
        lb = 0.0
        ub = 5000.0
    if len(sys.argv) > 4:
        path  = sys.argv[4]
    else:
        path = ""
    cut_off = number_of_weightpoints
    
    dir = str(path)+str(cut_off)+'_points_network/' 
    main(cut_off,lb,ub, dir, path)





