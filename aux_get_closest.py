lista=[14,28,42,56]
number=57

closest=lista[0]
minimo=0
for i in range(len(lista)):
    if number <= lista[i] and number > minimo:
        closest=lista[i]
        minimo=lista[i]
        
print closest
