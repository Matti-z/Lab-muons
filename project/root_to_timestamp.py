import uproot
import os.path
import numpy as np
import matplotlib.pyplot as plt

delta = 500

def timestamp_calculator(vec:np.ndarray , frequency:float , dT_ptrigg: float , csv_filename:str):
    if not os.path.isfile(csv_filename):
        if "/" in csv_filename:
            print("creating directories:\t" , os.path.dirname(csv_filename))
            os.makedirs(os.path.dirname(csv_filename), exist_ok=True)


    vec -= max(vec)
    if vec[0]< -500:
        append_csv(csv_filename , 0)
    for index in range(1 , len(vec)):
        if vec[index] < -500 and vec[index-1]>-500:
            # plt.figure()
            # plt.plot(vec)
            # plt.plot(index, vec[index], 'ro')
            # plt.xlabel('Index')
            # plt.ylabel('Value')
            # plt.axvline(x=dT_ptrigg*frequency, color='g', linestyle='--', label='dT_ptrigg')
            # plt.title('Vector with detected point')
            # plt.show()
            append_csv(csv_filename , float(index)/frequency - dT_ptrigg)
            
def append_csv(filename: str, value: float):
    with open(filename, 'a') as f:
        f.write(f"{value}\n")
    


def import_root_file(tree , branch_name: str):

    arr = tree[branch_name].array(library="np")
    return arr[0]

def import_root_settings(file):
    tree_name = "settings"
    tree = file[tree_name]
    
    return tree["freq_hz"].array(library="np")[0] , tree["post_trigger"].array(library="np")[0] , tree["data_len"].array(library="np")[0]

def process_root_files(root_folder:str , csv_filename:str):
    if os.path.isfile(csv_filename):
        raise ValueError("csv path inserted is already a file")
    if len(root_folder) != 0:
        if root_folder[-1] != "/":
            root_folder += "/"


    n = 0
    fname = root_folder + f"file_{n}.root"

    
    with uproot.open(fname) as file: # type: ignore
        frequency, post_trigger , data_len = import_root_settings(file)
        dT_ptrigg = data_len*(100 - post_trigger)/(frequency*100)

    print(fname)
    while(os.path.isfile(fname)):
        with uproot.open(fname) as file: # type: ignore
            tree = file["events"]
            tree_keys = tree.keys()
            for branch_name in tree_keys:
                vec = import_root_file(tree , branch_name)
                if max(vec) - min(vec) > delta:
                    timestamp_calculator(vec , frequency , dT_ptrigg, csv_filename)
                branch_name = f"event_{id}"
        n+=1
        fname = root_folder + f"file_{n}.root"

if __name__ == "__main__":
    process_root_files("" , "try.csv")
    