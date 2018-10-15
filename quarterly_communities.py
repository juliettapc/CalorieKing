from communities_CK_GC_list_of_lists import *
import os
 
path = str(os.getcwd())+"/5_points_network_2010/data/new_networks/"
input_files = ["friends_undirected_all_quarter0","friends_undirected_all_quarter1","friends_undirected_all_quarter2",\
                "friends_undirected_all_quarter3","friends_undirected_all_quarter4","friends_undirected_all_quarter5",\
                "friends_undirected_all_quarter6","friends_undirected_all_quarter7"]

f = open(str(path)+"quartely_community_summary.dat","w")
print>>f,"number of members for each_community" 

for input in input_files:
    name = str(input)
    file = open(str(path)+str(name)+"_communities.dat","w")
    
    list_of_lists = main(path+input)
    list_of_lists = map(str,list_of_lists)
    
    print>>f, str(input),":",map(len,list_of_lists)
    print>>file,";".join((map(lambda x: str(x).strip('[]').strip("''"),list_of_lists)))

    print ";".join((map(lambda x: (str(x).strip('[]')).strip("''"),list_of_lists)))
    file.close()

for x in list_of_lists:
    print len(x)

f.close()
 
