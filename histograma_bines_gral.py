#! /usr/bin/env python


import numpy


def histograma_bins(lista,Nbins, name_h):
                      

    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(float(min(lista)),float(max(lista))))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*500000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas=[]
    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        #if  hist[b] !=0:
        print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/float(len(lista)),float(hist[b])/(float(len(lista))*bin_size),  float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b]),  float(hist[b])/float(len(lista))       
        tupla=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(hist[b])/(float(len(lista))*bin_size))
        lista_tuplas.append(tupla)
        
       

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   
 #   print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size), cumul_prob (normalization by N events only)"
   
    print "written file:", name_h


    return lista_tuplas



def histograma_bins_return_only_freq(lista,Nbins, name_h):
                      

    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(float(min(lista)),float(max(lista))))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
  #  print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*50000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
   
    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        if  hist[b] !=0:
            print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b])/float(len(lista)),float(Cumul_prob[b])     
      

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   
    print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size)"
   
    return hist


def histograma_bins_return_prob_and_cumul(lista,Nbins, name_h):
                      

    hist, bin_edges= numpy.histogram(lista, bins=Nbins, range=(float(min(lista)),float(max(lista))))  # optional: range=( , ) The lower and upper range of the bins.
#if i wanna compare several distrib. i MUST give same Nbins and (max,min) range too!!!
   
  #  print "\n",name_h,"max:",max(lista),"min:",min(lista)
   


    Cumul_prob=[0]*50000
    norm=0.
    for item in lista:
        for b in range (len(bin_edges)): 
            value_bin=bin_edges[b]
            if value_bin<= item:
                Cumul_prob[b]+=1.
        norm+=1.




  #  print  "bin size:", bin_edges[1]-bin_edges[0],  bin_edges[2]-bin_edges[1],  bin_edges[3]-bin_edges[2]
    bin_size=float(bin_edges[1]-bin_edges[0])

# ojoooooo! normalizar tb por bin size, ademas de N puntos
    
    lista_tuplas_prob=[]
    lista_tuplas_cumulat_prob=[]

    origin=float(bin_edges[0]) 
    file = open(name_h,'wt')
    for b in range (len(bin_edges)-1):    
        if  hist[b] !=0:
            print >> file,origin+(bin_edges[b+1]-bin_edges[b])/2.0,  float(hist[b])/(float(len(lista))*bin_size), float(hist[b]),float(Cumul_prob[b])/(float(len(lista))*bin_size),float(Cumul_prob[b])/float(len(lista)),float(Cumul_prob[b])

        
        tupla_prob=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(hist[b])/(float(len(lista))*bin_size))
        tupla_cumulat=(origin+(bin_edges[b+1]-bin_edges[b])/2.0, float(Cumul_prob[b])/(float(len(lista))*bin_size))

        lista_tuplas_prob.append(tupla_prob)
        lista_tuplas_cumulat_prob.append(tupla_cumulat)
      
       

        origin=origin+(bin_edges[b+1]-bin_edges[b])
    file.close()
   
    print "written:", name_h, "  colum names:  norm_prob, raw_count, cumul_prob, raw_cumul_count  (normalization by N events times bin_size)"
   
    return lista_tuplas_prob,lista_tuplas_cumulat_prob

