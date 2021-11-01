import json
import numpy

variableOrder = ['gyrox', 'gyroy', 'gyroz'] 

def parse(f):
    with open(f,'r') as load_f:
        load_dict = json.load(load_f)
    
    records = {}
    for entry in load_dict:
        time, value, variable = entry['time'], entry['value'], entry['variable']
        realTime = time[:-3]
        try:
            records[realTime][variable] = value
        except KeyError:
            records[realTime] = {variable:value}
    records = sorted(records.items(), key=lambda x: x[0], reverse=False)
    data = []
    """ states
        0: not reading data
        1: reading when key1 = 1
        2: reading data
        3: reading when key1 = 0
    """
    state = 0
    for item in records:
        if("key1" not in item[1].keys()):
            item[1]['key1'] = 0
        if(state == 0):
            if(int(item[1]['key1']) == 1):
                state = 1
        elif(state == 1):
            if(int(item[1]['key1']) == 0):
                state = 2
        elif(state == 2):
            if(int(item[1]['key1']) == 1):
                state = 3
        else:
            if(int(item[1]['key1']) == 0):
                state = 0
        if(state != 0):
            data.append([item[1][name] for name in variableOrder])
    return numpy.mat(data)

def main():
    data = parse("export.json")
    print(data)

if __name__ == "__main__":
    main()