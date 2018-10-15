#! /usr/bin/env python

import sys
import networkx as nx

def in_counted_pairs(t,pairs):
	in_pairs = False
	if t in pairs:
		in_pairs = True
	elif (t[1],t[0]) in pairs:
		in_pairs = True
	return in_pairs

def get_na_connections(H):
	total_na = 0
	total_na_a = 0
	total_na_n = 0
	total_aa = 0
	total_nn = 0
	counted_pairs = []
	for n in H.nodes(data=True):
		nbunch = H.neighbors(n[0])
		for v in H.nbunch_iter(nbunch):
			u = H.node[v]
			pair = (n[0],v)
			if not in_counted_pairs(pair, counted_pairs):
				counted_pairs.append(pair)
				if u['type'] == 'N' and n[1]['type'] == 'A':
					total_na += 1
					total_na_a += 1
				elif u['type'] == 'A' and n[1]['type'] == 'N':
					total_na += 1
					total_na_n += 1
				elif u['type'] == 'A' and n[1]['type'] == 'A':
					total_aa += 1
				elif u['type'] == 'N' and n[1]['type'] == 'N':
					total_nn += 1
	results = {"Total Hetero Connections": total_na, "Total NA connections for A": total_na_a,\
	 	"Total NA connections for N": total_na_n, "Total Homo Connections for A": total_aa,\
		"Total Homo Connections for N": total_nn, "Average NA connections": float(total_na)/len(counted_pairs),\
		"Total Connections": H.size()}
	return results
	
def main(graph_file):
	#load the graph
	H = nx.read_gml(graph_file)
	
 	r = get_na_connections(H)
	for result in r:
		print result, r[result]
	
if __name__ == "__main__":
	main(sys.argv[1])