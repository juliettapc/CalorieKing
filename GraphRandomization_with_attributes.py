'''
Created on May 4, 2010
Produces Monte-Carlo Randomizations of a NetworkX Graph
@author: dwmclary
'''
import networkx as nx
import random


def order_tuple(t):
    '''Given a pair t, orders the pair smallest to largest.'''
    if t[0] > t[1]:
        return (t[1], t[0])
    else:
        return t
    

def evaluate_edges(t,w, edges):
    '''For two tuples t and w and a list of edges:
    if the intersection of t and w is not empty,
    all ordered 2-permutations t' and w' of the union of t and w are
    compared against the edgelist.  If t' and w' are not
    present in the edgelist, a list containing t' and w' is returned.'''    
    if not (t[0] in w or t[1] in w):
            t_prime = order_tuple((t[0], w[0]))
            w_prime = order_tuple((t[1], w[1]))
            if t_prime not in edges and w_prime not in edges:
                return [t_prime, w_prime]
            else:
                t_prime = order_tuple((t[0], w[1]))
                w_prime = order_tuple((t[1], w[0]))
                if t_prime not in edges and w_prime not in edges:
                    return [t_prime, w_prime]
    return []
     
#Marta's code sets fact=10, but why?

def mc_randomize_m(G):
    '''Given a NetworkX graph G, produces a randomization H generated via
    monte-carlo method.'''



    edges = G.edges()
    fact = 10
    for i in range(fact*len(edges)):
        edge1 = random.choice(edges)
        selected_pairs = []
        count = 0
        while not selected_pairs and count < 10:
            edge2 = random.choice(edges)
            selected_pairs = evaluate_edges(edge1, edge2, edges)
            count += 1
            if selected_pairs:
                edges.remove(edge1)
                edges.remove(edge2)
                edges += selected_pairs
        if len(edges) != len(G.edges()):
            print "Randomization error: could not substitute all edges"
            break
    H = nx.Graph()
    H.add_edges_from(edges)
    

    return H


def print_graph(G, file=None):
    '''Given a NetworkX graph G, prints the edgelist.  If a file handle is passed,
    G will be written to file.'''
    for edge in G.edges():
        if file != None:
            print >> file, " ".join(map(str,edge))
        else:
            print " ".join(map(str,edge))

        
       print G.node[100]['label'],G.node[node]['role'],G.node[node]['percentage_weight_change'],G.node[node]['weigh_ins']
  


        
    
