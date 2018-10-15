#! /usr/bin/env python

import csv
import networkx as nx
import numpy

def main():


    weigh_ins=5  #minimum number of weigh-ins for a user to be consider
   


    list_days=[]  #minimum number of days present in the system for a user to be consider
    list_days.append(1)
    for i in range (10,601,10):  #(inicio, fin, intervalo)
        
        list_days.append(i)
    
       

    name1="5_points_network_2010/data/all_2.csv"  
    directory=name1.split("all")[0]
   



#data in the csv file:

#"id", "weigh_ins", "initial_weight", "weight_change","days","n_weight_change", "percentage_weight_change", "time_in_system", "height", "age", "initial_BMI", "final_BMI", "change_in_BMI"


  #Each row read from the csv file is returned as a list of strings. 
            #No automatic data type conversion is performed.
 





#output file
    filename1=directory+"weight_averages_"+str(weigh_ins)+"weigh_ins_obese.dat"
    file = open(filename1,'wt')
    file.close()

    filename2=directory+"BMI_averages_"+str(weigh_ins)+"weigh_ins_obese.dat"
    file = open(filename2,'wt')
    file.close()


    filename3=directory+"weight_percentage_averages_"+str(weigh_ins)+"weigh_ins_obese.dat"
    file = open(filename3,'wt')
    file.close()



    BMI_label='obese'






    name2="5_points_network_2010/data/friend_graph_all_5_2010_comm_roles.gml"
    H=nx.read_gml(name2)
    name2=name2.split(".gml")[0]


   # print type(H.node[19]['label']),H.node[19]['label'],type(H.node[19]['id']),H.node[19]['id']
    

    G = nx.connected_component_subgraphs(H)[0]

    list_friends=[] # list of ids of the people in the friend network
    list_friends_GC=[] # list of ids of the people in the friend network
    list_friends_not_GC=[] # list of ids of the people in the friend network
    for node in H.nodes():
        list_friends.append(H.node[node]['label'])
        if node in G.nodes():
            list_friends_GC.append(H.node[node]['label'])     
        else:
            list_friends_not_GC.append(H.node[node]['label'])
         


#clasify the users  that belong to the network into BMI categories:
        if (float(H.node[node]['initial_BMI']) >30): #obese
            H.node[node]['BMI_group']='obese'

        elif (float(H.node[node]['initial_BMI'])>25) and(float(H.node[node]['initial_BMI']) <30): #overweighted
            H.node[node]['BMI_group']='overweighted'
                                                            
        elif (float(H.node[node]['initial_BMI']) < 25) and (float(H.node[node]['initial_BMI'])> 18.5): #normal   
            H.node[node]['BMI_group']='normal'

        elif (float(H.node[node]['initial_BMI'])< 18.5): #underweighted group   
            H.node[node]['BMI_group']='underweighted'


         
        #print node, H.node[node]['initial_BMI'],H.node[node]['BMI_group']
   
   

    #exit()

    for days in list_days:  # loop over all day-restrictions               

        print "\n",days,"days"

        list_weight_changes_all=[]
        list_weight_changes_network=[]
        list_weight_changes_not_network=[]
        list_weight_changes_network_GC=[]
        list_weight_changes_network_not_GC=[]
      

        list_BMI_changes_all=[]
        list_BMI_changes_network=[]
        list_BMI_changes_not_network=[]
        list_BMI_changes_network_GC=[]
        list_BMI_changes_network_not_GC=[]
     
  


        list_weight_percentage_all=[]
        list_weight_percentage_network=[]
        list_weight_percentage_not_network=[]
        list_weight_percentage_network_GC=[]
        list_weight_percentage_network_not_GC=[]
      
  



#POR QUE, SI NO LO VUELVO A LEER CADA VEZ, A PARTIR DE LA SEGUNDA VEZ ESTA VACIO!!???
 

# delimiter is a 1-character string that separates fields, quotechar is used to quote fields containing special characters,
        resultado= csv.reader(open(name1, 'rb'), delimiter=',')#, quotechar='|')
        for row in resultado:      
     
            try:     

               
                node=int(row[0]) # the user's id  

                if int(row[1])>=weigh_ins:  #more than x weigh-ins

                    if (float(row[10])>30): #obese
                    #if (float(row[10])>25) and(float(row[10])<30): #overweighted
                    #if (float(row[10])>18.5) and (float(row[10])<25): #normal   
                    #if (float(row[10])< 18.5): #underweighted group

                        #print float(row[10]), float(row[2]), float(row[3])
      
                        if int(row[4])>=days: # present in the system for more than x days        

                
                            list_weight_changes_all.append(float(row[3]))
                            list_BMI_changes_all.append(float(row[12]))
                            list_weight_percentage_all.append(float(row[6]))
                
                            if node in list_friends:
                                list_weight_changes_network.append(float(row[3]))                   
                                list_BMI_changes_network.append(float(row[12]))                   
                                list_weight_percentage_network.append(float(row[6]))                   
                           

                                if node in list_friends_GC:
                                    list_weight_changes_network_GC.append(float(row[3]))
                                    list_BMI_changes_network_GC.append(float(row[12]))
                                    list_weight_percentage_network_GC.append(float(row[6]))
                                elif  node in list_friends_not_GC:
                                    list_weight_changes_network_not_GC.append(float(row[3]))
                                    list_BMI_changes_network_not_GC.append(float(row[12]))
                                    list_weight_percentage_network_not_GC.append(float(row[6]))

                            else:  # not in the friend network
                                list_weight_changes_not_network.append(float(row[3]))
                                list_BMI_changes_not_network.append(float(row[12]))
                                list_weight_percentage_not_network.append(float(row[6]))
                   


               
            except ValueError:  #to exclude the first row of the csv file
                pass



        
    
        file = open(filename1,'at')
        print >> file,days,"all", len(list_weight_changes_all), numpy.mean(list_weight_changes_all),numpy.std(list_weight_changes_all),
       

        print >> file, "not_GC", len(list_weight_changes_network_not_GC),numpy.mean(list_weight_changes_network_not_GC),numpy.std(list_weight_changes_network_not_GC),


        print >> file,"network", len(list_weight_changes_network),numpy.mean(list_weight_changes_network),numpy.std(list_weight_changes_network),

        print >> file, "GC", len(list_weight_changes_network_GC),numpy.mean(list_weight_changes_network_GC),numpy.std(list_weight_changes_network_GC)

        file.close()



        file = open(filename2,'at')
        print >> file,days,"all", len(list_BMI_changes_all), numpy.mean(list_BMI_changes_all),numpy.std(list_BMI_changes_all),              
        
        print >> file, "not_GC", len(list_BMI_changes_network_not_GC),numpy.mean(list_BMI_changes_network_not_GC),numpy.std(list_BMI_changes_network_not_GC),
        

        print >> file,"network", len(list_BMI_changes_network),numpy.mean(list_BMI_changes_network),numpy.std(list_BMI_changes_network),
        
        print >> file, "GC", len(list_BMI_changes_network_GC),numpy.mean(list_BMI_changes_network_GC),numpy.std(list_BMI_changes_network_GC)

        file.close()





        file = open(filename3,'at')
        print >> file,days,"all", len(list_weight_percentage_all), numpy.mean(list_weight_percentage_all),numpy.std(list_weight_percentage_all),
       

        print >> file, "not_GC", len(list_weight_percentage_network_not_GC),numpy.mean(list_weight_percentage_network_not_GC),numpy.std(list_weight_percentage_network_not_GC),


        print >> file,"network", len(list_weight_percentage_network),numpy.mean(list_weight_percentage_network),numpy.std(list_weight_percentage_network),

        print >> file, "GC", len(list_weight_percentage_network_GC),numpy.mean(list_weight_percentage_network_GC),numpy.std(list_weight_percentage_network_GC)

        file.close()



#create a new gml file with the added atribute -BMI group-:

    nx.write_gml(H,name2+"_BMI_groups.gml")





########################################
if __name__== "__main__":   
    
    main()
######################################
