#! /usr/bin/env python

import numpy as n
import sys
import scipy.sparse as sparse
import scipy.interpolate
import scipy.ndimage
from shakey_greedy_sort import ShakeyGreedySort

def make_node_entry(row_number,row):
	return '{nodeName: "'+str(row_number)+'", group:'+str(int(n.max(row)))+'},\n'

def make_node_list(m):
	node_list_head = 'nodes:[\n'
	for row in range(m.shape[0]):
		node_list_head += make_node_entry(row,m[row,:])
	node_list_head += '],'
	return node_list_head
	
def make_link_list(m):
	m = sparse.lil_matrix(m)
	link_list_head = '\nlinks:[\n'
	#because this is a sparse matrix, I know that m.rows contains the 
	for row in range(m.shape[0]):
		for col in m.rows[row]:
			link_list_head += '{source:'+str(row)+', target:'+str(col)+',value:'+str(m[row,col]*4)+'},\n'
	link_list_head += ']\n'
	return link_list_head

	

def make_javascript_matrix(filename):
	m = n.load(filename)['arr_0']*4
	if m.shape[0] > 200:
		m = congrid(m,(100,100),method='neighbour')
	sg_sort = ShakeyGreedySort()
	l = sg_sort.sparse_to_lines(sparse.lil_matrix(m))
	mx,links = sg_sort.make_dict_matrix(l)
	t,c = sg_sort.sort(mx,links,m.shape[0])
	new_m = sg_sort.transtable_to_coo(c,m.shape[0])
	new_m = new_m.toarray()
	
	header = 'var coclassification = {\n'
	nodes = make_node_list(new_m)
	links = make_link_list(new_m)
	header += nodes
	header += links
	header += '};'
	return header
	
def congrid(a, newdims, method='linear', centre=False, minusone=False):
    '''Arbitrary resampling of source array to new dimension sizes.
    Currently only supports maintaining the same number of dimensions.
    To use 1-D arrays, first promote them to shape (x,1).

    Uses the same parameters and creates the same co-ordinate lookup points
    as IDL''s congrid routine, which apparently originally came from a VAX/VMS
    routine of the same name.

    method:
    neighbour - closest value from original data
    nearest and linear - uses n x 1-D interpolations using
                         scipy.interpolate.interp1d
    (see Numerical Recipes for validity of use of n 1-D interpolations)
    spline - uses ndimage.map_coordinates

    centre:
    True - interpolation points are at the centres of the bins
    False - points are at the front edge of the bin

    minusone:
    For example- inarray.shape = (i,j) & new dimensions = (x,y)
    False - inarray is resampled by factors of (i/x) * (j/y)
    True - inarray is resampled by(i-1)/(x-1) * (j-1)/(y-1)
    This prevents extrapolation one element beyond bounds of input array.
    '''
    if not a.dtype in [n.float64, n.float32]:
        a = n.cast[float](a)

    m1 = n.cast[int](minusone)
    ofs = n.cast[int](centre) * 0.5
    old = n.array( a.shape )
    ndims = len( a.shape )
    if len( newdims ) != ndims:
        print "[congrid] dimensions error. " \
              "This routine currently only support " \
              "rebinning to the same number of dimensions."
        return None
    newdims = n.asarray( newdims, dtype=float )
    dimlist = []

    if method == 'neighbour':
        for i in range( ndims ):
            base = n.indices(newdims)[i]
            dimlist.append( (old[i] - m1) / (newdims[i] - m1) \
                            * (base + ofs) - ofs )
        cd = n.array( dimlist ).round().astype(int)
        newa = a[list( cd )]
        return newa

    elif method in ['nearest','linear']:
        # calculate new dims
        for i in range( ndims ):
            base = n.arange( newdims[i] )
            dimlist.append( (old[i] - m1) / (newdims[i] - m1) \
                            * (base + ofs) - ofs )
        # specify old dims
        olddims = [n.arange(i, dtype = n.float) for i in list( a.shape )]

        # first interpolation - for ndims = any
        mint = scipy.interpolate.interp1d( olddims[-1], a, kind=method )
        newa = mint( dimlist[-1] )

        trorder = [ndims - 1] + range( ndims - 1 )
        for i in range( ndims - 2, -1, -1 ):
            newa = newa.transpose( trorder )

            mint = scipy.interpolate.interp1d( olddims[i], newa, kind=method )
            newa = mint( dimlist[i] )

        if ndims > 1:
            # need one more transpose to return to original dimensions
            newa = newa.transpose( trorder )

        return newa
    elif method in ['spline']:
        oslices = [ slice(0,j) for j in old ]
        oldcoords = n.ogrid[oslices]
        nslices = [ slice(0,j) for j in list(newdims) ]
        newcoords = n.mgrid[nslices]

        newcoords_dims = range(n.rank(newcoords))
        #make first index last
        newcoords_dims.append(newcoords_dims.pop(0))
        newcoords_tr = newcoords.transpose(newcoords_dims)
        # makes a view that affects newcoords

        newcoords_tr += ofs

        deltas = (n.asarray(old) - m1) / (newdims - m1)
        newcoords_tr *= deltas

        newcoords_tr -= ofs

        newa = scipy.ndimage.map_coordinates(a, newcoords)
        return newa
    else:
        print "Congrid error: Unrecognized interpolation type.\n", \
              "Currently only \'neighbour\', \'nearest\',\'linear\',", \
              "and \'spline\' are supported."
        return None
	
if __name__ == "__main__":
	js = make_javascript_matrix(sys.argv[1])
	f = open("coclassification.js","w")
	print >> f, js
	f.close()