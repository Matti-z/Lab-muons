import uproot
import os.path
import numpy as np
import time


if __name__ == "__main__":
    
    n = 0
    fname = f"file_{n}.root"


    id = 1
    start = time.time()
    tree_name = f"event {id}"
    end = time.time()
    print(f"Time elapsed: {end - start:.10f} seconds")
    tree_name = f"event {id}"

    
    with uproot.open(fname) as file: # type: ignore
        start = time.time()
        print(tree_name in file)
        end = time.time()
        print(f"Time elapsed: {end - start:.10f} seconds")
        start = time.time()
        a = file.keys()
        end = time.time()
        print(type(a))
        
    print(f"Time elapsed: {end - start:.10f} seconds")

    