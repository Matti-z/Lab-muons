from xml_parser import xml_digitizer_parser
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os


path = "/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA/"
delta_val = 300

frequency = 2.5e8


timestamp_list = []


def normalize_data( x:np.array ):
    if max(x) - min(x) < delta_val:
        return np.zeros_like(x)
    
    return np.where( x < (max(x) - delta_val) , 1 , 0)

def debug( timestamp, event , time):
    plt.vlines(timestamp , 0 , 2)
    plt.plot(time , event)
    plt.show()

def timestamp_calculator( path: str):
    for id in os.listdir(path):
        print(id)
        data = np.genfromtxt(path+id, delimiter=',')
        data = normalize_data(data)
        step = False
        for i_point , point in enumerate(data):
            if not point:
                step = True
            if point and step:
                step = False
                timestamp_list.append( i_point/frequency )



def save_csv():
    csv_filename = datetime.now().strftime("%Y-%m-%d.csv")
    np.savetxt( csv_filename , timestamp_list , delimiter=",")
                


if __name__ =="__main__":
    timestamp_calculator( path )
    save_csv()
    plt.hist(timestamp_list)
    



