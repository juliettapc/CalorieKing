if len(posible_target_comm) == 0:
  print "communidad de loners!"

  for node in small_comm:
                for neighbor in G.neighbors(node):
                    print G.node[node]['community_index'],G.node[neighbor]['community_index'],"new_address:",G.node[neighbor]['aux_comm_index']
                    raw_input()
                    if (G.node[neighbor]['community_index'] != G.node[node]['community_index']) and (G.node[neighbor]['community_index'] not in posible_target_comm ) and (G.node[neighbor]['community_index'] not in list_small_comm_index):
                        
                        posible_target_comm.append(G.node[neighbor]['community_index'])
                        print "node", node,"connected to:", neighbor, "so, targent comm:", G.node[neighbor]['community_index']
                        
                    else: 
                        print "not gonna happen!"       
                        raw_input()
            print posible_target_comm
    

 
    
