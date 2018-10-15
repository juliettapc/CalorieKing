#! /usr/bin/env python

class CKSummary(object):
	
	def __init__(self, graph, summary_size = 10):
		#build a networkx graph of the candidates
        if not graph_file:
            ckg = CKGraph()
            self.graph = ckg.build_undirected_graph(uids=uids, write=False)[0]
        else:
            if ".gml" in graph_file:
                self.graph = nx.read_gml(graph_file)
                self.graph = nx.Graph(self.graph.to_undirected())
            else:
                self.graph = nx.read_edgelist(graph_file)
            self.graph = nx.relabel_nodes(self.graph, dict(zip(self.graph.nodes(),map(int, self.graph.nodes()))))
        #extract only the giant component
        self.output = {}

	def _build_output_row(self, entry_key, entry):
	    #entries are structures: node, metric, neighbor1:neighbor2:
	    entry_list = [entry_key,entry[0],":".join(map(str, entry[1]))]
	    return ",".join(map(str,entry_list))

	def build_output_data(self, nodes, metric_name):
	      """add a new metric to the output hash"""
	      self.output[metric_name] = []
	      for key in nodes:
	          self.output[metric_name].append(self._build_output_row(key, nodes[key]))
	
	def build_summary(self):