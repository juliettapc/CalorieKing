import networkx as nx
import numpy, os, sys, random
from look_up_table import *
from transform_labels_to_nx import *


class more_annotations():
    """
    class to add any native attributes, that is attributes that are contained in the database, such
    as the number of weigh_ins or join_date, height, state, etc
    """

    def __init__(self,in_gml,out_gml, metric, look_up_table):

        self.in_gml  = str(in_gml)
        self.out_gml = str(out_gml)
        self.metric  = str(metric)
        self.look_up_table = look_up_table

    def _annotate(self):

        G = nx.read_gml(self.in_gml)
        G = transform_labels_to_nx(G)

        print G.nodes()

        for n in G.nodes():
            try:
                if G.node[n][self.metric]:
                    G.node[n][self.metric] = ""
            except:
                KeyError

            G.node[n][self.metric] = int(self.look_up_table[self.metric][int(n)])

        nx.write_gml(G,out_gml)

    def main(self):
        self.look_up_table
        self._annotate()

if __name__=="__main__":

    try:
        import psycho
        pyscho.full()
    except:
        ImportError

    if len(sys.argv) > 1:
        in_gml = sys.argv[1]

    if len(sys.argv) > 2:
        out_gml = sys.argv[2]

    if len(sys.argv) > 3:
        metric = sys.argv[3]

    print "in_gml", in_gml
    print "out_gml", out_gml
    print "metric", metric


    look_up_table = look_up_table()

    obj = more_annotations(in_gml,out_gml,metric,look_up_table)
    obj._annotate()
    obj.main()

