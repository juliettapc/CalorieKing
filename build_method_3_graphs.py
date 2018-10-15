from transform_labels_to_nx import *
from look_up_table import *
import sys
import networkx as nx

def filter_adherence(in_gml):
    
    H = nx.read_gml(str(in_gml))
    H = transform_labels_to_nx(H)
    selfloops = H.selfloop_edges()
    
    for u in selfloops:
        H.remove_edge(u[0],u[1])
    
    G_ad = nx.Graph()
    G_nonad = nx.Graph()
    
    for n in H.nodes():
        if H.node[n]["weighins"] <5:
            H.remove_node(n)
    G_ad = nx.write_gml(H,"./method3_50/networks/method_3_adherent.gml")
    
    F = nx.read_gml(str(in_gml))
    F = transform_labels_to_nx(F)

    for n in F.nodes():
        if F.node[n]["weighins"] >=5:
            F.remove_node(n)
    
    G_nond = nx.write_gml(F,"./method3_50/networks/method_3_nonadherent.gml")
    
if __name__== "__main__":
    
    if len(sys.argv) > 1:
        in_gml = sys.argv[1]
    
    filter_adherence(in_gml)
