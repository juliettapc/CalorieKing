#! /usr/bin/env python

import csv
import networkx as nx
import numpy

def main():


    weigh_ins=5  #minimum number of weigh-ins for a user to be consider
    list_days=[1,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]  #minimum number of days present in the system for a user to be consider




    list_days=[]
    list_days.append(1)
    for i in range (10,601,10):  #(inicio, fin, intervalo)
        
        list_days.append(i)
    
        # delimiter is a 1-character string that separates fields, quotechar is used to quote fields containing special characters,

    name1="5_points_network_2010/data/all_2.csv"  
    directory=name1.split("all")[0]
   



#data in the csv file:

#"id", "weigh_ins", "initial_weight", "weight_change","days","n_weight_change", "percentage_weight_change", "time_in_system", "height", "age", "initial_BMI", "final_BMI", "change_in_BMI"


  #Each row read from the csv file is returned as a list of strings. 
            #No automatic data type conversion is performed.
 





#output file
    filename1=directory+"weight_averages_"+str(weigh_ins)+"weigh_ins.dat"
    file = open(filename1,'wt')
    file.close()

    filename2=directory+"BMI_averages_"+str(weigh_ins)+"weigh_ins.dat"
    file = open(filename2,'wt')
    file.close()


    filename3=directory+"weight_percentage_averages_"+str(weigh_ins)+"weigh_ins.dat"
    file = open(filename3,'wt')
    file.close()





    name2="5_points_network_2010/data/friend_graph_all.gml"
    H=nx.read_gml(name2)

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
            
        
        
   

    for days in list_days:  # loop over all day-restrictions at once (instead of running the code several times)              

        print days,"days"

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

        resultado= csv.reader(open(name1, 'rb'), delimiter=',')#, quotechar='|')
        for row in resultado:
            node=str(row[0]) # the user's id
            
            #print row

            try:                       

                if int(row[1])>=weigh_ins:  #more than x weigh-ins
                    
      
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









########################################
if __name__== "__main__":   
    
    main()
######################################
