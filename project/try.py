
import numpy as np

import matplotlib.pyplot as plt

# Read the CSV file
data = np.genfromtxt('16_1_2026_16_55.csv', delimiter=',')

data = data.T[0]

# Plot the data
plt.figure(figsize=(10, 6))
plt.hist(max(data) - data)
plt.xlabel('Column Index')
plt.ylabel('Value')
plt.title('CSV Data Plot')
plt.grid(True)
plt.show()