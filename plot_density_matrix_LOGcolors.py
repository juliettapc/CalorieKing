#!/usr/bin/env python


import sys
from PlotGrace import plot_matrix

outfilename="matrix.agr"
colorscheme="YlOrRd"
if len(sys.argv) >= 2:
    outfilename=sys.argv[1]
    if len(sys.argv) >= 3:
        colorscheme = sys.argv[2]

# INPUT MATRIX
mx = []
for rowline in sys.stdin:
    row = map(float, rowline.split())
    mx.append(row)


# format check
num_rows = len(mx)
for row in mx:
    num_cols = len(row)
    if num_rows != num_cols:
        print >> sys.stderr, "Warning! n_rows != n_cols"

# inform size
size = len(mx)
print >> sys.stderr, "<plot_logmatrix> Network size: ", size

plot_matrix(mx, outfilename,
            logcolorbar=True,
            colorscheme=colorscheme,
            reversecolorscheme=True)




