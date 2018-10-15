from communities_CK_GC_list_of_lists import *
import os
 
path = str(os.getcwd())+"/5_points_network_2010/data/new_networks/"
input_files = ["friends_undirected_all_sixmonths0","friends_undirected_all_sixmonths1","friends_undirected_all_sixmonths2",\
                "friends_undirected_all_sixmonths3"]

f = open(str(path)+"six_monthly_community_summary.dat","w")
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
 
