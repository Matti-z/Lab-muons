import numpy as np
import scipy
from scipy.stats import expon, norm, uniform, chi2
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL
from IPython.display import display
import pandas as pd


N = 19944

def exp( x , a, A, tau ):
    return a *N* expon.cdf(x , A , tau) 



def exp_unif(x, a, b, tau, A):
    return a * N * (expon.cdf(x, A, tau) + b * N * uniform.cdf(x, 0, 8e-6))

def exp_unif_pdf(x, a, b, tau, A):
    return a * N * (expon.pdf(x, A, tau) + b * N * uniform.pdf(x, 0, 8e-6))



def exp_gauss(x, a, b, tau, A, mu, sigma):
    return a * N * (expon.cdf(x, A, tau) + b * norm.cdf(x, mu, sigma))

def exp_gauss_pdf(x, a, b, tau, A, mu, sigma):
    return a * N * (expon.pdf(x, A, tau) + b * norm.pdf(x, mu, sigma))



def complete(x, a, b, c, tau, A, mu, sigma ):
    return a * N * (expon.cdf(x, A, tau) + b * norm.cdf(x, mu, sigma) + c * uniform.cdf(x, 0, 8e-6))

def complete_pdf(x, a, b, c, tau, A, mu, sigma ):
    return a * N * (expon.pdf(x, A, tau) + b * norm.pdf(x, mu, sigma) + c * uniform.pdf(x, 0, 8e-6))



def exp_fit(cdf, a, A, tau, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, A, tau )
    n.fixed["A"] = True
    #n.limits['a'] = (10000, 1000000)
    n.migrad()
    n.hesse()
    return n

def exp_gauss_fit(cdf, a, b, tau, A, mu, sigma, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, b, tau, A, mu, sigma)
    # n.fixed['N'] = True
    n.fixed['A'] = True
    n.fixed['tau'] = True
    n.fixed['a'] = True
    n.fixed['mu'] = True
    #n.limits['a'] = (0, 10000)
    n.limits['b'] = (0, 10000)
    n.limits['mu'] = (1e-6, None)
    
    n.migrad()
    n.hesse()
    return n

def exp_unif_fit(cdf, a, b, tau, A, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, b, tau, A )
    # n.fixed['N'] = True
    n.fixed['A'] = True
    # n.limits['b'] = (0, 1)
    n.migrad()
    n.hesse()
    return n

def complete_fit(cdf, a, b, c, tau, A, mu, sigma, count , edges):
    
    cost = ExtendedBinnedNLL(count, edges, cdf)
    n = Minuit(cost, a, b, c, tau, A, mu, sigma)
    # n.fixed['N'] = True
    n.fixed['A'] = True
    #n.fixed['tau'] = True
    #n.fixed['a'] = True
    #n.fixed['mu'] = True
    #n.limits['a'] = (0, 10000)
    n.limits['b'] = (0, 10000)
    n.limits['mu'] = (1e-6, None)
    
    n.migrad()
    n.hesse()
    return n


n_bins = 70

if __name__ == "__main__":

    df = pd.read_csv('Jack/old.csv')
    old=[]
    for i in df.values:
        old.append(i[0])
    old=np.array(old)

    timestamp = np.loadtxt('Jack/timestamps_M.txt')
    timestamp = np.array(timestamp)

    timestamp=timestamp[timestamp>3e-7]
    #timestamp=timestamp[timestamp>2e-6]
    count_1, edges_1 =  np.histogram(timestamp, bins=n_bins)



    timestamp_e=timestamp[(timestamp<1e-6) | (timestamp>2.3e-6)]
    count_e, edges_e =  np.histogram(timestamp_e, bins=n_bins)

    e = exp_fit(exp, 1, 0, 0.8e-6, count_e , edges_e)
    display(e)


    '''plt.hist(timestamp_e, bins=70, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x = np.linspace(edges_e[0], edges_e[-1], 1000)
    y = np.diff(edges_e)[0] *N* e.values['a'] *expon.pdf(x,  e.values['A'], e.values['tau'])
    plt.plot(x, y, label='Fit', color='red', linewidth=2)
    plt.legend()
    plt.show()'''


    u = exp_unif_fit(exp_unif, e.values['a'], 0, e.values['tau'], e.values['A'], count_e , edges_e)
    display(u)

    '''plt.hist(timestamp_e, bins=70, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x = np.linspace(edges_e[0], edges_e[-1], 1000)
    y = np.diff(edges_e)[0] * exp_unif_pdf(x, u.values['a'], u.values['b'], u.values['tau'], u.values['A'])
    plt.plot(x, y, label='Fit', color='blue', linewidth=2)
    plt.legend()
    plt.show()'''




    k = exp_gauss_fit(exp_gauss, e.values['a'], 0.5, e.values['tau'], e.values['A'], 1.3e-6, 7e-7, count_1 , edges_1)
    display(k)

    '''plt.hist(timestamp, bins=70, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x = np.linspace(edges_1[0], edges_1[-1], 1000)
    y = np.diff(edges_1)[0] * exp_gauss_pdf(x, k.values['a'], k.values['b'], k.values['tau'], k.values['A'], k.values['mu'], k.values['sigma'])
    plt.plot(x, y, label='Fit', color='red', linewidth=2)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()'''



    c = complete_fit(complete, u.values['a'], 0.5, u.values['b'], u.values['tau'], u.values['A'], 1.3e-6, 7e-7, count_1 , edges_1)
    display(c)

    print('p_value =', 1 - chi2.cdf(c.fmin.fval, c.ndof))


    plt.hist(timestamp, bins=70, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x = np.linspace(edges_1[0], edges_1[-1], 1000)
    y = np.diff(edges_1)[0] * complete_pdf(x, c.values['a'], c.values['b'], c.values['c'], c.values['tau'], c.values['A'], c.values['mu'], c.values['sigma'])
    plt.plot(x, y, label=f'Fit', color='green', linewidth=2)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()





    old=old[old>4e-7]
    count_old, edges_old =  np.histogram(old, bins=n_bins)

    c_old = complete_fit(complete, u.values['a'], 0.5, u.values['b'], u.values['tau'], u.values['A'], 1.3e-6, 7e-7, count_old , edges_old)
    display(c_old)

    print('p_value =', 1 - chi2.cdf(c_old.fmin.fval, c_old.ndof))

    plt.hist(old, bins=n_bins, alpha=0.5, label='Data', color='gray', edgecolor='black')
    x_old = np.linspace(edges_old[0], edges_old[-1], 1000)
    y_old = np.diff(edges_old)[0] * complete_pdf(x_old, c_old.values['a'], c_old.values['b'], c_old.values['c'], c_old.values['tau'], c_old.values['A'], c_old.values['mu'], c_old.values['sigma'])
    plt.plot(x_old, y_old, label=f'Fit', color='green', linewidth=2)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()


    #Normalized histograms

    start = 4e-7
    end = 3.6e-6
    nbins = 70
    timestamp_1 = timestamp[(timestamp>start) & (timestamp<end)]
    old_1 = old[(old>start) & (old<end)]

    count_norm, edges_norm =  np.histogram(timestamp_1, bins=np.linspace(start,end,nbins+1), density=True)
    count_old_norm, edges_old_norm =  np.histogram(old_1, bins=np.linspace(start,end,nbins+1), density=True)

    n = complete_fit(complete, c.values['a']/N, c.values['c'], c.values['b'], c.values['tau'], c.values['A'], c.values['mu'], c.values['sigma'], count_norm , edges_norm)
    display(n)
    no = complete_fit(complete, u.values['a'], 0.5, u.values['b'], u.values['tau'], u.values['A'], 1.3e-6, 7e-7, count_old_norm , edges_old_norm)
    display(no)

    plt.hist(timestamp, bins=n_bins, alpha=0.5, label='Data', color='gray', edgecolor='black', density=True)
    x = np.linspace(edges_norm[0], edges_norm[-1], 1000)
    y = np.diff(edges_norm)[0] * complete_pdf(x, n.values['a'], n.values['b'], n.values['c'], n.values['tau'], n.values['A'], n.values['mu'], n.values['sigma'])
    plt.plot(x, y, label=f'Fit', color='green', linewidth=2)

    #plt.hist(old, bins=n_bins, alpha=0.5, label='Old Data', color='blue', edgecolor='black', density=True)
    x_old = np.linspace(edges_old_norm[0], edges_old_norm[-1], 1000)
    y_old = np.diff(edges_old_norm)[0] * complete_pdf(x_old, no.values['a'], no.values['b'], no.values['c'], no.values['tau'], no.values['A'], no.values['mu'], no.values['sigma'])
    #plt.plot(x_old, y_old, label=f'Old Fit', color='blue', linewidth=2)

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()



    count_diff = np.abs(count_old_norm - count_norm)
    edges_diff = edges_norm

    plt.hist(timestamp_1, bins=nbins, alpha=0.5, label='Data', color='gray', edgecolor='black', density=True)
    plt.hist(old_1, bins=nbins, alpha=0.5, label='Old Data', color='blue', edgecolor='black', density=True)
    #plt.hist(count_diff, bins=nbins, alpha=0.5, label='Difference', color='red', edgecolor='black', density=True)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Histogram of Timestamps')
    plt.show()
    