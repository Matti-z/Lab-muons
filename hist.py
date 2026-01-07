import numpy as np
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL
from scipy.stats import expon


n_bins = 100

def exp( x , A , tau):
    return expon(x , loc = A , scale = tau)

def gauss_fit(cdf, A , tau, en):
    """
    Fits a Gaussian to the histogram using ExtendedBinnedNLL.
    Parameters:
        cdf: Cumulative distribution function
        mean: Initial mean guess
        std: Initial std guess
        en: Energy array
        fixed: If True, fixes mean during fit
    Returns:
        Fitted mean, std, normalization, covariance matrix
    """
    count, edges = np.histogram(en, bins=n_bins)
    cost = ExtendedBinnedNLL(count, edges, cdf)
    p_index = list(count).index(max(count))  # Index of peak bin
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, A = A , tau = tau)
    n.migrad(ncall=1000)
    return n

if __name__ == "__main__":
    data = np.genfromtxt("2026-01-07.csv", delimiter=',')
    n = gauss_fit( exp , 1 , 1 , data)
    print(n)