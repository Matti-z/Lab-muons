from xml_parser import xml_digitizer_parser
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


path = "digitizer/prova_xml.xml"
delta_val = 50


timestamp_list = []


def normalize_data( x:np.array ):
    if max(x) - min(x) < delta_val:
        return np.zeros_like(x)
    
    return np.where( x > (min(x) + delta_val) , 1 , 0)
    

def debug( timestamp, event , time):
    plt.vlines(timestamp , 0 , 2)
    plt.plot(time , event)
    plt.show()

def timestamp_calculator( path: str):
    events, time , frequency = xml_digitizer_parser(path)
    events = np.array(events)
    print( len(events) )
    if  (not all(len(event) == len(time) for event in events)):
        raise ValueError("something wrong with xml")
    for event in events:
        debug_list = []
        event = normalize_data(event)
        step = False
        for i_point , point in enumerate(event):
            if not point:
                step = True
            if point and step:
                step = False
                debug_list.append(time[ i_point ])
                timestamp_list.append( time[ i_point ] )
        debug( debug_list , event , time)


def save_csv():
    csv_filename = datetime.now().strftime("%Y-%m-%d.csv")
    np.savetxt( csv_filename , timestamp_list , delimiter=",")
                


if __name__ =="__main__":
    timestamp_calculator( path )
    save_csv()



