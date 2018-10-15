#! /usr/bin/env python

import numpy
import sys
import os
import matplotlib
from matplotlib import pyplot as plt
from pylab import *
from build_friend_graph import *
from empirical_cdf_class import *
from itertools import *

def compute_activity(cut_off,lb,ub, path): 
    
    """
    This function can be used to extract slices of users based on their activity. Networks, can then be constructed based on these slices  
    
    cuf_off: the number of weigh in points 2,5,10 which define adherence thresholds
    lb: lower activity bound
    ub: upper activity bound
    
    """
    #file with activity data for each user in that threshold

    f = open(str(path)+'candidate_activity_with_'+str(cut_off)+'/total_activity_for_all_user_'+str(cut_off)+'_threshold.dat','r')
    
    activity_data=f.readlines()[1:]
    
    activity = []
    
    for line in activity_data:
        datum = float(line.split(',')[2])
        activity.append(datum)

    activity = filter(lambda x: lb<=x<=ub, activity)
    print "activity", activity

    return activity_data, activity

def return_ids_for_graph(activity_data,lb,ub):
    
    """ 
    
    This function extracts the uids for users with activity instances bounded by the lb and ub. These uids can be used to extract
    networks for this slice    
    
    """
    
    user_data = [[x.split(',')[0],x.split(',')[1],x.split(',')[2]] for x in activity_data]
    
    user_uids = []
         
    for datum in user_data:
        b=float(datum[2]) 

        if(b>=lb) and (b<=ub):   
            
            user_uids.append(datum[0])
        
        else:
            pass
    
    return user_uids

def main(cut_off,lb,ub, dir, path):
    
    activity_data,activity = compute_activity(cut_off,lb,ub,path)
    
    uids = return_ids_for_graph(activity_data,lb,ub)
    
    #extract network
    ckg = CKGraph()
    G=ckg.build_undirected_graph(uids=uids)
    Gprime = G[0]  
    degree = Gprime.degree()
    
    degree_values = map(float,list(degree.values()))
    
    cdf_degree = EmpiricalCDF(degree_values,dir+"/plots/"+'degree_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub),\
                 'degree_distribution_'+str(cut_off)+'_points_all','P(K>=k)','degree (k)' ) 
    
    cdf_degree.cdf_data()
    cdf_degree.cdf_plotting()
 
    cdf_activity = EmpiricalCDF(activity,dir+"/plots/"+'activity_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub),\
                    'activity_distribution_'+str(cut_off)+'_points_all','P(A>=a)','activity (a)') 
      
    cdf_activity.cdf_data()
    cdf_activity.cdf_plotting()

    figure(1) 
    plt.hist(degree_values,normed=0,bins=200)
    plt.xlabel('degree, (k)')
    plt.ylabel('N(k)')
    plt.title('degree distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax = gca()
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+"/plots/"+'degree_distribution_'+str(cut_off)+'_points_'+str(lb)+'_'+str(ub)+'.eps', dpi=100)

    figure(2)
    nbins = max(activity)
    plt.hist(activity,normed=0,bins=nbins)
    plt.xlabel('activity, (a)')
    plt.ylabel('N(a)')
    plt.title('activity distribution for '+str(cut_off)+'_points_with_active_count_'+str(int(lb))+'_to_'+str(int(ub)))
    ax=gca()
    ax.autoscale_view()
    plt.grid(True)
    plt.savefig(str(dir)+'/plots/activity_distribution_'+str(cut_off)+'_points_'+str(int(lb))+'_'+str(int(ub))+'.eps', dpi=100)
    
    plt.show()

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
    
    path = os.getcwd()+"/"
        
    cut_off = number_of_weightpoints
    
    dir = str(path)+str(cut_off)+'_points_network/' 
    main(cut_off,lb,ub, dir, path)
