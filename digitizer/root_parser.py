import os
import pandas as pd
import ROOT
import uproot
import numpy as np
from pathlib import Path
from array import array


default_dir = str(Path(".").absolute()).split("string_A")[0]+"Lab-muons/"
universal_dir = lambda path: default_dir + path

def csv_to_root(csv_folder, output_root):
    """
    Combine all CSV files in a folder into a single ROOT file.
    
    Args:
        csv_folder: Path to folder containing CSV files
        output_root: Path for output ROOT file
    """
    csv_files = os.listdir(csv_folder)
    
    if not csv_files:
        print("No CSV files found in folder")
        return
    
    root_output_file =  universal_dir(output_root)


    output_root_file = ROOT.TFile(root_output_file, "UPDATE")
    tree = ROOT.TTree("timestamp", "recollection of timestamps")

    # Remove existing tree if present
    with uproot.open(root_output_file) as f:
        for key in f.keys():
            if "timestamp" in key:
                output_root_file.Delete(key)
                break
    

    data = np.empty(1024 , dtype=np.float32)
    file_list = os.listdir(csv_folder)
    
    for i in range(len(file_list)):
        event = [array("f" , [0]) for _ in range(1024)]
        data_branch_name = f"event_{str(file_list[i]).removesuffix(".csv")}"
        data_branch_title = f"event_{str(file_list[i]).removesuffix(".csv")} %\F"
        tree.Branch(data_branch_name, event, data_branch_title)

        for j in range(1024):
            event[j][0] = data[j]
        tree.Fill()
        

    output_root_file.Write()
    output_root_file.Close()

if __name__ == "__main__":
    csv_folder = "./your_csv_folder"  # Change this path
    output_root = "./combined_data.root"
    csv_to_root(csv_folder, output_root)