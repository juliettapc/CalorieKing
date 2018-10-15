#! /usr/bin/env python

import csv
import networkx as nx
import numpy

def main():


    weigh_ins=5  #minimum number of weigh-ins for a user to be consider
   


    list_days=[]  #minimum number of days present in the system for a user to be consider
    #list_days.append(1)
   

    #for i in range (10,601,10):  #(inicio, fin, intervalo)
        
     #   list_days.append(i)
    




    list_days.append(100)
       






    name1="5_points_network_2010/data/all_2.csv"  
    directory=name1.split("all")[0]
   



#data in the csv file:

#"id", "weigh_ins", "initial_weight", "weight_change","days","n_weight_change", "percentage_weight_change", "time_in_system", "height", "age", "initial_BMI", "final_BMI", "change_in_BMI"


  #Each row read from the csv file is returned as a list of strings. 
            #No automatic data type conversion is performed.
 





#output file
    filename1=directory+"weight_averages_"+str(weigh_ins)+"weigh_ins_underweight.dat"
    file = open(filename1,'wt')
    file.close()

    filename2=directory+"BMI_averages_"+str(weigh_ins)+"weigh_ins_underweight.dat"
    file = open(filename2,'wt')
    file.close()


    filename3=directory+"weight_percentage_averages_"+str(weigh_ins)+"weigh_ins_underweight.dat"
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
     

        list_nodes_all=[]
        list_nodes_network=[]
        list_nodes_not_network=[]
        list_nodes_network_GC=[]
        list_nodes_network_not_GC=[]
     


        list_weight_percentage_all=[]
        list_weight_percentage_network=[]
        list_weight_percentage_not_network=[]
        list_weight_percentage_network_GC=[]
        list_weight_percentage_network_not_GC=[]
      
  



#POR QUE, SI NO LO VUELVO A LEER CADA VEZ, A PARTIR DE LA SEGUNDA VEZ ESTA VACIO!!???
 

# delimiter is a 1-character string that separates fields, quotechar is used to quote fields containing special characters,

        resultado= csv.reader(open(name1, 'rb'), delimiter=',')#, quotechar='|')
        for row in resultado:
            node=str(row[0]) # the user's id
            
            #print row

            try:                       

                if int(row[1])>=weigh_ins:  #more than x weigh-ins

                   #if (float(row[10])>30): #obese
                    #if (float(row[10])>25) and(float(row[10])<30): #overweighted
                    #if (float(row[10])>18.5) and (float(row[10])<25): #normal   
                    if (float(row[10])< 18.5): #underweighted group

                        #print float(row[10]), float(row[2]), float(row[3])
      
                        if int(row[4])>days: # present in the system for more than x days        

                
                            list_weight_changes_all.append(float(row[3]))
                            list_BMI_changes_all.append(float(row[12]))
                            list_weight_percentage_all.append(float(row[6]))
                            list_nodes_all.append(node)

                            if node in list_friends:
                                list_weight_changes_network.append(float(row[3]))                   
                                list_BMI_changes_network.append(float(row[12]))                   
                                list_weight_percentage_network.append(float(row[6]))                   
                                list_nodes_network.append(node)
                               

                                if node in list_friends_GC:
                                    list_weight_changes_network_GC.append(float(row[3]))
                                    list_BMI_changes_network_GC.append(float(row[12]))
                                    list_weight_percentage_network_GC.append(float(row[6]))
                                    list_nodes_network_GC.append(node)

                                elif  node in list_friends_not_GC:
                                    list_weight_changes_network_not_GC.append(float(row[3]))
                                    list_BMI_changes_network_not_GC.append(float(row[12]))
                                    list_weight_percentage_network_not_GC.append(float(row[6]))
                                    list_nodes_network_not_GC.append(node)

                            else:  # not in the friend network
                                list_weight_changes_not_network.append(float(row[3]))
                                list_BMI_changes_not_network.append(float(row[12]))
                                list_weight_percentage_not_network.append(float(row[6]))
                                list_nodes_not_network.append(node)


               
            except ValueError:  #to exclude the first row of the csv file
                pass



        filename4=directory+"users_"+str(weigh_ins)+"weigh_ins_"+str(days)+"days_NonNetw_underweight.dat"
        file = open(filename4,'wt')
        print >> file,list_nodes_not_network
        file.close()
   

        filename4=directory+"users_"+str(weigh_ins)+"weigh_ins_"+str(days)+"days_IsolClust_underweighted.dat"
        file = open(filename4,'wt')
        print >> file,list_nodes_network_not_GC
        file.close()
   

        filename4=directory+"users_"+str(weigh_ins)+"weigh_ins_"+str(days)+"days_GCt_underweighted.dat"
        file = open(filename4,'wt')
        print >> file,list_nodes_network_GC
        file.close()
   



        print "underweighted:", len(list_nodes_all), "(all)    ", len(list_nodes_network), "(Netw)    ", len(list_nodes_not_network), "(nonNetw)    ",len(list_nodes_network_not_GC), "(nGC)    ",len(list_nodes_network_GC), "(GC)    "
    







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
