from transform_labels_to_nx import *
from look_up_table import *
import sys
import networkx as nx

H0 = nx.read_gml("method3/networks/engaged_users_network.gml")

print H0.nodes()

def filter_adherence(in_gml):
       
   H1 = nx.read_gml(str(in_gml))

   for m in H0.nodes() :
    for n in H1.nodes():
     if H1.node[n]["label"]==H0.node[m]["label"] :

      H1.node[n]["time_in_system"] = H0.node[m]["time_in_system"]
      H1.node[n]["degree"] = H0.node[m]["degree"]
      H1.node[n]["final_bmi"] = H0.node[m]["final_bmi"]
      H1.node[n]["age"] = H0.node[m]["age"]
      H1.node[n]["days"] = H0.node[m]["days"]
      H1.node[n]["vitality"] = H0.node[m]["vitality"]
      H1.node[n]["betweenness"] = H0.node[m]["betweenness"]
      H1.node[n]["activity"] = H0.node[m]["activity"]
      H1.node[n]["weigh_ins"] = H0.node[m]["weigh_ins"]
      H1.node[n]["initial_weight"] = H0.node[m]["initial_weight"]
      H1.node[n]["height"] = H0.node[m]["height"]
      H1.node[n]["percentage_weight_change"] = H0.node[m]["percentage_weight_change"]
      H1.node[n]["initial_bmi"] = H0.node[m]["initial_bmi"]
      H1.node[n]["weight_change"] = H0.node[m]["weight_change"]
   print H1.nodes()
   for n in H1.nodes():
        print H1.node[n]["percentage_weight_change"], H1.node[n]["id"]
   G_ad2 = nx.write_gml(H1,"method3/networks/method3_SC_adherent_attrib.gml")

if __name__== "__main__":
    
    if len(sys.argv) > 1:
        in_gml = sys.argv[1]
    
    filter_adherence(in_gml)
