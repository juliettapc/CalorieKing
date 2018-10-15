'''
Created on Sep 27, 2010

@author: rmukogo

This module can be used to calculated the mean and standard deviation of the a list of numbers

'''

def mean(datalist):
    try:
        average = float(sum(datalist))/float(len(datalist))
    except ZeroDivisionError:
        
        average = 0.0
    return average


def stddev(datalist):
    data = datalist
    _mean = mean(data)
   
    t = len(data)

    if t <= 1:

        standard_deviation = ""
    else:

        b = []
        standard_deviation = 0.0
        for n in range((len(data))):
            if data[n] > _mean:
                b.append((data[n]- _mean)**2.0)
            if data[n] < _mean:
                b.append((_mean-data[n])**2.0)
        try:       
            standard_deviation = (sum(b)/float(len(data)-1))**(1.0/2.0)
       
        except ValueError:
            print"someting is very wrong"

    return standard_deviation

