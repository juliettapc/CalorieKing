from transform_labels_to_nx import *
import networkx as nx
import pprint



def look_up_table():

    '''
    dictionary to hold all the attributes for all users in the CalorieKing database
    '''
    
    infile = open("./1_points_network_2010/all_1.csv")
    lines = infile.readlines()
    infile.close()

    data = {}
    header = lambda x: x.strip().strip('"')
    properties = map(header, lines[0].split(","))
    properties = properties[1:-1]

    for p in properties:
        data[p] = {}

    for line in lines[1:]:
        rows = line.split(",")
        id = int(rows[0])
        values = rows[1:]

        for p,v in zip(properties,values):
            data[p][id] = v

    return data
    
data = look_up_table()    

 
def activity_table():

    '''
    dictionary to hold all the activity for all users in the CalorieKing database
    '''
    
    infile = open("./activity_for_all_users.csv")
    lines = infile.readlines()
    infile.close()

    data = {}
    header = lambda x: x.strip().strip('"')
    properties = map(header, lines[0].split(","))
    properties = properties[1:]

    for p in properties:
        data[p] = {}

    for line in lines[1:]:
        rows = line.strip().split(",")
        id = int(rows[0])
        values = rows[1:]

        for p,v in zip(properties,values):
            data[p][id] = v

    return data
 


def mean_value(list,dict=data, property ="percentage_weight_change"):

    count = 0.0
    for n in list:
        try:
            if abs(float(dict[property][int(n)])<50.0):
                count += float(dict[property][int(n)])
                #print count
            else: pass

        except ValueError:
            pass
    try:
        mean = float(count/len(list))
    except ZeroDivisionError:
        mean = 0
        pass
        
    return mean
    
def values(data, list, property ="percentage_weight_change"):

    values = []
    for n in list:
        try:
            if abs(float(data[property][int(n)])<50.0):
                values.append((float(data[property][int(n)]))) 
            else: pass
        except ValueError:
            pass
    return values

def frac(list,threshold = -5, data=data):
    x = values(data, list) 
    value = []   
    for item in x:
        if item < threshold:
            value.append(item)
            
    return (float(len(value))/float(len(list)))*100

if __name__ == '__main__':
    
    look_up = look_up_table()

    pprint.pprint(look_up.keys())

    
    
