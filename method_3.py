from transform_labels_to_nx import *
import networkx as nx, sys
from look_up_table import *
from build_friend_graph import *

look_up = look_up_table()

class method3:
    """This script takes the engaged_users_network, and then separates it into gaint and
        small components. After that, the giant is further split into adherent and non-adherent
        The same procedure is carried out for the  small components"""

    def __init__(self, in_gml):
        self.G = nx.read_gml(str(in_gml))
        self.G = transform_labels_to_nx(self.G)

        H = self.G.copy()

        self_loop_nodes = []
        for u,v in H.edges_iter():
            if int(u)==int(v):
                self.G.remove_edge(u,v)
                self_loop_nodes.append(u)

        for n in self_loop_nodes:
            if len(H.neighbors(n)) <=1:
                self.G.remove_node(n)

        print "size of the cleaned up *gml file", len(self.G)
        print "size of overall network", len(self.G)

        nx.write_gml(self.G,"./method3/networks/engaged_users_network.gml")

        self.Gcc = nx.connected_component_subgraphs(self.G)[0]
        print "size of the giant component", len(self.Gcc)

        self.sc = set(self.G.nodes()) - set(self.Gcc.nodes())
        print "number of small components", len(self.sc)

    def giant_adherent(self):
        """function to generate giant nonadherent graph"""

        H = self.Gcc
        
        g = open("./method3/csv/adherent_giant_pwl.csv","w")
 
        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] < 5:
                H.remove_node(n)
        nx.write_gml(H,"./method3/networks/method3_adherent_giant.gml")

        print "length of adherent giant  component", len(H)
        print "length of the giant of the adherent component giant",len(nx.connected_component_subgraphs(H)[0])

        result = [(n,look_up["percentage_weight_change"][n]) for n in map(int,H.nodes())]

        for r in result:
            
            print>>g, r[0],",",r[1] 

        g.close()

        return H

    def giant_nonadherent(self):
        """function to generate giant nonadherent graph"""
        H = self.G

        Hcc = nx.connected_component_subgraphs(H)[0]

        g = open("./method3/csv/nonadherent_giant_pwl.csv","w")
         

        for n in Hcc.nodes():
            if self.G.node[n]["weigh_ins"] >=5:
                Hcc.remove_node(n)

        print "should be 68", len(Hcc)
        

        nx.write_gml(Hcc,"./method3/networks/method3_nonadherent_giant.gml")

        result = [(n,look_up["percentage_weight_change"][n]) for n in map(int,Hcc.nodes())]
        
        for r in result:
            print>>g, r[0],",",r[1] 

        print "length of the nonadherent giant", len(Hcc)
        
        g.close()
         
        return H

    def _sc_graph(self):
        """function to create a graph for the small component nodes"""
        #sc = set(self.G.nodes()) - set(self.Gcc.nodes())
        print "number of small component nodes should be 316", len(self.sc)
        look_up = look_up_table()
        uids = [look_up["ck_id"][n] for n in map(int,list(self.sc))]

        print "uids should be 316", len(uids)

        obj  = CKGraph()
        self.SC_graph = obj.build_undirected_graph(uids = uids)

        return self.SC_graph[0]

    def sc_adherent(self):
        """function to prune network to produce adherent network for small components"""
        self.sc_graph = self._sc_graph()

        H = self.sc_graph.copy()
        g = open("./method3/csv/adherent_sc_pwl.csv","w")
         

        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] < 5:
                H.remove_node(n)
        nx.write_gml(H,"./method3/networks/method3_adherent_sc.gml")

        
        result = [(n,look_up["percentage_weight_change"][n]) for n in map(int,H.nodes())]
        result = [ [str(r[0]),str(r[1])] for r in result ]
         

        for r in result:
            print>>g, r[0],",",r[1]
        
        g.close()
          
        return H

    def sc_nonadherent(self):
        """function to prune network to produce nonadherent network for small components"""
        H = self.sc_graph
        g = open("./method3/csv/nonadherent_sc_pwl.csv","w")

        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] >=5:
                H.remove_node(n)
        nx.write_gml(H,"./method3/networks/method3_nonadherent_sc.gml")

        print "the number of small components that are nonadherent", len(H)

        result = [(n,look_up["percentage_weight_change"][n])for n in map(int,H.nodes())]
        result = [ [str(r[0]),str(r[1])] for r in result ]
         
        for r in result:
            print>>g, r[0],",",r[1] 
        
        g.close() 
        
        return H

    def adherent_not_net(self):

        f = open("./master_adherent.csv", "r")
        g = open("./method3/csv/adherent_not_networked_pwl.csv","w")

        H = self.giant_adherent()
        M = self.sc_adherent()
        adherent = [x.split(",")[0] for x in f.readlines()[1:]]
        print "adherent should be 11242", len(adherent)
        ad_not_net = set(adherent) - (set(H.nodes())|set(M.nodes()))
        print "adherent not networked should be 9885", len(ad_not_net)
     
        result = [(n,look_up["percentage_weight_change"][n]) for n in map(int,ad_not_net)]
        result = [ [str(r[0]),str(r[1])] for r in result ]
         

        for r in result:
            print>>g, r[0],",",r[1] 

        g.close()
        f.close()

        return ad_not_net

    def nonadherent_not_net(self):

        f = open("./master_nonadherent.csv", "r")
        g = open("./method3/csv/nonadherent_not_networked_pwl.csv","w")
        D = self.giant_nonadherent()
        M = self.sc_nonadherent()
        nonadherent = [x.split(",")[0] for x in f.readlines()[1:]]
        print "non adherent network", len(nonadherent)

        nonad_not_net = set(nonadherent) - (set(D.nodes())|set(M.nodes()))
        print "non_adherent_not networked", len(nonad_not_net)
     
        result = [(n,look_up["percentage_weight_change"][n]) for n in map(int,nonad_not_net)]

        result = [ [str(r[0]),str(r[1])] for r in result ]

        for r in result:
            print>>g, r[0],",",r[1] 

        g.close()
        f.close()

        return nonad_not_net

    def main(self):
        """function to call all methods required to plot graphs"""
        self.adherent_not_net()
        self.nonadherent_not_net()

if __name__=="__main__":

    try:
        import psycho
        pyscho.full()

    except ImportError:
        pass

    if len(sys.argv) > 1:
        in_gml = sys.argv[1]

    obj = method3(in_gml)
    obj.main()





