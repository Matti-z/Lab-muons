import numpy as np
import os
from pathlib import Path

DATA_PATH = Path('Lab-muons/pippo')


# Read CSV file
print(len(os.listdir(DATA_PATH)))
for i in os.listdir(DATA_PATH):
    data = np.genfromtxt(DATA_PATH+i, delimiter=',')
    if abs(min(data) - max(data)) < 300:
        os.remove(DATA_PATH+i)
print(len(os.listdir(DATA_PATH)))
    