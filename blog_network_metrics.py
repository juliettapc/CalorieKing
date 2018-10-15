import networkx as nx
from numpy import *
from empirical_cdf_class import EmpiricalCDF
from database import *
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from network_structure_color import *


class DBConnection(object):
    
    def __init__(self, server="tarraco.chem-eng.northwestern.edu", user="calorieking", passwd="n1ckuDB!"):
        self.database = "calorie_king_social_networking"
        self.db = Connection(server, self.database, user, passwd)
        
    def query(self, q_string):
        return self.db.query(q_string)

class baseline:

    def __init__(self):
        

        self.G = nx.read_gml("./Blog_comments_network/data/blog_graph_all.gml")
        self.Gprime = nx.read_gml("./5_points_network/data/friend_graph_all0.gml") 

        self.db = DBConnection()
        self.num_points =  5
        self.blogs = self.db.query("SELECT DISTINCT bc.owner_id from blog_comments AS bc")

        #blog owner ckids
        self.blog_owners = [x.values() for x in self.blogs]
        self.blog_owners = reduce(lambda x,y: x+y,self.blog_owners) 
        print self.blog_owners

    def overlap(self):
        """
        calculate the fraction of friendships in one network that are also found in the 
        frienship network
        """
        friend_graph = self.Gprime.edges()
        blog_graph = self.G.edges()
        frac = len(set(friend_graph)&set(blog_graph))/float(len(blog_graph))
        
        print "fractions of blog friendships that are in the friend network:", frac
    
        return frac

    def avg_num_posts(self):
        
        blogs = self.blog_owners
        b_posts_list = []

        for ck in blogs:
            
            posts = self.db.query("SELECT COUNT(poster_id) from blog_comments where owner_id = '"+str(ck)+"'")
            
            try:
                b_posts_list.append(posts[0]['COUNT(poster_id)'])
            except IndexError: pass

        f = open("./Blog_comments_network/data/data_to_plot_posting distribution.dat","w")

        for x in b_posts_list:
            print>>f, float(x)

        f.close()
        
        self.avg_posts = mean(b_posts_list)
        self.std_posts = std(b_posts_list)
        

        print "average number of posts", self.avg_posts
        print "std of the number of posts", self.std_posts

        self.b_plots_list = b_posts_list

        return self.avg_posts, self.std_posts


    def dist_num_posts(self):

        dist = EmpiricalCDF(self.b_plots_list,"./Blog_comments_network/plots/"\
                ,"distribution_of_number_blog_posts"," posts (n)", "P(N>=n)")

        self.data = dist.cdf_data()

    def _dist_formatting(self):

        Dir = "./Blog_comments_network/plots/"
        self.filename= "distribution_of_number_of_blog_com_on_each_blog"
            
        data = self.data

        grace = Grace(colors=ColorBrewerScheme('Paired'))
        graph = grace.add_graph()
        graph.set_labels("posts (n)", "P(N>=n)")
        
        dataset1 = graph.add_dataset(data)
        dataset1.line.type = 0
        dataset1.line.color = 1
        dataset1.line.linewidth = 4.0
        dataset1.symbol.fill_color = 'white'
        dataset1.symbol.shape = 1
        dataset1.symbol.size = 0.7
        dataset1.symbol.color = 1
        dataset1.symbol.color = 'black' 
        
        graph.legend.box_color  = 0
        graph.legend.char_size  = 0.85
        graph.legend.loc        = (0.55,0.80)
        
        graph.yaxis.set_log()
        graph.xaxis.set_log()
        
        #graph.autoscaley()
        #graph.autoscalex()
        
        xmin,xmax,ymin,ymax = 0.80,10000,0.00001,1
       
        graph.set_world(xmin,ymin,xmax,ymax)
        graph.xaxis.set_format('decimal',0)
        
        graph.title.text = str(self.filename)
        graph.subtitle.text = ("average="+str(self.avg_posts)+"std="+str(self.std_posts))
        graph.title.size = 1.2
        graph.subtitle.size = 0.8
        
        grace.write_file(Dir+str(self.filename)+'.agr')
    
    def plot_degree(self):

        degree = nx.degree(self.G)

        dist = EmpiricalCDF(self.b_plots_list,"./Blog_comments_network/plots/"\
        ,"degree_distribution"," degree (k)", "P(K>=k)")



    def plot_network_graph(self):
        main("./5_points_network/data/blog_pm_graph_5pts.gml") 

if __name__ =="__main__":

    obj = baseline()
    obj.overlap()
    obj.avg_num_posts()
    obj.dist_num_posts()
    obj._dist_formatting()
    obj.plot_network_graph()
    obj.plot_degree()     
