import networkx as nx 
from read_a_gml import *
from look_up_table import *


look_up = look_up_table()
"""
    This script simply calculates the average weight loss of the neighbors of a node, and prints it
    to a file
    
    Written by Rufaro Gerald Mukogo, Northwestern University on 2011-07-26

    """

def mean(X):
    X = map(float,X)
    return float(sum(X))/float(len(X))

def get_neighbor_weightloss(in_gml, outdir):

    G = read_a_gml(str(in_gml))
   
    G = nx.connected_component_subgraphs(G)[0]

    f = open(str(outdir)+"/users_neighbor_weight_loss.dat","w")

    for n in G.nodes():
        print>>f,look_up["percentage_weight_change"][int(n)],\
        mean([look_up["percentage_weight_change"][n] for n in map(int,G.neighbors(n))]) 
    
if __name__== "__main__":

    if len(sys.argv) > 1:
        in_gml = sys.argv[1]

    if len(sys.argv) > 2:
        outdir = sys.argv[2]

    get_neighbor_weightloss(in_gml,outdir)
