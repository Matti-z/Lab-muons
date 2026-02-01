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
    




def import_root_settings(file):
    tree_name = "settings"
    tree = file[tree_name]
    
    settings = {
        "freq_hz": tree["freq_hz"].array(library="np")[0],
        "post_trigger": tree["post_trigger"].array(library="np")[0],
        "data_len": tree["data_len"].array(library="np")[0],
        "resolution": tree["resolution"].array(library="np")[0],
        "volt_low": tree["volt_low"].array(library="np")[0],
        "volt_high": tree["volt_high"].array(library="np")[0]
    }
    return settings

def process_root_files(root_folder:str , csv_filename:str):
    ls = os.listdir(root_folder)
    if len(ls) == 0:
        print("Empty directory: \t" , root_folder)
        exit(-1)
    max_num = max([int(f.split('_')[1].split('.')[0]) for f in ls if f.startswith('file_') and f.endswith('.root')])
    if os.path.isfile(csv_filename):
        raise ValueError("csv path inserted is already a file")
    if len(root_folder) != 0:
        if root_folder[-1] != "/":
            root_folder += "/"

    
    n = 0
    fname = root_folder + f"file_{n}.root"
    
    
    with uproot.open(fname) as file: # type: ignore
        dict = import_root_settings(file)
        frequency = dict["freq_hz"]
        post_trigger = dict["post_trigger"]
        data_len = dict["data_len"]
        dT_ptrigg = data_len*(100 - post_trigger)/(frequency*100)

    while(os.path.isfile(fname)):
        with uproot.open(fname) as file: # type: ignore
            tree = file["events"]
            matrix = tree["events"].array(library="np") # type: ignore
            print(matrix)
            print(matrix.shape)
            input()
            for vec in matrix:
                if max(vec) - min(vec) > delta:
                    timestamp_calculator(vec , frequency , dT_ptrigg, csv_filename)
                branch_name = f"event_{id}"
        n+=1
        fname = root_folder + f"file_{n}.root"

        perc: int = int(round(n /  max_num * 30))
        string: str = (
            "[" + "#" * perc + "-" * (30 - perc) + "]\t" + "\t" + str(n) + "\t" + str(max_num))
        print("\r" + string, end="", flush=True)


def root_settings_to_csv( root_folder: str , csv_filename:str):
    a = 0
    n = 0
    if len(os.listdir(root_folder)) == 0:
        print("Empty directory: \t" , root_folder)
        exit(-1)
    fname = root_folder + f"file_{n}.root"
    if os.path.isfile(csv_filename):
        raise ValueError("settings file already exists")
    
    with uproot.open(fname) as file: # type: ignore
        dict = import_root_settings( file)
        with open(csv_filename, 'x') as f:
            for key, value in dict.items():
                f.write(f"{key},{value}\n")



if __name__ == "__main__":
    process_root_files("big_data/root/19_01_2026_10_27" , "try.csv")
    