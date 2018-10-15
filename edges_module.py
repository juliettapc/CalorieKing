#!/usr/bin/env python
"""
The module returns the pairwise combinations of all intergers in a sequence, without duplicates

created by Rufaro Mukogo NOrthwestern University 2011-02-27

"""

def perm(seq):

    combination = []

    for i in range(len(seq)):
        for j in range(i,len(seq)):

            if seq[i]==seq[j]:
                pass
            else:
                combination.append((seq[i],seq[j]))

    #print "combination", combination
    return combination

if __name__=="__main__":
    pass

