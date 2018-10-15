from transform_labels_to_nx import *
import networkx as nx, sys
from look_up_table import *
from build_friend_graph import *
from bootstrap_module import *
import scipy 
from scipy.stats import *
from scipy import stats

look_up = look_up_table()

def mean(X):
    X = map(float,X)
    return sum(X)/float(len(X))

def frac(X,threshold = -5):    
    value = []
   
    X = list(X)

    for item in X:
        if float(item) < threshold:
            value.append(item)
            
    return (float(len(value))/float(len(X)))*100

class bootstrap_hyp:
    
    def __init__(self,pair, stat, N=1000):      
    
        self.stat = stat
        self.N = N
        self.pair = pair
        
        if self.stat == "mean":
            self.orig_stat = self._true_mean_difference(self.pair)    
        elif self.stat == "frac":
            self.orig_stat = self._true_frac_difference(self.pair)    
        
        print "originat test statistic", self.orig_stat

    def bootstrap(self):
        """ bootstrap algorithm to test for equality of means"""     
                 
        k1,k2 = map(len,self.pair) 
        population = list(itertools.chain(*self.pair))
        population = map(float,population)

        dist_of_stat = [] 
        statistic = []
      
        for i in xrange(self.N):
            
            if self.stat == "frac":
                statistic = self._frac_difference(self._sample_wr(population,k1),\
            self._sample_wr(population,k2))
            
            elif self.stat == "mean":
                statistic = self._mean_difference(self._sample_wr(population,k1),\
            self._sample_wr(population,k2))
            
            dist_of_stat.append(statistic)

        return dist_of_stat
        
    def _true_mean_difference(self, x):
        """calculate the true mean difference between a pair of lists"""           
        return abs(self._mean_difference(x[0],x[1]))
        
    def _true_frac_difference(self, x):
        """calculate the true frac difference between a pair of lists"""
        return self._frac_difference(x[0],x[1])                    
        
    def _mean(self,x):
         
        return float(sum(x)) / float(len(x))

    def _frac(self,X,threshold = -5):    
        
        X = list(X)
        value = []

        for item in X:
            if float(item) < threshold:
                value.append(item)
        
        t = (float(len(value))/float(len(X)))*100
        
        return t
        
    def _mean_difference(self,x,y):
        
        r = self._mean(x)
        s = self._mean(y)
        t = r-s                      
    
        return abs(float(t))
    
    def _frac_difference(self,x,y):
       r = self._frac(x)
       s = self._frac(y)
       t = r - s
       
       return abs(float(t))
               
    def _sample_wr(self,population, k):
        """Chooses k random elements (with replacement) from a population"""
        n = len(population)
        _random, _int = random.random, int  # speed hack 
        result = [None] * k
        for i in xrange(k):
            j = _int(_random() * n)
            result[i] = population[j]
        return list(result)
        
    def _hypothesis_test(self,x,org_stat):
        value = []
        
        for item in x:
            if item >= org_stat:
                value.append(item)
        
        p =  float(len(value))/float(len(x))
        
        return float(p)
        
    def hypo(self):
        """hypothesis test"""      
        
        orig_stat = self.orig_stat
        distrib = self.bootstrap()        
   
        p_value = float(self._hypothesis_test(distrib,orig_stat))
        
        print "p-value = %f for pair with %g and %g" %(p_value,len(self.pair[0]),len(self.pair[1]))
        
        return (len(self.pair[0]),len(self.pair[1]),p_value)


class method3:
    
    """
        method3.py
            
        Created by Rufaro Mukogo on 2011-07-07.
        Copyright (c) 2010 __Northwestern University. All rights reserved.
                
        This script takes the engaged_users_network, and then separates it into gaint and
        small components. After that, the giant is further split into adherent and non-adherent
        The same procedure is carried out for the small components.
        
        Indexing for csv files:
        
        0  - id
        1  - ck_id
        2  - initial_weight
        3  - weigh_ins
        4  - activity
        5  - weight_change
        6  - percentage_weight_change
        7  - time in system
        8  - age
        9  - height
        10 - initial bmi
        11 - final bmi
    """
        
    
    def __init__(self, in_gml, out_dir):
    
        self.G = nx.read_gml(str(in_gml))
        self.G = transform_labels_to_nx(self.G)
        self.dir = out_dir
        print "'self.dir", self.dir
        
        self.header = ["id","ck_id","initial_weight","weigh_ins",\
                    "activity","weight_change","percentage_weight_change","time_in_system",\
                    "age","height", "initial_bmi", "final_bmi"]
        
        self.look_up = look_up_table()
        self.activity = activity_table()

        self.H = self.G.copy()
        
        print "input *gml file", len(self.G)
        selfloops = self.H.selfloop_edges()
    
        for u in selfloops:
            self.H.remove_edge(u[0],u[1])
        
        for n in self.H.nodes():
            if float(self.H.node[n]["initial_weight"])>500 or float(self.H.node[n]["initial_bmi"])>70 or\
                self.H.node[n]["initial_weight"]<100 or float(self.H.node[n]["initial_bmi"])<15:

               self.H.remove_node(n)

        print "size of the cleaned up *gml file", len(self.H)

        nx.write_gml(self.G,str(self.dir)+"/networks/engaged_users_network.gml")

        self.Gcc = nx.connected_component_subgraphs(self.H)[0]
        print "size of the giant component", len(self.Gcc)

        self.sc = set(self.H.nodes()) - set(self.Gcc.nodes())
        print "number of small components", len(self.sc)

    def giant_adherent(self):
        """function to generate giant nonadherent graph"""
        
        look_up = self.look_up
        Gactivity_table = self.activity
        
        H = self.Gcc
        g = open(str(self.dir)+"/csv/adherent_giant.csv","w")
        g1 = open(str(self.dir)+"/csv/adherent_giant_ck_ids.csv","w")
        print>>g, ",".join(map(str,self.header))
        
        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] < 5:
                H.remove_node(n)
        
        nx.write_gml(H,str(self.dir)+"/networks/method3_adherent_giant.gml")


        nodes = map(int,H.nodes())

        print "nodes", nodes

        for n in nodes:
            print look_up["weigh_ins"][n]


        print "length of adherent giant  component", len(H)
        print "length of the giant of the adherent component giant",len(nx.connected_component_subgraphs(H)[0])

        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in nodes]
        
        print "result", result


        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
        
        x = open(str(self.dir)+"/csv/adherent_giant_normal.csv","w")
        y = open(str(self.dir)+"/csv/adherent_giant_overweight.csv","w")
        z = open(str(self.dir)+"/csv/adherent_giant_obese.csv","w")
        
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/adherent_giant_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/adherent_giant_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/adherent_giant_obese_ck_ids.csv","w")
        
        self.over_ad = over
        self.obese_ad = ob
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()
        
        for r in result:      
            print>>g, ",".join(map(str,r))
            print>>g1, r[1]
        g.close()
        g1.close()

        return H, result

    def giant_nonadherent(self):
        """function to generate giant nonadherent graph"""
        
        H = self.G
        Hcc = nx.connected_component_subgraphs(H)[0]
        look_up = self.look_up
        activity_table = self.activity
           
        g = open(str(self.dir)+"/csv/nonadherent_giant.csv","w")
        g1 = open(str(self.dir)+"/csv/nonadherent_giant_ck_ids.csv","w")
        print>>g, ",".join(map(str,self.header))
              
        for n in Hcc.nodes():
            if self.G.node[n]["weigh_ins"] >=5:
                Hcc.remove_node(n)

        print "giant nonadherent", len(Hcc)
        
        nx.write_gml(Hcc,str(self.dir)+"/networks/method3_nonadherent_giant.gml")

        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in list(map(int,Hcc.nodes()))]
        
        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
        
        x = open(str(self.dir)+"/csv/nonadherent_giant_normal.csv","w")
        y = open(str(self.dir)+"/csv/nonadherent_giant_overweight.csv","w")
        z = open(str(self.dir)+"/csv/nonadherent_giant_obese.csv","w")
        
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/nonadherent_giant_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/nonadherent_giant_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/nonadherent_giant_obese_ck_ids.csv","w")
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()

        for r in result:
            print>>g, ",".join(map(str,r))
            print>>g1, r[1]

        print "length of the nonadherent giant", len(Hcc)
        
        g.close()
        g1.close()
        
        return H, result

    def _sc_graph(self):
        """function to create a graph for the small component nodes"""
  
        print "number of small component nodes", len(self.sc)
        look_up = self.look_up
        activity_table = self.activity
        
        uids = [look_up["ck_id"][n] for n in map(int,list(self.sc))]

        print "uids", len(uids)

        obj  = CKGraph()
        self.SC_graph = obj.build_undirected_graph(uids = uids)

        return self.SC_graph[0]

    def sc_adherent(self):
        """function to prune network to produce adherent network for small components"""
        self.sc_graph = self._sc_graph()
        look_up = self.look_up
        activity_table = self.activity
        
        H = self.sc_graph.copy()
        g = open(str(self.dir)+"/csv/adherent_sc.csv","w")
        g1 = open(str(self.dir)+"/csv/adherent_sc_ck_ids.csv","w")
        print>>g, ",".join(map(str,self.header))
         
        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] < 5:
                H.remove_node(n)
        nx.write_gml(H,str(self.dir)+"/networks/method3_adherent_sc.gml")

        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in list(map(int,H.nodes()))]
        
        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30.0, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
        
        x = open(str(self.dir)+"/csv/adherent_sc_normal.csv","w")
        y = open(str(self.dir)+"/csv/adherent_sc_overweight.csv","w")
        z = open(str(self.dir)+"/csv/adherent_sc_obese.csv","w")
        
        self.over_sc = over
        self.obese_sc = ob

       
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/adherent_sc_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/adherent_sc_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/adherent_sc_obese_ck_ids.csv","w")
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()
        
        for r in result:
            print>>g, ",".join(map(str,r))
            print>>g1, r[1]
        
        g.close()
        g1.close()
          
        return H,result

    def sc_nonadherent(self):
        """function to prune network to produce nonadherent network for small components"""
        H = self.sc_graph
        g = open(str(self.dir)+"/csv/nonadherent_sc.csv","w")
        g1 = open(str(self.dir)+"/csv/nonadherent_sc_ck_ids.csv","w")
        print>>g, ",".join(map(str,self.header))
        
        look_up = self.look_up
        activity_table = self.activity
        
        for n in H.nodes():
            if self.G.node[n]["weigh_ins"] >=5:
                H.remove_node(n)
                
        nx.write_gml(H,str(self.dir)+"/networks/method3_nonadherent_sc.gml")

        print "the number of small components that are nonadherent", len(H)

        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in list(map(int,H.nodes()))]
        
        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
        
        x = open(str(self.dir)+"/csv/nonadherent_sc_normal.csv","w")
        y = open(str(self.dir)+"/csv/adherent_sc_overweight.csv","w")
        z = open(str(self.dir)+"/csv/adherent_sc_obese.csv","w")
        
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/adherent_sc_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/adherent_sc_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/adherent_sc_obese_ck_ids.csv","w")
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()
        
        for r in result:
            print>>g, ",".join(map(str,r)) 
            print>>g1, r[1]
        
        g.close() 
        g1.close()
        
        return H, result

    def adherent_not_net(self):

        f = open(str(self.dir)+"/csv/master_adherent.csv", "r")
        g = open(str(self.dir)+"/csv/adherent_not_networked.csv","w")
        g1 = open(str(self.dir)+"/csv/adherent_not_networked_ck_ids.csv","w")     
        print>>g, ",".join(map(str,self.header))
        
        look_up = self.look_up
        activity_table = self.activity
        
        H, r = self.giant_adherent() #r is not used in this step just for unpacking function args
        M, r = self.sc_adherent()   #r is not used in this step
        
        adherent = [x.split(",")[0] for x in f.readlines()[1:]]
        print "adherent", len(adherent)
        ad_not_net = set(adherent) - (set(H.nodes())|set(M.nodes()))
        print "adherent not networked", len(ad_not_net)
     
        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in map(int,ad_not_net)]
       
        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
       

        self.over_ad_not_net = over
        self.obese_ad_not_net = ob

        x = open(str(self.dir)+"/csv/adherent_not_net_normal.csv","w")
        y = open(str(self.dir)+"/csv/adherent_not_net_overweight.csv","w")
        z = open(str(self.dir)+"/csv/adherent_not_net_obese.csv","w")
        
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/adherent_not_net_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/adherent_not_net_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/adherent_not_net_obese_ck_ids.csv","w")
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()
       
        for r in result:
            print>>g, ",".join(map(str,r))
            print>>g1, r[2]

        g.close()
        g1.close()
        f.close()

        return result

    def nonadherent_not_net(self):

        f = open(str(self.dir)+"/csv/master_nonadherent.csv", "r")
        g = open(str(self.dir)+"/csv/nonadherent_not_networked.csv","w")
        g1 = open(str(self.dir)+"/csv/nonadherent_not_networked_ck_ids.csv","w")
        print>>g, ",".join(map(str,self.header))

        D,r = self.giant_nonadherent()
        M,r = self.sc_nonadherent()
        look_up = self.look_up
        activity_table = self.activity
        
        nonadherent = [x.split(",")[0] for x in f.readlines()[1:]]
        print "non adherent network", len(nonadherent)

        nonad_not_net = set(nonadherent) - (set(D.nodes())|set(M.nodes()))
        print "non_adherent_not networked", len(nonad_not_net)
     
        result = [(n, look_up["ck_id"][n],look_up["initial_weight"][n],look_up["weigh_ins"][n],\
        activity_table["activity"][n], look_up["weight_change"][n],look_up["percentage_weight_change"][n],\
        look_up["time_in_system"][n],look_up["age"][n],look_up["height"][n],look_up["initial_bmi"][n],\
        look_up["final_bmi"][n]) for n in map(int,nonad_not_net)]
        
        norm = filter(lambda x: float(x[10]) < 25.0,result)
        over = filter(lambda x: 25< float(x[10]) < 30, result)
        ob = filter(lambda x: float(x[10]) > 30.0,result)
        
        x = open(str(self.dir)+"/csv/nonadherent_not_net_normal.csv","w")
        y = open(str(self.dir)+"/csv/nonadherent_not_net_overweight.csv","w")
        z = open(str(self.dir)+"/csv/nonadherent_not_net_obese.csv","w")
        
        #list of ck_ids for each group 
        xx = open(str(self.dir)+"/csv/nonadherent_not_net_normal_ck_ids.csv","w")
        yy = open(str(self.dir)+"/csv/nonadherent_not_net_overweight_ck_ids.csv","w")
        zz = open(str(self.dir)+"/csv/nonadherent_not_net_obese_ck_ids.csv","w")
        
        bmi_data = 2*[norm,over,ob]
        files = [x,y,z,xx,yy,zz]
        
        #headers
        for ii in range(len(bmi_data)):
            if ii<3:
                print>>files[ii],",".join(map(str,self.header))
    
        #write the csv files to for each set
        for ii in range(len(bmi_data)):
            for n in bmi_data[ii]:
                if ii<3:
                    print>>files[ii],",".join(map(str,n))
                else:
                    print>>files[ii],n[1]
        
        for x in files:
            x.close()
        
        for r in result:
            print>>g, ",".join(map(str,r))
            print>>g1, r[2]

        g.close()
        f.close()
        g1.close()

        return result

    def main(self):
        """function to call all methods required to plot graphs, check the lambda function to make sure that 
           the index matches up with the attribute of interest
           0  - id
           1  - ck_id
           2  - initial_weight
           3  - weigh_ins
           4  - activity
           5  - weight_change
           6  - percentage_weight_change
           7  - time in system
           8  - age
           9  - height
           10 - initial bmi
           11 - final bmi
        """
        
        ad_not_net = self.adherent_not_net()
        ad_not_net = map(lambda x: x[6],ad_not_net)
        print len(ad_not_net)

        H,ad_sc = self.sc_adherent()
        ad_sc = map(lambda x: x[6],ad_sc)
        print len(ad_sc)
        
        H,ad_giant  = self.giant_adherent()
        ad_giant = map(lambda x: x[6],ad_giant)
        print len(ad_giant)
        
        nonad_not_net = self.nonadherent_not_net()
        nonad_not_net = map(lambda x: x[6],nonad_not_net)
        print len(nonad_not_net)
        
        H,nonad_sc = self.sc_nonadherent()
        nonad_sc = map(lambda x: x[6],nonad_sc)
        print len(nonad_sc)
        
        H, nonad_giant = self.giant_nonadherent()
        nonad_giant = map(lambda x: x[6],nonad_giant)
        print len(nonad_giant)
        
        datasets= [nonad_not_net,nonad_sc,nonad_giant,ad_not_net,ad_sc,ad_giant]   
        
        
        bmi_datasets =\
        [self.over_ad_not_net,self.over_sc,self.over_ad,\
        self.obese_ad_not_net,self.obese_sc,self.obese_ad] 

        f = open(str(self.dir)+"/csv/confint_ad_nonad_means_barplots.dat","w")
        g = open(str(self.dir)+"/csv/confint_ad_nonad_frac_barplots.dat","w")
       
        ff = open(str(self.dir)+"/csv/confint_ad_over_obese_means_barplots.dat","w")
        gg = open(str(self.dir)+"/csv/confint_ad_over_obese_frac_barplots.dat","w")
        
        h = open(str(self.dir)+"/csv/sig_test_ad_nonad_means.dat","w")
        i = open(str(self.dir)+"/csv/sig_test_ad_nonad_frac.dat","w")

        hh = open(str(self.dir)+"/csv/sig_test_ad_over_obese_means_barplots.dat","w")
        ii = open(str(self.dir)+"/csv/sig_test_over_obese_frac_barplots.dat","w")
        
        for n in datasets:
        #since the data is negative multiple tby -1 to flip weightloss to a positive number
            d = [float(x) for x in n]
            obj        = bootstrap(d,len(d))
            fractions  = obj.bootstrapCI(frac)
            print>>g, " ".join(map(str,fractions))
            means      = obj.bootstrapCI(mean)
            print>>f, " ".join(map(str,means))
        
        for n in bmi_datasets:
        #since the data is negative multiple tby -1 to flip weightloss to a positive number
            n = map(lambda x: x[6],n)
            d = [float(x) for x in n]
            obj        = bootstrap(d,len(d))
            fractions  = obj.bootstrapCI(frac)
            print>>gg, " ".join(map(str,fractions))
            means      = obj.bootstrapCI(mean)
            print>>ff, " ".join(map(str,means))
        
        for n in itertools.combinations(datasets,2):
            
            n1 = map(lambda x: x[6],n[0])
            a = [float(x) for x in n1]    
            
            n2 = map(lambda x: x[6],n[1])
            b = [float(x) for x in n2]
            
            d = [a,b]
            
            obj_mean   = bootstrap_hyp(d,stat = "mean")
            obj_frac   = bootstrap_hyp(d,stat = "frac")
            
            t = obj_mean.hypo()
            m = obj_frac.hypo()

            print>>h, " ".join(map(str,t))
            print>>i, " ".join(map(str,m))
        
        h.close()
        i.close()

        for n in itertools.combinations(bmi_datasets,2):
            
            #this extracts the correct values for the overweigh and obese user sets
            n1 = map(lambda x: x[6],n[0])
            d = [float(x) for x in n1]    
            
            n2 = map(lambda x: x[6],n[1])
            b = [float(x) for x in n2]
            
            n = [d,b]
            
            obj_mean   = bootstrap_hyp(n,stat = "mean")
            obj_frac   = bootstrap_hyp(n,stat = "frac")
            
            t = obj_mean.hypo()
            m = obj_frac.hypo()

            print>>hh, " ".join(map(str,t))
            print>>ii, " ".join(map(str,m))
        
        hh.close()
        ii.close()

if __name__=="__main__":

    try:
        import psycho
        pyscho.full()

    except ImportError:
        pass

    if len(sys.argv) > 1:
        in_gml = sys.argv[1]
    
    if len(sys.argv) > 2:
        out_dir = sys.argv[2]
    
    obj = method3(in_gml, out_dir)
    obj.main()





