import numpy as np
import scipy
from scipy.stats import expon, norm, uniform, chi2
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL
from IPython.display import display
import pandas as pd

N = 2107951

def exp( x , a, A, tau ):
    return a *N* expon.cdf(x , A , tau)

def exp_pdf( x , a, A, tau ):
    return a *N* expon.pdf(x , A , tau)

def exp_fit(cdf, a, A, tau, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, A, tau )
    n.fixed["A"] = True
    n.limits['a'] = (0, None)
    n.migrad()
    n.hesse()
    return n





def exp_gauss(x, a, b, tau, A, mu, sigma):
    return a * N * (expon.cdf(x, A, tau) + b * norm.cdf(x, mu, sigma))

def exp_gauss_pdf(x, a, b, tau, A, mu, sigma):
    return a * N * (expon.pdf(x, A, tau) + b * norm.pdf(x, mu, sigma))

def exp_gauss_fit(cdf, a, b, tau, A, mu, sigma, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, b, tau, A, mu, sigma)
    # n.fixed['N'] = True
    n.fixed['A'] = True
    #n.fixed['tau'] = True
    #n.fixed['a'] = True
    #n.fixed['mu'] = True
    n.limits['a'] = (0, None)
    n.limits['b'] = (0, None)
    n.limits['mu'] = (1.3e-6, None)
    
    n.migrad()
    n.hesse()
    return n





def complete(x, a, b, c, tau, A, mu, sigma ):
    return a * N * (expon.cdf(x, A, tau) + b * norm.cdf(x, mu, sigma) + c * uniform.cdf(x, 0, 8e-6))

def complete_pdf(x, a, b, c, tau, A, mu, sigma ):
    return a * N * (expon.pdf(x, A, tau) + b * norm.pdf(x, mu, sigma) + c * uniform.pdf(x, 0, 8e-6))

def complete_fit(cdf, a, b, c, tau, A, mu, sigma, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, b, c, tau, A, mu, sigma)
    
    n.fixed['A'] = True
    n.fixed['c'] = True
    #n.fixed['tau'] = True
    #n.fixed['a'] = True
    #n.fixed['mu'] = True
    n.limits['a'] = (0, None)
    n.limits['b'] = (0, 10000)
    n.limits['mu'] = (1.e-6, None)
    
    n.migrad()
    n.hesse()
    return n





n_bins = 100

if __name__ == "__main__":

    df = pd.read_csv('Jack/old.csv')
    old=[]
    for i in df.values:
        old.append(i[0])
    old=np.array(old)

    old=old[old>4e-7]

    old_cut=old[(old<1e-6) | (old>2.2e-6)]
    print(len(old_cut) , len(old))

    count_1, edges_1 =  np.histogram(old_cut, bins=n_bins)
    
    e = exp_fit(exp, 1, 0, 2.2e-6, count_1 , edges_1)
    display(e)

    plt.hist(old_cut, bins=n_bins, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x = np.linspace(edges_1[0], edges_1[-1], 1000)
    y = np.diff(edges_1)[0] * exp_pdf(x, e.values['a'], e.values['A'], e.values['tau'])
    plt.plot(x, y, label='Fit', color='red', linewidth=2)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps with Exponential Fit')
    plt.show()
    
    
    
    
    count, edges =  np.histogram(old, bins=n_bins)
    x = np.linspace(edges[0], edges[-1], 1000)

    
    o= exp_gauss_fit(exp_gauss, 1, 0.5, 2.2e-6, 0, 1.3e-6, 7e-7, count , edges)
    display(o)


    '''plt.hist(old, bins=n_bins, alpha=0.5, label='Data', color='gray', edgecolor='black')
    y = np.diff(edges)[0] * exp_gauss_pdf(x, o.values['a'], o.values['b'], o.values['tau'], o.values['A'], o.values['mu'], o.values['sigma'])
    plt.plot(x, y, label='Fit', color='red', linewidth=2)
    plt.legend()
    plt.show()'''

    c_old = complete_fit(complete, 0.2, 1, 0, 2.2e-6, 0, 1.660e-6, 0.217e-6, count , edges)
    display(c_old)

    print('p_value =', 1 - chi2.cdf(c_old.fmin.fval, c_old.ndof))

    plt.hist(old, bins=70, alpha=0.5, label='Data', color='gray', edgecolor='black')
    y = np.diff(edges)[0] * complete_pdf(x, c_old.values['a'], c_old.values['b'], c_old.values['c'], c_old.values['tau'], c_old.values['A'], c_old.values['mu'], c_old.values['sigma'])
    plt.plot(x, y, label=f'Fit', color='green', linewidth=2)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()