import uproot
import os.path
import numpy as np
import matplotlib.pyplot as plt

DELTA = 500

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
    




def define_settings_dict(file):
    tree_name = "settings"
    tree = file[tree_name]
    
    settings = {
        "freq_hz": tree["freq_hz"].array(library="np")[0],
        "post_trigger": tree["post_trigger"].array(library="np")[0],
        "data_len": tree["data_len"].array(library="np")[0],
        "resolution": tree["resolution"].array(library="np")[0],
        "volt_low": tree["volt_low"].array(library="np")[0],
        "volt_high": tree["volt_high"].array(library="np")[0],
        "delta": DELTA
    }
    return settings

def process_root_files(root_folder:str , csv_filename:str):
    ls = os.listdir(root_folder)
    if len(ls) == 0:
        print("Empty directory: \t" , root_folder)
        exit(-1)
    if os.path.isfile(csv_filename):
        raise ValueError("csv path inserted is already a file")
    if len(root_folder) != 0:
        if root_folder[-1] != "/":
            root_folder += "/"

    fname = root_folder + f"file.root"
    
    
    with uproot.open(fname) as file: # type: ignore
        dict = define_settings_dict(file)
        frequency = dict["freq_hz"]
        post_trigger = dict["post_trigger"]
        data_len = dict["data_len"]
        dT_ptrigg = data_len*(100 - post_trigger)/(frequency*100)


    with uproot.open(fname) as file: # type: ignore
        tree = file["events"]
        n_entries = tree["events"].num_entries # type: ignore
        counter = 0
        for batch in tree.iterate(step_size=1000, library="np"):# type: ignore

            if not all(len(v) == len(batch["events"][0]) for v in batch["events"]):# type: ignore
                    # raise ValueError("Not all vectors have the same length.")
                    continue
            
            for vec in batch["events"]: # type: ignore
                counter +=1
                if max(vec) - min(vec) > DELTA:
                    timestamp_calculator(vec , frequency , dT_ptrigg, csv_filename)

                perc: int = int(round(counter /  n_entries * 30))
                string: str = (
                    "[" + "#" * perc + " " * (30 - perc) + "]\t" + "\t" + str(counter) + "\t" + str(n_entries))
                print("\r" + string, end="", flush=True)


def root_settings_to_csv( root_folder: str , csv_filename:str):
    if len(os.listdir(root_folder)) == 0:
        print("Empty directory: \t" , root_folder)
        exit(-1)
    fname = root_folder + f"file.root"
    if os.path.isfile(csv_filename):
        raise ValueError("settings file already exists")
    
    with uproot.open(fname) as file: # type: ignore
        dict = define_settings_dict( file)
        with open(csv_filename, 'x') as f:
            for key, value in dict.items():
                f.write(f"{key},{value}\n")



if __name__ == "__main__":
    # from pathlib import Path


    # default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
    # universal_dir = lambda path: default_dir + path
    # xml_path = universal_dir("big_data/error_prop_700ns.xml")
    # xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
    # csv_path = universal_dir("Data/timestamp/"+xml_filename+".csv")
    # csv_settings_path = universal_dir("Data/settings/"+ xml_filename + ".csv")



    # root_path = universal_dir("big_data/root/"+xml_filename+"/")

    # process_root_files(root_path , csv_path)
    a = 0