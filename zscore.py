import sys
import math


def main(iteraciones):

    data=[]

    mod_list=[]
    average_modularity=0.0    
    for i in range(int(iteraciones)): # leo los ficheros rand_summary_modularity... y hago la media
        name='rand_summary_modularity_analysis'+str(i)
        file = open(name).readlines()  #devuelve una lista, cuyos elem son las lineas del fichero leido
       

        cadena=str(file[0])

        #data.append(file)
        lista=cadena.split(" ") #devuelve una lista, cuyos elem son el resultado de saparar cadena[0], usando los espacios en blanco que contuviera
        #print cadena, lista
        average_modularity=average_modularity+float(lista[3])
        print i,lista[3]

        mod_list.append(lista[3])


    average_modularity=average_modularity/float(iteraciones)
    print "<M>:",average_modularity


    sigma=0.0
    for i in range(int(iteraciones)):
        sigma=sigma+(float(mod_list[i])-average_modularity)**2


    sigma=sigma/float(iteraciones)
    sigma=math.sqrt(sigma)
    print "sigma:", sigma

    mod=0.5
    zscore=(average_modularity-mod)/sigma

    print "zscore:",zscore




if __name__ == "__main__":
    if len(sys.argv) >1:
        iteraciones=sys.argv[1]
    main(iteraciones)
