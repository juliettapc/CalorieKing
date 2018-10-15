from standard_deviation_class import *
import sys,os
import networkx as nx
import pprint

class roles:
    """Created by Rufaro Mukogo on 2011-03-12.
    Copyright (c) 2010 __Northwestern University__. All rights reserved.

    This script generates a dat file with two vector separated by commas (role, metric) this format is convenient for 
    plotting boxplots in R. The code can easiky be modified to calculate global properties like the mead and standard    deviation for each role.
    """

    def __init__(self,graph_file,num_points=5, roles =[], key=None):

        self.key = key
        self.roles = roles
        self.num_points = num_points
        self.graph_file = graph_file
        self.G = nx.read_gml("./"+str(self.num_points)+"_points_network_2010/data/"+str(self.graph_file))
        self.G = nx.connected_component_subgraphs(self.G)[0]
        print "number of nodes", len(self.G.nodes())

    def extract_roles(self):
        

        f = open("./"+str(self.num_points)+"_points_network_2010/data/roles/"+str(self.key[0])+".dat", "w")

        metric_list = []
       
        print>>f,"role",",",str(self.key[0])

        for r in self.roles:
            nodelist = []
            metric_data = 0
            for n in self.G.nodes():
                if self.G.node[n]["role"] == r:
                    nodelist.append(n)

            metric_data = map(lambda x: [self.G.node[n][x] for n in nodelist], self.key)
            metric_list.append(metric_data)
            
            print metric_list
                       
            for g in sum(metric_data,[]):
                print>>f,r,",",g
            
            #std_property[r] = map(lambda x: stddev([self.G.node[n][x] for n in nodelist]), self.key)
            #print "data", ",".join(map(str,sum(metric_data,[])))
            #print>>f,str(r),",",",".join(map(str,sum(metric_data,[])))

if __name__ =='__main__':
    
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = "change_in_BMI"
   
    if len(sys.argv) > 2:
        num_points = sys.argv[2]
    else:
        num_points = 5

    if len(sys.argv) > 3:
        graph_file = sys.argv[3]
    else:
        graph_file = "friend_graph_all_5_2010.gml"

    obj = roles(graph_file=graph_file,num_points = num_points, roles = ["R1","R2","R3","R4","R5","R6","R7"], key =[key])
    obj.extract_roles()

