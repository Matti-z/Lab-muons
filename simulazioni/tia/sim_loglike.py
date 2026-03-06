import numpy as np
import scipy.stats as stats
from scipy.stats import expon, uniform
import random
import matplotlib.pyplot as plt
from lib import *

def exp_unif(x, N , a, b, tau, e):
    return a * N * (expon.pdf(x, 0, tau) + b * N * uniform.pdf(x, 0, e))

def exp(x, a, tau):
    return a * expon.pdf(x, 0, tau) 

def singolo_punto(funct, parameters : np.ndarray): #voglio creare il singolo punto della distribuzione

    if funct is exp_unif:
        N0 = parameters[0]
        a0 = parameters[1]
        b0 = parameters[2]
        tau0 = parameters[3]
        e0 = parameters[4]
        
        while True:
            x0 = np.random.uniform(0, 7e-6)
            y0 = np.random.uniform(0, a0 * N0 / tau0 + b0 * N0 / e0 )
            if y0 < exp_unif(x0, N0, a0, b0, tau0, e0):
                return x0, y0
    if funct is exp:
        a0 = parameters[0]
        tau0 = parameters[1]
        
        while True:
            x0 = np.random.uniform(0, 7e-6)
            y0 = np.random.uniform(0, a0 / tau0 )
            val = exp(x0, a0, tau0)
            if y0 < val:
                return x0, y0
    else:
        print("funzione non riconosciuta")
        return 0, 0
    
def singola_distribuzione(funct, parameters : np.ndarray, n_points = 100000): #voglio creare la distribuzione completa
    x = np.zeros(n_points)
    y = np.zeros(n_points)
    for i in range(n_points):
        x1, y1 = singolo_punto(funct, parameters)
        x[i] = x1
        y[i] = y1
    return x, y

def fitting_singola_distribuzione(funct, parameters : np.ndarray, n_points = 100000, bin = 67):#n_points è numero di punti in singola distribuzione
    x, y = singola_distribuzione(funct, parameters, n_points)
    if funct is exp_unif:
        m = dataset_analysis(x, funct, args = { "a": parameters[1], "b": parameters[2],
                                                "tau": parameters[3], "e": parameters[4]}, bins = bin)
    if funct is exp:
        m = dataset_analysis(x, funct, args = {"a": parameters[0], "tau": parameters[1]}, bins = bin)
    return m.values, m.errors

def save_number_data(funct, parameters : np.ndarray, n_points = 100000, q = 50): #q è numero di fit che voglio fare
    am = np.zeros(q)
    bm = np.zeros(q)
    taum = np.zeros(q)
    em = np.zeros(q)
    err_am = np.zeros(q)
    err_bm = np.zeros(q)
    err_taum = np.zeros(q)
    err_em = np.zeros(q)
    for i in range (q):
        v, err = fitting_singola_distribuzione(funct = funct, parameters = parameters, n_points = n_points)
        am[i] = v[0]
        bm[i] = v[1]
        taum[i] = v[2]
        em[i] = v[3]
        err_am[i] = err[0]
        err_bm[i] = err[1]
        err_taum[i] = err[2]
        err_em[i] = err[3]
        print("fit done", i, "/", q, ", tau value:", v[2])
    plt.hist(taum, 8,)
    plt.show()
    return taum
    



if __name__ == "__main__":
    N = 46506
    a = 1.031
    b = 1.39e-6
    tau = 2.09e-6
    e = 6.484e-6

    parameters = [N, a, b, tau, e]
    parameters_exp = [a, tau]
    # x, y = singola_distribuzione(exp_unif, parameters, n_points = 50000)
    # v, er = fitting_singola_distribuzione(exp_unif, parameters, n_points = 5000)
    a_data = save_number_data(exp_unif, parameters, n_points = 10000, q = 100)
    # print(a_data)
    
    