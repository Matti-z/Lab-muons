import numpy as np
import scipy.stats as stats
from scipy.stats import expon, uniform
import random
import matplotlib.pyplot as plt
from lib import *
import time 

def exp_unif(x, N , A, a, b, tau, e):
    return a * N * (expon.pdf(x, A, tau) + b * N * uniform.pdf(x, 0, e))
def exp_unif_cdf(x, N , A, a, b, tau, e):
    return a * N * (expon.cdf(x, A, tau) + b * N * uniform.cdf(x, 0, e))

def exp(x, a, tau):
    return a * expon.pdf(x, 0, tau) 
def exp_cdf(x, N, A, a, tau):
    return a * N * expon.cdf(x, A, tau)

def singolo_punto(funct, parameters : np.ndarray): #voglio creare il singolo punto della distribuzione

    if funct is exp_unif:
        n0 = parameters[0]
        A0 = parameters[1]
        a0 = parameters[2]
        b0 = parameters[3]
        tau0 = parameters[4]
        e0 = parameters[5]
        
        while True:
            random.seed(time.time())
            x0 = np.random.uniform(0, 7e-6)
            #ottimizzazione y triangolare tra max in 0 e max in 7e-6, non funziona
            # y0 = np.random.uniform(0, (funct(7e-6, *parameters)-funct(0, *parameters)/(7e-6) * x0)+ (funct(0, *parameters))) 
            y0 = np.random.uniform(0, funct(0, *parameters))
            if y0 < exp_unif(x0, n0, A0, a0, b0, tau0, e0):
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

def fitting_singola_distribuzione(funct, funct_cdf, parameters : np.ndarray, n_points = 100000, bin = 67):#n_points è numero di punti in singola distribuzione
    x, y = singola_distribuzione(funct, parameters, n_points)

    #cose correttive al momento inutili, ma le lascio: sinoli plot
    # x_prime = np.linspace(0, 7e-6, 10000)
    # plt.hist(x, bins = 100, density = True, label = "exp_unif")
    # plt.plot(x_prime, exp_unif(x_prime, *parameters)/ (parameters[0]))
    # plt.show()

    if funct is exp_unif:
        count, edges = np.histogram( x , bins=bin) 
        cost = ExtendedBinnedNLL(count, edges, funct_cdf)
        m = Minuit(cost, *parameters)
        m.fixed['A'] = True
        m.fixed['N'] = True
        m.migrad()

    if funct is exp:
        count, edges = np.histogram( x , bins=bin) 
        cost = ExtendedBinnedNLL(count, edges, funct_cdf)
        m = Minuit(cost, *parameters)
        m.fixed['A'] = True
        m.migrad()
    
    # print(m)
    return m.values, m.errors

def save_number_data(funct, funct1, parameters : np.ndarray, n_points = 100000, q = 50): #q è numero di fit che voglio fare-->numero di valori diversi di theta
    nm = np.zeros(q)
    Am = np.zeros(q)
    am = np.zeros(q)
    bm = np.zeros(q)
    taum = np.zeros(q)
    em = np.zeros(q)
    err_Am = np.zeros(q)
    err_nm = np.zeros(q)
    err_am = np.zeros(q)
    err_bm = np.zeros(q)
    err_taum = np.zeros(q)
    err_em = np.zeros(q)
    for i in range (q):
        v, err = fitting_singola_distribuzione(funct = funct, funct_cdf = funct1, parameters = parameters, n_points = n_points)
        nm[i] = v[0]
        Am[i] = v[1]
        am[i] = v[2]
        bm[i] = v[3]
        taum[i] = v[4]
        em[i] = v[5]
        err_nm[i] = err[0]
        err_Am[i] = err[1]
        err_am[i] = err[2]
        err_bm[i] = err[3]
        err_taum[i] = err[4]
        err_em[i] = err[5]
        counter = i
        perc: int = int(round(counter /  q * 30))
        string: str = (
            "[" + "#" * perc + " " * (30 - perc) + "]\t" + "\t" + str(counter) + "\t" + str(q))
        print("\r" + string, end="", flush=True)
        # print("fit done", i, "/", q, ", tau value:", v[4])
    # plt.hist(taum, 15)
    # plt.show()
    return nm, Am, am, bm, taum, em, err_nm, err_Am, err_am, err_bm, err_taum, err_em


if __name__ == "__main__":
    N = 46506
    a = 1.031
    A = 0
    b = 1.39e-6
    tau = 2.09e-6
    e = 6.484e-6

    parameters = [N, A, a, b, tau, e]
    parameters_exp = [a, tau]
    # x, y = singola_distribuzione(exp_unif, parameters, n_points = 5)
    # plt.hist(x, bins = 100, density = True, label = "exp_unif")
    # plt.show()
    # v, er = fitting_singola_distribuzione(exp_unif, parameters, n_points = 5000)
    a_data = save_number_data(exp_unif, exp_unif_cdf, parameters, n_points = N, q = 1000)
    with open ("data_sim_exp_unif3.txt", "w") as f:
        f.write("N A a b tau e err_N err_A err_a err_b err_tau err_e\n")
        for i in range(len(a_data[0])):
            f.write(f"{a_data[0][i]} {a_data[1][i]} {a_data[2][i]} {a_data[3][i]} {a_data[4][i]} {a_data[5][i]} {a_data[6][i]} {a_data[7][i]} {a_data[8][i]} {a_data[9][i]} {a_data[10][i]}\n")

    
    