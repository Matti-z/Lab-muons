from scipy.stats import norm
import numpy as np
from numpy.random import random
from typing import Callable
import matplotlib.pyplot as plt

muon_dist_approx = norm(np.pi/2 , 1)
muon_dist = lambda x: np.where((x > 0) & (x<np.pi) , np.sin(x)**(2/3)/2.4, 0)

def HoM( pdf: Callable , approx):
    y = random()
    x = approx.rvs()
    if( y < pdf(x)): return x
    return HoM(pdf , approx)

dataset = [ HoM(muon_dist , muon_dist_approx) for _ in range(int(1e4))]
# Check for negative values and NaN
print(f"Negative values: {np.sum(np.array(dataset) < 0)}")
print(f"NaN values: {np.sum(np.isnan(dataset))}")


x = np.linspace( 0 , np.pi)
plt.plot(x , muon_dist_approx.pdf(x))
plt.hist(dataset , bins = 100 , density=True)
plt.plot( x ,muon_dist(x))
plt.show()
