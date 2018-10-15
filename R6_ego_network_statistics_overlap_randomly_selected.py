
    cont=0
    for n in G.nodes():
        if len(G.neighbors(n))==0:
            cont=cont+1
   # print "# friendless guys after:", cont


#####################################
def histograma(list,Nbins,dir,name,who):
                      #who es una etiqueta para saber sobre que poblacion hago el histograma

    hist, bin_edges= numpy.histogram(list, bins=Nbins,range=(-45.0,22.0))
#if i wanna compare several distrib. i MUST give same Nbins and max_min range too!!!
   
    #print "max:",max(list),"min:",min(list)
    #print hist, bin_edges

   
    area=0.0
    origin=float(bin_edges[0])
    file = open(dir+name+"_histogram_weight_change_"+who,'wt')
    for b in range (len(bin_edges)-1):        
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0, hist[b], float(hist[b])/float(len(list))

        area=area+float(hist[b])/float(len(list))
        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()



   # print "area for",who,":",area




######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
        main(graph_filename)
    else:
        print "usage: python R6_ego_network_statistics.py path/network_file.gml"

    
