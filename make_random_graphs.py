#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-01-10.
Copyright (c) 2011 __Northwestern University__. All rights reserved.

A mapper script which randomizes the input graph and computes the different between giant-component weight loss and all other components.
The graph to be randomized is read from ck_mc_graph, and a csv containing the corresponding weight data is read from ck_mc_data.
"""

import sys
import os
import string
import GraphRandomization as mcg
import networkx as nx

def compute_mean_weight_loss(G,data):
    components = nx.connected_component_subgraphs(G)
    giant_component = components[0]
    components.remove(giant_component)
    
    giant_component_weight_loss = 0.0
    for n in giant_component.nodes():
        try:
            giant_component_weight_loss += data[n]
        except KeyError:
            pass
    giant_component_weight_loss /= float(len(giant_component))
    
    external_component_weight_loss = 0.0
    for c in components:
        for n in c.nodes():
            try:
                external_component_weight_loss += data[n]
            except KeyError:
                pass
    external_component_weight_loss /= float(sum(map(len,components)))
    
    return giant_component_weight_loss, external_component_weight_loss

    
def main(external=False):
    #open the graph
    G = nx.read_edgelist("./ck_mc_graph")
    #open the data
    datafile = map(string.split, map(string.strip, open("./ck_mc_data").readlines()))
    data = {}

    for line in datafile:
        data[line[0]] = float(line[1])
    #randomize the graph
    R = mcg.mc_randomize_m(G)
    if external:      
      giant_weight_loss, external_weight_loss = compute_external_weight_loss(R,data)
    else:
      giant_weight_loss, external_weight_loss = compute_mean_weight_loss(R,data)
    print " ".join(map(str, [giant_weight_loss, external_weight_loss]))
    


if __name__ == '__main__':
    try:
        import psyco
    except ImportError:
        pass
    external = False
    if len(sys.argv) > 1:
      if sys.argv[1] == "external":
        external = True
    main(external)

