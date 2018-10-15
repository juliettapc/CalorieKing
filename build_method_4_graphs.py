from transform_labels_to_nx import *
from look_up_table import *
import sys
import networkx as nx

def filter_adherence(in_gml):
    
    H2 = nx.read_gml(str(in_gml))
#    H2 = transform_labels_to_nx(H2)
    Hcc = nx.connected_component_subgraphs(H2)
    H = Hcc[0]

    G_ad = nx.Graph()
    G_nonad = nx.Graph()
    
    for n in H.nodes():
        if H.node[n]["weigh_ins"] <5:
            H.remove_node(n)
    G_ad = nx.write_gml(H,"method_4_GC_adherent.gml")
    
    F2 = nx.read_gml(str(in_gml))
#    F2 = transform_labels_to_nx(F2)
    Fcc = nx.connected_component_subgraphs(F2)
    F = Fcc[0]
    for n in F.nodes():
        if F.node[n]["weigh_ins"] >=5:
            F.remove_node(n)
    
    G_nond = nx.write_gml(F,"method_4_GC_nonadherent.gml")

    G_ad2 = nx.Graph()
    G_nonad2 = nx.Graph()

    H3 = nx.Graph()
    for Gi in Hcc[1:]:
      if len(Gi) > 1:
       for u,v in Gi.edges():
         H3.add_edges_from(Gi.edges())
    for n in H3.nodes():
       
      H3.node[n]["id"] = H2.node[n]["id"]
      H3.node[n]["label"] = H2.node[n]["label"]
      H3.node[n]["time_in_system"] = H2.node[n]["time_in_system"]
      H3.node[n]["degree"] = H2.node[n]["degree"]
      H3.node[n]["final_bmi"] = H2.node[n]["final_bmi"]
      H3.node[n]["age"] = H2.node[n]["age"]
      H3.node[n]["days"] = H2.node[n]["days"]
      H3.node[n]["vitality"] = H2.node[n]["vitality"]
      H3.node[n]["betweenness"] = H2.node[n]["betweenness"]
      H3.node[n]["activity"] = H2.node[n]["activity"]
      H3.node[n]["weigh_ins"] = H2.node[n]["weigh_ins"]
      H3.node[n]["initial_weight"] = H2.node[n]["initial_weight"]
      H3.node[n]["height"] = H2.node[n]["height"]
      H3.node[n]["percentage_weight_change"] = H2.node[n]["percentage_weight_change"]
      H3.node[n]["initial_bmi"] = H2.node[n]["initial_bmi"]
      H3.node[n]["weight_change"] = H2.node[n]["weight_change"]
    print H3.edges()
    for n in H3.nodes():
        if H3.node[n]["weigh_ins"] < 5:
            H3.remove_node(n)

    G_ad2 = nx.write_gml(H3,"method_4_SC_adherent.gml")

    F3 = nx.Graph()
    for Gi2 in Fcc[1:]:
      if len(Gi2) > 1:
       for u,v in Gi.edges():
         F3.add_edges_from(Gi.edges())

    for n in F3.nodes():
       
      F3.node[n]["id"] = F2.node[n]["id"]
      F3.node[n]["label"] = F2.node[n]["label"]
      F3.node[n]["time_in_system"] = F2.node[n]["time_in_system"]
      F3.node[n]["degree"] = F2.node[n]["degree"]
      F3.node[n]["final_bmi"] = F2.node[n]["final_bmi"]
      F3.node[n]["age"] = F2.node[n]["age"]
      F3.node[n]["days"] = F2.node[n]["days"]
      F3.node[n]["vitality"] = F2.node[n]["vitality"]
      F3.node[n]["betweenness"] = F2.node[n]["betweenness"]
      F3.node[n]["activity"] = F2.node[n]["activity"]
      F3.node[n]["weigh_ins"] = F2.node[n]["weigh_ins"]
      F3.node[n]["initial_weight"] = F2.node[n]["initial_weight"]
      F3.node[n]["height"] = F2.node[n]["height"]
      F3.node[n]["percentage_weight_change"] = F2.node[n]["percentage_weight_change"]
      F3.node[n]["initial_bmi"] = F2.node[n]["initial_bmi"]
      F3.node[n]["weight_change"] = F2.node[n]["weight_change"]

    print F3.edges()
    for n in F3.nodes():
        if F3.node[n]["weigh_ins"] >=5:
            F3.remove_node(n)

    G_nonad2 = nx.write_gml(F3,"method_4_SC_nonadherent.gml")
    
if __name__== "__main__":
    
    if len(sys.argv) > 1:
        in_gml = sys.argv[1]
    
    filter_adherence(in_gml)
