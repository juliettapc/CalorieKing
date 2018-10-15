import sys, os
import math
from numpy import *
import networkx as nx
import string
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from transform_labels_to_nx import *
import operator

class EmpiricalCDF:
	
	def __init__(self, datalist, Dir, filename, key):

		''' 
		class that holds a list of data and returns an empirical cdf 
		defined as p(X>=x). The data are return as a list of tuple (x,y)
		with x representing the value of the variable and y the cumulative probability.

		The plotting method returns a pygrace plot of the cdf toa specified location
		
		datalist: the data to be plotted in a cdf
		Dir:	  the directory where the plot will be saved
		filename: the filename of the .agr file
		key:	  the attribute in the network to be plotted

		'''	 
		
		self.key = key
		self.axis_labels ={}
		self.n = len(datalist)
		self.datalist = datalist
		self.filename = filename
		self.Dir = Dir

		#disctionaries for seting axes and formatting for axes
		self.axis_labels['initial_weight'] = {}
		self.axis_labels['initial_weight']['x_axis'] = "w (lbs)"
		self.axis_labels['initial_weight']['y_axis'] = "P(W>=w)"
		
		self.axis_labels['weight_loss'] = {}
		self.axis_labels['weight_loss']['x_axis'] = "w (lbs)"
		self.axis_labels['weight_loss'] = "P(W>=w)"
		
		self.axis_labels['weigh_ins'] = {}
		self.axis_labels['weigh_ins']['x_axis'] = "n"
		self.axis_labels['weigh_ins']['y_axis'] = "P(N>=n)"
		
		self.axis_labels['activity'] = {}
		self.axis_labels['activity']['x_axis'] = "a"
		self.axis_labels['activity']['y_axis'] = "P(A>=a)"
		
		self.axis_labels['degree'] = {}
		self.axis_labels['degree']['x_axis'] = "k"
		self.axis_labels['degree']['y_axis'] = "P(K>=k)"
		
		self.axis_labels['height'] = {}
		self.axis_labels['height']['x_axis'] = "h (inches)"
		self.axis_labels['height']['y_axis'] = "P(H>=h)"
		
		self.axis_labels['weight_change'] = {}
		self.axis_labels['weight_change']['x_axis'] = "w (lbs)"
		self.axis_labels['weight_change']['y_axis'] = "P(W>=w)"
		
		
		self.axis_labels['days'] = {}
		self.axis_labels['days']['x_axis'] = "n(days)"
		self.axis_labels['days']['y_axis'] = "P(N>=n)"
		
		self.axis_labels['time_in_system'] = {}
		self.axis_labels['time_in_system']['x_axis'] = "t (days)"
		self.axis_labels['time_in_system']['y_axis'] = "P(T>=t)"
		
		self.axis_labels['initial_BMI'] = {}
		self.axis_labels['initial_BMI']['x_axis'] = "b"
		self.axis_labels['initial_BMI']['y_axis'] = "P(B>=b)"
 

		self.axis_labels['final_BMI'] = {}
		self.axis_labels['final_BMI']['x_axis'] = "b"
		self.axis_labels['final_BMI']['y_axis'] = "P(B>=b)"
		
		self.axis_labels['change_in_BMI'] = {}
		self.axis_labels['change_in_BMI']['x_axis'] = "b"
		self.axis_labels['change_in_BMI']['y_axis'] = "P(B>=b)"

		self.axis_labels['percentage_weight_change'] = {}
		self.axis_labels['percentage_weight_change']['x_axis'] = "w"
		self.axis_labels['percentage_weight_change']['y_axis'] = "P(W>=w)"
		
		self.axis_labels['n_weight_change'] = {}
		self.axis_labels['n_weight_change']['x_axis'] = "w"
		self.axis_labels['n_weight_change']['y_axis'] = "P(W>=w)"

		self.axis_format = {}
		
		self.axis_format['initial_weight'] = "F"
		self.axis_format['weight_loss'] = "F" 
		self.axis_format['weigh_ins'] = "F"
		self.axis_format['activity'] = "T"
		self.axis_format['height'] = "F"
		self.axis_format['weight_change'] = "F"
		self.axis_format['days'] = "F"
		self.axis_format['time_in_system'] = "F"
		self.axis_format['initial_BMI'] = "F"
		self.axis_format['percentage_weight_change'] = "F"
		self.axis_format['n_weight_change'] = "F"
		self.axis_format['change_in_BMI'] = "F"

	def cdf_data(self):
			
		data = self.datalist
		self.plotdata = []
		
		try:
			for i in range(data):
				if data[i+1]<data[i]:
					raise ValueError
		except:
			pass

		self.denominator = self.n
		self.bar = dict((i,data.count(i)) for i in set(data))
		self.barlist = [(k,v) for k,v in self.bar.iteritems()]
		self.numbers = [item[0] for item in self.barlist]
		self.numbers.sort()
		self.list_of_counts = [item[1] for item in self.barlist]
		
		self.cumsum =[]
		self.cumsum.append(0.0)
		
		for x in self.list_of_counts:
			self.cumsum.append(self.cumsum[-1] + x if self.cumsum else x)
		
		last_term = self.cumsum[-1]
		
		self.numerator = [last_term-item for item in self.cumsum]
		self.probabilities = [item/last_term for item in self.numerator]
		self.plotdata = zip(self.numbers,self.probabilities)
		
		return self.plotdata
		
	def cdf_plotting(self):
	
		Dir = self.Dir
		data = self.plotdata

		grace = Grace(colors=ColorBrewerScheme('Paired'))
		graph = grace.add_graph()
		graph.set_labels(str(self.axis_labels[self.key]['x_axis']),str(self.axis_labels[self.key]['y_axis']))
		
		dataset1 = graph.add_dataset(data)
		dataset1.line.type = 0
		dataset1.line.color = 1
		dataset1.line.linewidth = 4.0
		dataset1.symbol.fill_color = 'white'
		dataset1.symbol.shape = 1
		dataset1.symbol.size = 0.9
		dataset1.symbol.linewidth = 1.75
		dataset1.symbol.color = 1
		dataset1.symbol.color = 'Paired-5' 
		
		graph.legend.box_color	= 0
		graph.legend.char_size	= 0.85
		graph.legend.loc		= (0.55,0.80)
		
		if self.axis_format[self.key] == "T":
			graph.xaxis.set_log()
		else:
			graph.autoscalex()
		
		graph.yaxis.set_log()

		if self.key == "activity":
			xmaxx = 10000
		else:
			xmaxx = float(math.ceil(float(max(self.datalist))+.1*float(max(self.datalist))))
		if (self.key == "percentage_weight_loss" or self.key =="weight_change" or\
				self.key == "n_weight_loss" or self.key == "percentage_weight_change"):

			xminx =float(math.floor(float(min(self.datalist)+0.1*float((min(self.datalist))))))				   
				
		else:
			xminx = 0.0

		ymin_val = min(data,key = operator.itemgetter(1))

		if ymin_val>=0 and ymin_val<=0.1:
			ymin = 0.1
		elif ymin_val>0.1 and ymin_val<=0.01:
			ymin = 0.01

		elif ymin_val>0.01 and ymin_val<=0.001:
			ymin = 0.001
	
		elif ymin_val>0.001 and ymin_val<=0.0001:
			ymin = 0.0001
		else:
			ymin = 0.00001
		
		xmin,xmax,ymin,ymax = xminx,xmaxx,0.001,1
		print "xmin,xmax, ymin, ymax", xmin, xmax, ymin, ymax

		graph.set_world(xmin,ymin,xmax,ymax)
		#graph.autoscalex()

		graph.xaxis.set_format('decimal',0)
		graph.title.text = str(self.filename)
		graph.title.size = 1.1
		graph.subtitle.size = 0.9
		grace.write_file(Dir+str(self.filename)+'.agr')

class distributions:

	def __init__(self, num_points=5, metric=None, pdir=None,list_of_nodes = [], com_id=None):
		 
		self.num_points = num_points
		self.Dir = "./"+str(num_points)+"_points_network_2010/"
		self.G = nx.read_gml(str(self.Dir)+"data/friend_graph_all_5_2010.gml")
		self.G = transform_labels_to_nx(self.G)
		self.com_id =com_id
		print "nodes", len(self.G.nodes())
		
		self.Gcc = nx.connected_component_subgraphs(self.G)[0]
		self.nodelist = list_of_nodes
		self.metric = metric
		self.pdir = pdir
  
		string_mapping = dict(zip(self.G.nodes(), map(str, self.G.nodes())))
		self.G = nx.relabel_nodes(self.G, string_mapping)

		
		self.nodelist_all = self.G.nodes()	 
		self.nodelist_giant = self.Gcc
		 
		s = set(self.G.nodes())
		t = set(self.Gcc)
		self.nodelist_not_giant = list(s.difference(t))
		print "here is the new node list", len(self.nodelist)
		
		#this is for plotting communities distributions
		
	def plot_comm_distrib(self):

		nodelist = self.nodelist
		data = []
		data_all = []
		data_giant = []
		data_not_giant =[]
		
		for n in nodelist:
			if self.G.node[n][self.metric]:
				data.append(self.G.node[n][str(self.metric)])
	  
		data = map(float,data)

		distobj = EmpiricalCDF(data,pdir,str(self.com_id)+"_"\
				+str(len(self.nodelist))+"_"+str(self.metric)+"_for_"+str(self.num_points)+"_pts"\
				,self.metric)
		
		distobj.cdf_data()
		distobj.cdf_plotting()
		
	def plot_network_distrib(self):
	
		data_all = []
		data_giant = []
		data_not_giant =[]
		
		#all
		for n in self.nodelist_all:
			if self.G.node[n][self.metric]:
				data_all.append(self.G.node[n][str(self.metric)])
		# giant component
		for n in self.nodelist_giant:
			if self.G.node[n][self.metric]:
				data_giant.append(self.G.node[n][str(self.metric)])
		
		# outside of the the giant component
		for n in self.nodelist_not_giant:
			if self.G.node[n][self.metric]:
				data_not_giant.append(self.G.node[n][str(self.metric)])
		
		datasets = [data_all,data_giant,data_not_giant]
		
		for d in datasets:
			#avoid issues with non float values in grace autoscale functions
			d = map(float,d)
			distobj = EmpiricalCDF(d,pdir,str(len(d))+"_"+str(self.metric)+"_for_"+str(self.num_points)+"_pts",self.metric)

			distobj.cdf_data()
			distobj.cdf_plotting()

if __name__ == "__main__":
	
	if len(sys.argv)>1:
		num_points = sys.argv[1]
	else:
		num_points = 5

	if len(sys.argv)>2:
		metric_list = [str(sys.argv[2])]
	else:
		metric_list =["activity"] #, "weight_change",'\
			#'"days","n_weight_change", "percentage_weight_change", "height", "age",\
			#"state", "initial_BMI", "final_BMI"]
			
	new_dir = "./"+str(num_points)+"_points_network_2010/data/"+str(metric_list[0])+"_"+str(num_points)+"/"
	
	try:
		os.mkdir(new_dir)
	except:
		if os.path.exists(new_dir):
			pass
		else:
			raise IOError
	
	pdir = new_dir
	dist = distributions(num_points=num_points,metric=metric_list[0],pdir=pdir)
	dist.plot_network_distrib()
	
	#get community ids 
	communities = open("./"+str(num_points)+"_points_network_2010/data/friend_graph_all0_2010_list_of_communities_Dans_notation").readlines()
	communities = [f.strip().split(";") for f in communities]
	community_list = [x.strip().split(",") for x in communities[0]]
	community_list = sorted(community_list, key=len, reverse=True)
	
	ii=0
	for x in community_list:
		y = map(lambda x:x.strip(),x)
		for s in metric_list:
		
			try:
				os.mkdir(new_dir)
			except:
				if os.path.exists(new_dir):
					pass
				else:
					raise IOError
			
			if len(y)>5:
				pdir  =	 new_dir
				dist = distributions(num_points=num_points,metric=s,pdir=pdir, list_of_nodes=y,com_id=ii)
				dist.plot_comm_distrib()

				print "Plotting distribtion for %s for network with %3d nodes" %(s,len(y))
		ii=ii+1
