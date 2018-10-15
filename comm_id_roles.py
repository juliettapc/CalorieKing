import subprocess as sp
import networkx as nx
import sys
from transform_labels_to_nx import *
from read_a_gml import *
import itertools

class communities_and_roles:

    """ 
       Created by Rufaro Mukogo and Julia Poncela on 2011-07-20.
       Copyright (c) 2010 __Northwestern University. All rights reserved 
    
       class takes in a .gml file and does community analysis using Roger's algorithm
       and then does the roles analysis and identification. The final output is a gml file 
       that has both roles and communities completely annotated
       
    """
    
    def __init__(self,in_gml,out_gml):
        
        self.in_gml = read_a_gml(self.in_gml)
        self.giant = nx.connected_component_subgraphs(self.in_gml)[0]
        self.giant = self._remove_isolates(self.giant) 
        
        self.new_edges = [' '.join(map(str,e)) for e in self.giant.edges_iter()]
    
    def _remove_isolates(self, G):
    
        m = G.selfloop_edges()
        for u in m:
            G.remove_edge(u[0],u[1])
        
        return G
               
    def _find_communities(self):
    
        p = sp.Popen(["/opt/communityID"], stdin=sp.PIPE, stdout=sp.PIPE)
        output, error = p.communicate("\n".join(self.new_edges))
        community_lines = output.split("part")
        modularity = float(community_lines[0])
        partition_lines = community_lines[1].split("\n")
        self.modules = []
    
        for p in partition_lines:
            this_module = p.split("---")         
            if len(this_module) > 1:
                this_module = this_module[1] # 'this_module' is the list of nodes in the current module
                this_module = map(int, this_module.split())
                self.modules.append(this_module) # list of modules (list of lists)
                self.modules = sorted(self.modules, reverse = False)
                
        self.com_nodes= itertools.chain(*self.modules)
        print "communites", map(len,self.modules)
        
        H = self._annotate_conmmunities(self.giant,self.modules)
         
        return H
        

    def _annotate_communities(self, G, comlist):
        
        """
        function takes a graph object and a list of communities, and then annotates
        the nodes in the graph, based on what community they are in and the size of that community
        
        """
        
        G = G
        comlist = comlist #list of lists with each community
 
        for n in G.nodes():
            self.G.node[n]["community"] = ""
    
        ii = 0
        for co in self.modules:
            s = str(ii)+"_"+str(len(co))
            print "community_size", len(co)
            for n in co:    
                  #add attribute to the main GML file  
                self.G.node[str(n)]["community"] = s
            ii+=1
              
        print self.G.node(data=True)
       
        return G
        
    def _merge_communities(self, G):
        
        """
        function calls another function to merge smaller communities into larger one subject to a cut_off
        """ 
        M = self._merging(self.G)      
        H = self._annotate_communities(M)
        
        return H
        
    def _modularity(self):
        
        """
        Roger's simulated annealing modularity maximization algorithm for community identification
        """
    
        G = self.giant
        current_list_comm=[]
        
        for node in G.nodes():
            if G.node[node]['aux_comm_index'] not in current_list_comm:
                current_list_comm.append(G.node[node]['aux_comm_index'])
    
        number_comm=len (current_list_comm)
        L=float(len(G.edges()))
    
        list_of_lists=[]
        for s in current_list_comm:
            list=[]
            for node in G.nodes():
                if G.node[node]['aux_comm_index']==s:
                    list.append(node)          
            list_of_lists.append(list)
    
        mod=0.0
                
        for comm in list_of_lists:
            
            Subg=G.subgraph(comm)  
            l_s=float(len(Subg.edges())) #number of links among the community

            d_s=0.0
            for node in comm:
                d_s=d_s+float(len(G.neighbors(node)))         
            mod=mod+ l_s/L - (d_s/(2.0*L))*(d_s/(2.0*L))

        return mod 

    def _roles(self,G,coef_layer = 1.5):
    
        """
        Created by Julia Poncela, March 2011
    
        Given a name.gml file of a network with community structure (atributte 'community' of each node indicates to which community it belongs),
        it clasifies the nodes of the GC into different roles,
        according to its connectivity inside/outside its own community.
        
        It modifies the file name.gml with new atributtes for the nodes:
           Within-module degree zscore ('zi')
           Participation coefficient ('Pi')
           The role the node belongs to ('role')
        
        It also genarates a file zscore_vs_ParticipationCoef.dat for the scatter plot of zi vs. Pi
        
        For further detail, see: Cartography of complex networks: modules and universal roles.Guimera, R, Amaral, LAN. J. Stat. Mech.-Theory Exp.,  P02001 (2005).
        """
                       
        
        self.coef_layer = coef_layer
        list_nodes_GC = G.nodes()
    
        num_nodes_GC=int(len(list_nodes_GC))
    
        label_comm=[] #list of community labels
        for i in list_nodes_GC: 
            G.node[i]['zi']=0.0  # i add a new attribute to the nodes
            G.node[i]['Pi']=0.0  # i add a new attribute to the nodes
    
            community_index=G.node[i]['community'].split('_')[0]
            community_size=G.node[i]['community'].split('_')[1]
            
            G.node[i]['community_index']=int(community_index)
            G.node[i]['community_size']=community_size
    
            if G.node[i]['community_index'] not in label_comm:
                label_comm.append(G.node[i]['community_index'])
        
        num_com=int(len(label_comm))
        #print label_comm,len(label_comm)
        
        # calculate the within-module degree zscore (zi):
    
        average_ksi=[] #list of averages of total degree, computed inside each community si
        nodes_in_comm=[] #list of number of nodes for each community si
        deviation=[]  # standard deviation of k in community si
        for i in range(num_com):  # community indexes go from 0 to num_com-1
            average_ksi.append(0.0)
            nodes_in_comm.append(0.0)
            deviation.append(0.0)
       
        for i in list_nodes_GC:  # loop over all nodes in GC         
            average_ksi[G.node[i]['community_index']]=average_ksi[G.node[i]['community_index']]+G.degree(i)
            nodes_in_comm[G.node[i]['community_index']]=nodes_in_comm[G.node[i]['community_index']]+1
              
        for i in range(num_com): 
            average_ksi[i]=average_ksi[i]/nodes_in_comm[i]   
       
        for i in list_nodes_GC:
            deviation[G.node[i]['community_index']]=deviation[G.node[i]['community_index']]+(G.degree(i)-average_ksi[G.node[i]['community_index']])**2
    
        for i in range(num_com):
            deviation[i]=math.sqrt(deviation[i]/nodes_in_comm[i])
    
        for i in list_nodes_GC:   
            ki=0.0
            for node in G.neighbors(i):  # loop over  i's neighbors
                if G.node[i]['community_index']==G.node[node]['community_index']: #if both belong to the same comm
                    ki=ki+1        
            #print  ki, average_ksi[G.node[i]['community_index']],deviation[G.node[i]['community_index']], G.node[i]['community_index'] 
            if  deviation[G.node[i]['community_index']] >0.0:    
                G.node[i]['zi']=(ki-average_ksi[G.node[i]['community_index']])/deviation[G.node[i]['community_index']]
    
        #calculate participation coefficient:
        for i in list_nodes_GC:    
            add=0.0
            for c in range(num_com):  # loop over all communities
                kis=0.0 # number of neighbors of i belonging to comm c
                fraction=0.0     
                for node in G.neighbors(i):   #loop over i's neighbors
                    if G.node[node]['community_index']==c:
                        kis=kis+1.0  
                fraction=(kis/float(G.degree(i)))**2
                add=add+fraction
            G.node[i]['Pi']=1.0-add
    
        num_R1=num_R2=num_R3=num_R4=num_R5=num_R6=num_R7=0
    
    
        #asign a role to each node:
        for i in list_nodes_GC:
            if G.node[i]['zi']>= 2.0: #it is a hub
                if G.node[i]['Pi']< 0.3:
                    G.node[i]['role']='R5'
                    H.node[i]['role']='R5'
    
                elif (G.node[i]['Pi']>= 0.3 and G.node[i]['Pi']< 0.75):
                    G.node[i]['role']='standardR6'
                    H.node[i]['role']='standardR6'
    
                elif  G.node[i]['Pi']>= 0.75:
                    G.node[i]['role']='R7'
    
            else: # it is not a hub
                if G.node[i]['Pi']< 0.05:
                    G.node[i]['role']='R1'
                    H.node[i]['role']='R1'
    
                elif (G.node[i]['Pi']>= 0.05 and G.node[i]['Pi']< 0.65):
                    G.node[i]['role']='R2'
                    H.node[i]['role']='R2'
    
                elif (G.node[i]['Pi']>= 0.65 and G.node[i]['Pi']< 0.8):
                    G.node[i]['role']='R3'
                    H.node[i]['role']='R3'
            
                elif round(G.node[i]['Pi']) >= 0.80:
                   
                    G.node[i]['role']='R4'
                    H.node[i]['role']='R4'
    
        #now i modify the criterium, according to the diff. layers: 
        for i in list_nodes_GC:
    
            if float(G.node[i]['Pi']) >0:
                if (float(G.node[i]['zi']) >= 1.0/(coef_layer*float(G.node[i]['Pi']))): #it is a R6
                    G.node[i]['role']='R6'
                    H.node[i]['role']='R6'
    
                if G.node[i]['zi']>= 10.0: #it is a hub
                    G.node[i]['role']='special_R6'
                    H.node[i]['role']='special_R6'
                      
        #write zscore-Participation to a file
        #keep this but fix directory issue
        file1 = open(dir+info_name2+"_zscore_vs_ParticipationCoef_diff_layers"+str(coef_layer)+".dat",'wt')
    
        for i in list_nodes_GC:
            print >> file1, G.node[i]['Pi'],G.node[i]['zi']
     
        file1.close()
    
        #write the list of lists (communities) sorted by role to a file
        list_roles=["R1","R2","R3","R4","R5","R6","R7"]   
        
        #keep this but address directory issue
        file2 = open(dir+"list_of_communities_"+info_name2+"_by_role",'wt')
        for roles in list_roles:  # loop over roles
            for i in list_nodes_GC: # loop over nodes
                try:            
                    if G.node[i]['role']==roles:
                        # print i,G.node[i]['role']
                        print >> file2, i,
                except KeyError: pass
            
            print >> file2,";",
            
        file2.close()
    
        #write zscore-Participation with info about communities to a file
        file3 = open(dir+info_name2+"_zscore_vs_ParticipCoef_with_comm_info_diff_layers"+str(coef_layer)+".dat",'wt')
    
        for label in label_comm:
            for i in list_nodes_GC:
                if G.node[i]['community_index']==label:
    
                    print >> file3, G.node[i]['Pi'],G.node[i]['zi']
    
            print >> file3,"\n"  # extra line to separate communities
        file3.close()
    
        #create a new gml file with the added atributes:
        nx.write_gml(H,name+"_roles_diff_layers"+str(coef_layer)+".gml")
        
    def _merging(self,G,min_com = 10):

        num_moved_nodes=0
        list_nodes_to_merge=[]
        list_small_comm_index=[]
        
        #sort out this directory issue
       

        #this graph object is from the 
        G = G
        
        
        for node in G.nodes():      
                  
            community_index=int(G.node[node]['community'].split('_')[0])
            community_size=int(G.node[node]['community'].split('_')[1])
    
            G.node[node]['community_index']=community_index
            G.node[node]['aux_comm_index']=G.node[node]['community_index']  #to be modified when trying to merge
    
            #print >> file, node, community_index
    
            if community_size < min_com:  #minimum community size
                list_nodes_to_merge.append(node)
    
                if community_index not in list_small_comm_index:
                    list_small_comm_index.append(community_index)
              
    
        #file.close()
    
        print "initial_mod:",_modularity(G)
    
        list_of_list_small_comm=[]
        for index in list_small_comm_index:
            list=[]
            for node in list_nodes_to_merge:
                if G.node[node]['community_index']==index:
                    list.append(node)
            list_of_list_small_comm.append(list)
    
        print "list of lists of small communities",list_of_list_small_comm
    
        num_loner_comm=0
        list_nodes_to_deal_at_the_end=[]
       
        for small_comm in list_of_list_small_comm:  # i go over every small community
           
            posible_target_comm=[]  #list of all communities the nodes 
                                   #  in that small comm are conected to
            loner_nodes=[]
            for node in small_comm:
                for neighbor in G.neighbors(node):
    
                    if (G.node[neighbor]['community_index'] not in posible_target_comm) and\
                    (G.node[neighbor]['community_index'] not in list_small_comm_index):
                        
                        posible_target_comm.append(G.node[neighbor]['community_index'])
                     
    
            #The exception that one small community is only linked to one small community 
            #at the begining
            
            if len(posible_target_comm) == 0:
                print "communidad de loners!:", small_comm
                for node in small_comm:
                    list_nodes_to_deal_at_the_end.append(node)
                num_loner_comm=num_loner_comm+1
    
         # i reasign nodes of the current small comm. to different one:      
            if len(posible_target_comm)>1:         
                for node in small_comm:               
                    dict_mod={}
                    list_mod=[]
                    for comm_index in posible_target_comm:
                        G.node[node]['aux_comm_index']=comm_index
                        mod=self._modularity(G) #i calculate M with the 'aux_comm_index' of the nodes
                       
                        list_mod.append(mod)
                        dict_mod[mod]=comm_index
                    
                    max_mod=max(list_mod)                
                    index=dict_mod[max_mod]
    
                    G.node[node]['community_index']=dict_mod[mod] #move the node!
                    G.node[node]['aux_comm_index']=dict_mod[mod] #move the node!
                  
                    num_moved_nodes=num_moved_nodes+1
                    list_nodes_to_merge.remove(node)
    
            elif  len(posible_target_comm)==1:  # if there is only one option for the nodes to merge 
                for node in small_comm:
                    G.node[node]['community_index']=posible_target_comm[0]
                    G.node[node]['aux_comm_index']=posible_target_comm[0]
                    num_moved_nodes=num_moved_nodes+1
                    list_nodes_to_merge.remove(node)
    
        posible_target_comm=[]
        for node in list_nodes_to_deal_at_the_end:
            for neighbor in G.neighbors(node):
                if (G.node[node]['community_index'] != G.node[neighbor]['community_index']):
                    posible_target_comm.append(G.node[neighbor]['community_index'])  # if there are several options, it will overwrite!!!
    
        for node in list_nodes_to_deal_at_the_end:
            G.node[node]['community_index']=posible_target_comm[0]
            G.node[node]['aux_comm_index']=posible_target_comm[0]
            num_moved_nodes=num_moved_nodes+1
            list_nodes_to_merge.remove(node)
      
        file = open(dir+"final_comm_idexes",'wt')
        current_list_comm=[]
        for node in G.nodes():        
            print >> file, node, G.node[node]['community_index'] 
            if G.node[node]['community_index'] not in current_list_comm:
                current_list_comm.append(G.node[node]['community_index'])
        file.close()
    
        list_of_lists=[]
        for s in current_list_comm:
            list=[]
            for node in G.nodes():
                if G.node[node]['community_index']==s:
                    list.append(G.node[node]['label']) #node)  ##list of list with labels, not ids!!
                
            list_of_lists.append(list)
    
        #MAKE SURE YOU FIX THE DIRECTORTY ISSUE
        
        file = open(self.dir+"_list_of_lists_merged_communities",'wt')
        print >> file, list_of_lists
        file.close()
    
        element=[]
        for list in list_of_lists:
            element.append(",".join(map(str,list)))
    
            #print element
        string=";".join(map(str,element))
        #print string
        
        file = open(self.dir+"list_of_lists_merged_communities.csv",'wt') 
        print >> file, string 
        file.close()
      
        print  list_nodes_to_merge
        print "\n\n final comm count:\n",len(list_of_lists)
    
        print "final_mod:",self._modularity(G)
        
        return G

    def main(self):
    
        H = self._find_communities()
        G = self._merge_communities(H)
        T = self._roles(G)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        in_gml = sys.argv[1]
    
    if len(sys.argv) > 2:
        out_gml = sys.argv[2]
    print "args", sys.argv[2]

    obj = communities_and_roles(in_gml,out_gml)
    obj.main()
   
