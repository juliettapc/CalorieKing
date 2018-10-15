from transform_labels_to_nx import *
import networkx as nx
import sys

def read_a_gml(filename):

    if ".gml" not in filename:
        filename = str(filename) + ".gml"
    
    G = nx.read_gml(str(filename))
    G = transform_labels_to_nx(G)
    
    return G
    
if __name__=="__main__":
    pass
