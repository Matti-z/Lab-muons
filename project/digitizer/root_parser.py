import os
import pandas as pd
import ROOT
import uproot
import numpy as np
from pathlib import Path
from array import array
from gc import collect


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
    

    file_list = os.listdir(csv_folder)
    
    for i in range(len(file_list)):

        perc: int = int(round(i /  len(file_list) * 30))
        string: str = (
            "[" + "#" * perc + "-" * (30 - perc) + "]\t" + "\t" + str(i) + "\t" + str(len(file_list)))
        print("\r" + string, end="", flush=True)
        data = np.genfromtxt(csv_folder +"/"+  file_list[i], delimiter=',' , dtype=np.uint16)
        event = array("f" , [0])
        data_branch_name = f"event_{str(file_list[i]).removesuffix(".csv")}"
        data_branch_title = f"event_{str(file_list[i]).removesuffix(".csv")} /F"
        tree.Branch(data_branch_name, event, data_branch_title)

        for j in range(len(data)):
            event[0] = data[j]
            tree.Fill()
        
        # tree.Write("", ROOT.TObject.kOverwrite)
        del data
        del event
        del data_branch_name
        del data_branch_title
        collect()

    output_root_file.Write()
    output_root_file.Close()

if __name__ == "__main__":
    csv_folder = "csv/natale"  # Change this path
    output_root = "Data/root_folder/natale.root"
    csv_to_root(csv_folder, output_root)