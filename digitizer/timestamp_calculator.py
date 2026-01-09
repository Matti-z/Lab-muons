
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pathlib import Path
from numba import jit


path = str(Path("csv/natale"))
out_path =str(Path('Data/timestamp')) 
delta_val = 500
n = int(5e7)
i = 0
frequency = 2.5e8




def normalize_data( x:np.ndarray ):
    return np.where( x < (max(x) - delta_val) , 1 , 0)

def debug( timestamp, event , time):
    plt.vlines(timestamp , 0 , 2)
    plt.plot(time , event)
    plt.show()


def timestamp_calculator( path: str):
    timestamp_list = np.empty(n , dtype=np.float32)
    i = 0
    file_list = os.listdir(path)
    for id in file_list:
        data = np.genfromtxt(path+"/"+id, delimiter=',' , dtype=np.uint16)
        i = extract_timestamps( data , timestamp_list, i)
        perc: int = int(round(int(id.removesuffix(".csv")) /  int(file_list[-1].removesuffix(".csv")) * 30))
        string: str = (
            "[" + "#" * perc + "-" * (30 - perc) + "]\t" + id + "\t" + str(i))
        print("\r" + string, end="", flush=True)
    return timestamp_list

@jit(nopython=True , parallel=True)
def extract_timestamps(data:np.ndarray, timestamp_list:np.ndarray, i:int):
        # data = normalize_data(data)
    data = np.where( data < (max(data) - delta_val) , 1 , 0)
    step = False
    for i_point , point in enumerate(data):
        if point > max(data) - delta_val:
            step = True
        if point < max(data) - delta_val and step:
            step = False
            timestamp_list[i] = i_point/frequency
            i += 1
            if i == n:
                raise ValueError("array too small")
    return i


def save_csv(timestamp_list , out_path):
    csv_filename = str(Path(out_path))+"/"+ datetime.now().strftime("%Y-%m-%d.csv")
    np.savetxt( csv_filename , timestamp_list , delimiter=",")
            
def timestamp_parser(path , out_path):
    a = timestamp_calculator( path )
    save_csv(a, out_path)


if __name__ =="__main__":
    print(os.path.isdir(path))
    print(os.path.isdir(out_path))
    timestamp_parser(path , out_path)



