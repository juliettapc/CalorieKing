import subprocess as sp

edge_data = open("calorie_king_friends_no_staff_undirected_giant_month8").readlines()

#for linea in edge_data:
 #   print linea            con esto imprimiria el fichero que acabo de leer


p = sp.Popen(["/opt/communityID"], stdin=sp.PIPE, stdout=sp.PIPE)
output, error = p.communicate("".join(edge_data))
community_lines = output.split("part")
modularity = float(community_lines[0])
partition_lines = community_lines[1].split("\n")
modules = []
for p in partition_lines:
    this_module = p.split("---")
    if len(this_module) > 1:
        this_module = this_module[1]
        this_module = map(int, this_module.split())
        modules.append(this_module)
            
output_string = str(modularity) +":\n" #imprimo la modularidad y salto de linea
for s in modules:
    module_string = ",".join(map(str,s))
    output_string += module_string + ";\n" # imprimo los elem de cada comunidad, separados por ; y salto de linea
                
#print output_string.rstrip(";")
print output_string
