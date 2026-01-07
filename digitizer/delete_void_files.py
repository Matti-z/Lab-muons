import numpy as np
import os

# Read CSV file
print(len(os.listdir("/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA")))
for i in os.listdir('/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA'):
    data = np.genfromtxt("/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA/"+i, delimiter=',')
    if abs(min(data) - max(data)) < 300:
        os.remove("/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA/"+i)
print(len(os.listdir("/Users/ibolde/coding/Lab-muons/AAAAAAAAAAA")))
    