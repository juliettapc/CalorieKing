import ziggy.hdmc as hdmc
import ziggy.hdmc.hdfs as hdfs
import subprocess as sp


hdfs.rm("ten_thou_ints")




input_file_name="5_points_network/data/friend_graph_all0"


p = sp.Popen(["python","communities_CK_GC_same_code_ziggy.py",input_file_name],stdin=sp.PIPE, stdout=sp.PIPE)  #le mando ejecutar otro programa 


salida=p.communicate()  #es una tupla en la q guarda lo que sale 
         # por pantalla en el programa, de la forma: ('todo_lo_que_sea', None)

   

lista=[]
lista=salida[0].split()
    
    
mod=float(lista[0])


print mod








mapping_script = "randomizing_commID_routine.py"#"randints.py"
output_name="ten_thou_ints"
iterations=10
reducer = "comparison_ziggy.py"#"reduce_randints.py"
supporting_files=["GraphRandomization_modified.py"]

hdmc.submit_inline(mapping_script,output_name, iterations,supporting_files,reduction_script=reducer)
