import numpy as np
import math
from typing import Tuple
import matplotlib.pyplot as plt

class scint:  #definisco classe scintillatore
    def __init__ (self, r, theta, phi, z):
        self.r = r
        self.theta = theta
        self.phi = phi
        self.z = z
        self._compute_limits()

    def _compute_limits(self):
        self.upper_z = self.z + self.r * np.cos(self.theta)
        self.lower_z = self.z + -self.r * np.cos(self.theta)
        self.left_y  = - self.r * np.sin(self.theta) * np.sin(self.phi)
        self.right_y =   self.r * np.sin(self.theta) * np.sin(self.phi)
        self.pos_x   =   self.r * np.sin(self.theta) * np.cos(self.phi)
        self.neg_x   = - self.r * np.sin(self.theta) * np.cos(self.phi)

class muon:  #definisco classe muone
    def __init__ (self, r = float, theta = float, phi = float):
        self.r = r
        self.theta = theta
        self.phi = phi

def spher_to_cart(r, theta, phi): #converto coordinate sferiche in cartesiane
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


#verifico se il muone interseca lo scintillatore, dati due angoli di deviazione theta_d e phi_d
def intersec(m, s, theta_d, phi_d, upper_or_lower):
    pos = 0
    neg = 0
    x_0, y_0, z_0 = spher_to_cart(m.r, m.theta, m.phi)
    if upper_or_lower == 'lower':
        z_defined = s.lower_z
    elif upper_or_lower == 'upper':
        z_defined = s.upper_z
    else:
        raise ValueError("upper_or_lower must be 'lower' or 'upper'")
    delta_z =abs( z_0 - z_defined)
    y_prime = y_0 + delta_z * np.tan(theta_d)
    x_prime = x_0 + delta_z * np.tan(phi_d)
    dist_max_scint = np.sqrt(s.right_y**2 + s.pos_x**2)
    dist_prime = np.sqrt(x_prime**2 + y_prime**2)
    # if dist_prime > dist_max_scint:
    #     return x_prime, y_prime, z_defined, False
    if dist_prime <= dist_max_scint:
        if np.abs(s.right_y) >= np.abs(y_prime) and np.abs(s.pos_x) >= np.abs(x_prime):
            # print('intersezione piano superiore/inferiore con lo scintillatore')
            pos += 1
        if np.abs(s.right_y) < np.abs(y_prime) or np.abs(s.pos_x) < np.abs(x_prime):
            pos = 0
    return x_prime, y_prime, z_defined, pos


#restituisce proiezione sul piano distanza in scintillatore se il muone passa solo sopra
#funziona bene anche se passa su lato sotto, basta scambiare nella seguente funzione x e x_
def casi_una_faccia(x, x_, l_mezzi): ##i valori passati non devono essere in modulo! (solo l_mezzi nel caso)
    if (abs(x_) + abs(x) > abs(l_mezzi)) and (x * x_ >= 0):
        return abs(l_mezzi) - abs(x)
    elif (abs(x_) <= abs(l_mezzi)) and (abs(x_) > abs(x)) and (x * x_ >= 0):
        return abs(x_) - abs(x)    
    elif (abs(x_) < abs(x)) and (x * x_ >= 0):
        return abs(x) - abs(x_)
    elif (x * x_ < 0) and (abs(x_) < abs (l_mezzi)):
        return abs(x_) + abs(x)
    elif (x * x_ < 0) and (abs(x_) >= abs (l_mezzi)):
        return abs(l_mezzi) + abs(x)    
    

def scint_interaction(m, s1, theta_d, phi_d, lim_r_scint = 1.5): 
    #verifico se il muone interseca lo scintillatore, dati due angoli di deviazione theta_d e phi_d
    #sopra e sotto, sopra e di lato, sotto e di lato
    x, y, z, n_up_prov = intersec(m, s1, theta_d, phi_d, 'upper')
    x_, y_, z_, n_down_prov = intersec(m, s1, theta_d, phi_d, 'lower')
    s_e_s = 0
    s_e_l = 0
    l_e_s = 0
    r = 0
    if (n_up_prov == 1 and n_down_prov == 1):
        # print('passa sia up che down')
        s_e_s += 1
    if (n_up_prov == 1 and n_down_prov == 0):
        rx = casi_una_faccia(x, x_, s1.pos_x)
        ry = casi_una_faccia(y, y_, s1.right_y)
        r = np.sqrt(rx**2 + (ry * np.sin(theta_d))**2)
        # print('passa solo up, distanza percorsa: ', r)
        if (r > (np.sqrt(s1.right_y**2 + s1.pos_x**2+ s1.upper_z**2))): 
            print(f'ERROR!!!! r (={r}) > r_max (={np.sqrt(s1.right_y**2 + s1.pos_x**2+ s1.upper_z**2)}), sgravato sopra')
            print(f'x: {x}, x_: {x_}, y: {y}, y_: {y_}, rx: {rx}, ry: {ry}, theta_d: {theta_d}')
        if r > lim_r_scint:
            s_e_l += 1 
    if (n_up_prov == 0 and n_down_prov == 1):
        rx = casi_una_faccia(x_, x, s1.pos_x)
        ry = casi_una_faccia(y_, y, s1.right_y)
        r_ = np.sqrt(rx**2 + (ry * np.sin(theta_d))**2)
        # print('passa solo down, distanza percorsa: ', r_)
        if (r > (np.sqrt(s1.right_y**2 + s1.pos_x**2+ s1.upper_z**2))): print(f'ERROR!!!! r (={r}) > r_max (={np.sqrt(s1.right_y**2 + s1.pos_x**2+ s1.upper_z**2)}), sgravato sotto')
        if r_ > lim_r_scint:
            l_e_s += 1 
    return s_e_s, s_e_l, l_e_s

def coin_2_scint(muon, scint_up, scint_down, theta_d, phi_d): ##per fare coincidenze a due scintillatori
    d, n, m = scint_interaction(muon, s1, theta_d, phi_d, lim_r_scint = 1.5)
    d_, n_, m_ = scint_interaction(muon, s2, theta_d, phi_d, lim_r_scint = 1.5)
    if (d + d_ + n + n_ + m + m_) == 2 :
        return True
    elif (d + d_ + n + n_ + m + m_) < 2 :
        return False
    elif (d + d_ + n + n_ + m + m_) > 2 :
        print('ERRORE! piu di due scintillatori attivati!')
        return False
    
def coin_3_scint(muon, scint_up, scint_mid, scint_down, theta_d, phi_d): ##per fare coincidenze a tre scintillatori
    d, n, m = scint_interaction(muon, s1, theta_d, phi_d, lim_r_scint = 1.5)
    d_, n_, m_ = scint_interaction(muon, s2, theta_d, phi_d, lim_r_scint = 1.5)
    d__, n__, m__ = scint_interaction(muon, s3, theta_d, phi_d, lim_r_scint = 1.5)
    if (d + d_ + d__ + n + n_ + n__ + m + m_ + m__) == 3 :
        return True
    elif (d + d_ + d__ + n + n_ + n__ + m + m_ + m__) < 3 :
        return False
    elif (d + d_ + d__ + n + n_ + n__ + m + m_ + m__) > 3 :
        print('ERRORE! piu di tre scintillatori attivati!')
        return False
    
def muon_angle_distribution():
    """Sample (theta, phi) with angular distribution per unit solid angle ∝ cos^2(theta).

    This implements sampling for zenith angles in [0, pi/2] (muons from above).
    The cumulative for theta is F(theta)=1-cos^3(theta), so invert to get
    cos(theta) = (1 - u)^(1/3) for u ~ Uniform(0,1).
    """
    u = np.random.random()
    cos_theta = (1.0 - u) ** (1.0 / 3.0)
    theta_d = np.arccos(cos_theta)
    phi_d = np.random.uniform(0.0, 2.0 * np.pi)
    return theta_d, phi_d

def chat_gpt_cdf(x):
    return np.arccos((1-x)**(1/3))

def jack_cdf(y, tol=1e-12, max_iter=50):
    """
    Inverts the function:
        y = 1/pi * (x + 1/2 sin(2x)) + 1/2
    for x in [-pi/2, pi/2].

    Parameters:
        y : float or array-like in [0,1]
        tol : Newton convergence tolerance
        max_iter : maximum iterations

    Returns:
        x such that F(x) = y
    """
    y = np.asarray(y, dtype=float)
    # k = pi(y - 1/2)
    k = np.pi * (y - 0.5)
    # Initial guess x0 = k
    x = k.copy()
    for _ in range(max_iter):
        f  = x + 0.5*np.sin(2*x) - k
        fp = 1 + np.cos(2*x)
        dx = -f / fp
        x += dx
        if np.max(np.abs(dx)) < tol:
            break
    return x

def sample_cos2(N):
    """
    Samples x over [-pi/2, pi/2] with density ∝ cos^2(x).
    """
    u = np.random.rand(N)[0]
    return jack_cdf(u)



if __name__ == '__main__':
    triple = 0
    doppie = 0
    doppie_um = 0
    doppie_ml = 0
    numero_che_voglio = 999999 #numero di scintillazioni che voglio
    t = 0
    d = 0
    d_um = 0
    d_ml = 0
    n = 0
    s1 = scint(np.sqrt(15**2+40**2+(3.8/2)**2), np.arccos(3.8/(2*np.sqrt(15**2+40**2+(3.8/2)**2))), 
                   np.arctan2(40, 15), 3.8/2)
    s2 = scint(np.sqrt(15**2+40**2+(3.8/2)**2), np.arccos(3.8/(2*np.sqrt(15**2+40**2+(3.8/2)**2))), 
                   np.arctan2(40, 15), 8.4+(3.8/2))
    s3 = scint(np.sqrt(15**2+40**2+(3.8/2)**2), np.arccos(3.8/(2*np.sqrt(15**2+40**2+(3.8/2)**2))), 
                   np.arctan2(40, 15), 12.8+(3.8/2))
    while doppie <= numero_che_voglio:
        theta_d = sample_cos2(1)
        phi_d = sample_cos2(1)
        m = muon(np.random.uniform(43., 50.), np.random.uniform(0, np.pi/2), 
                 np.random.uniform(0, np.pi * 2))
        d = coin_2_scint(m, s1, s3, theta_d, phi_d)
        if d == True:
            d_um = coin_2_scint(m, s3, s2, theta_d, phi_d)
            d_ml = coin_2_scint(m, s2, s3, theta_d, phi_d)
        t = coin_3_scint(m, s1, s2, s3, theta_d, phi_d)
        doppie += d
        doppie_um += d_um
        doppie_ml += d_ml
        triple += t
        n += 1
    print(f'Number of muons generated to get {numero_che_voglio + 1} conteggi up: {n}')
    print('numero di doppie: ', doppie, ', numero di triple: ', triple)
    print('efficienza doppie/triple: ', doppie/triple)
    print('doppie up-middle: ', doppie_um)
    print('doppie middle-down: ', doppie_ml)
    
    # print(np.sqrt(s1.upper_z**2 + s1.right_y**2 + s1.pos_x**2))
    # print(np.sqrt(s2.upper_z**2 + s2.right_y**2 + s2.pos_x**2))
    # print(np.sqrt(s3.upper_z**2 + s3.right_y**2 + s3.pos_x**2))


    # samples = sample_cos2(10000)
    
    # # Bins per istogramma
    # bins = 80

    # # Range
    # xmin, xmax = -np.pi/2, np.pi/2

    # # Plot istogramma normalizzato
    # plt.hist(samples, bins=bins, range=(xmin, xmax),
    #          density=True, alpha=0.5, label="Sampled histogram")

    # # PDF teorica normalizzata:
    # # p(x) = (3/4) * cos^2(x)  su [-pi/2, pi/2]
    # # (costante ottenuta integrando)
    # x_plot = np.linspace(xmin, xmax, 500)
    # pdf = (3/4) * np.cos(x_plot)**2

    # plt.plot(x_plot, pdf, 'r-', lw=2, label="Theory: (3/4) cos²(x)")

    # plt.xlabel("x")
    # plt.ylabel("PDF")
    # plt.title("Sampling distribution ∝ cos²(x) on [-π/2, π/2]")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

