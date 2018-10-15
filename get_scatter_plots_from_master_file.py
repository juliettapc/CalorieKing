#!/usr/bin/env python


'''
Reading the master_file and creating files for scatter plots.

Created by Julia Poncela, on October, 2013

'''


def main():


    master_file_name="./analysis_time_bins_bmi_groups/master_users_file_weight_change_first6months_p180_p120_within.txt"
    file=open(master_file_name,'r')
    list_lines_file=file.readlines()


    name_topology="./analysis_time_bins_bmi_groups/scatter_plot_topology.dat"
    name_pwc="./analysis_time_bins_bmi_groups/scatter_plot_pwc_4m_6m.dat"

    output_file_topology = open(name_topology,'wt')
    output_file_pwc_4m_6m = open(name_pwc,'wt')

    cont_p120_p180=0

    cont_lines=0
    for line in list_lines_file:   
        if cont_lines >0:  # skip the header
            lista=line.split(" ")  
          

            degree=lista[26] 
            betweenness=lista[28]            
            num_R6_friends=lista[29]
            k_shell=lista[30]
            max_clique_size=lista[31]
                                              #1       2          3             4       5
            print >> output_file_topology,degree,betweenness,num_R6_friends,k_shell,max_clique_size


            p120=int(lista[18])
            p180=int(lista[19])
            pwc_4m=lista[4]
            pwc_6m=lista[5]

            if p120 ==1 and p180 ==1:               
                if pwc_4m!="NA" and pwc_6m!="NA":
                    print >> output_file_pwc_4m_6m, pwc_4m,pwc_6m
               # print p120, pwc_4m, p180, pwc_6m
                cont_p120_p180 +=1

        cont_lines +=1


    print  "number of people with p120=1 and p180=1:", cont_p120_p180

    output_file_topology.close()
    output_file_pwc_4m_6m.close()


    print "written scatter plot files:"
    print "  ",name_topology
    print "  ",name_pwc

##################################################
######################################
if __name__ == '__main__':
 
    
    main()
