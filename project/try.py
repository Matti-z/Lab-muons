import uproot
import os.path
import numpy as np
import time


if __name__ == "__main__":
    
    n = 0
    fname = f"file_{n}.root"



    
    with uproot.open(fname) as file: # type: ignore
        tree = file["events"]
        tree_keys = tree.keys()
        print(tree_keys[0])
        

    