import ziggy.hdmc as hdmc
import ziggy.hdmc.hdfs as hdfs

hdfs.rm("ten_thou_ints")

mapping_script = "randints.py"
output_name="ten_thou_ints"
iterations=10000
reducer = "reduce_randints.py"

hdmc.submit_inline(mapping_script,output_name, iterations,reduction_script=reducer)
