from transform_labels_to_nx import *
import networkx as nx

G = nx.read_gml("./5_points_network_2010/data/friend_graph_all.gml")
G = transform_labels_to_nx(G)
H = G.copy()
#remove nodes with more than 5  weigh ins
#print "before", len(H)

Gcc = nx.connected_component_subgraphs(G)[0]
H = Gcc.copy()

non_ad = []

for n in G.nodes():
    if int(G.node[n]['weigh_ins'])<5:
        non_ad.append(n)
    else:
        pass

#print sorted(map(int,non_ad)

#for n in H.nodes():
#    if int(H.node[n]['weigh_ins'])>=5:
#        H.remove_node(n)
#    else:
#        pass

for n in H.nodes():
    if int(H.node[n]['time_in_system'])<=100:
        H.remove_node(n)
    else:
        pass

print "networked  adherent",sorted( map(int,H.nodes()))

#print "after", len(H)

nx.write_gml(G,"./1_points_network_2010/friend_graph_adherent.gml")

nx.write_gml(H,"./1_points_network_2010/friend_graph_adherent_100.gml")
