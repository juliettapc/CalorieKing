import networkx as nx



G=nx.Graph()
print "trying to change Dan's code!"


G.add_edge(1, 2)   

G.add_edge(3, 2)   

G.add_edge(1, 3)   

G.add_edge(1, 5)   


G.add_edge(5,4)   


G.add_edge(4,6)   

G.add_edge(5,6)   


G.add_edge(3,7)   


G.add_edge(3,10)   


G.add_edge(10,11)   


G.add_edge(10,13)   


G.add_edge(12,13) 

G.add_edge(11,12) 

G.add_edge(10,12) 

G.add_edge(11,13)  


G.add_edge(7,8)   


G.add_edge(7,9)  

G.add_edge(9,8)   



lista=list(nx.find_cliques(G))

print lista

a=len(lista)

print  'tamagno de la lista:'
print  a

for i in range(a):
  
  print 'mayor elmen:'
  print max(lista)

  c= max(lista)

  b=lista.index(c) #devuelve el indice del elemento c de la lista  

  print b

  del lista[b]        #borro el elem cuyo indice es b

  print 'borrado elem mayor de la lista'



print 'all done'
