from scipy.integrate import quad, trapezoid
import numpy as np

def f( x , h , l):
    return 2*(np.pi - (np.arctan(h/(l-x)) + np.arctan(h/x)))

L1= 80
L2= 30
H = 27
H2 = 16
i = lambda x: f(x , H , L1)
triple = quad( lambda x: f(x , H , L1) , 0 , L1/2 )[0] * quad(lambda x: f(x , H , L2) , 0 , L2/2 )[0]
doppie = quad( lambda x: f(x , H2 , L1) , 0 , L1/2 )[0] * quad(lambda x: f(x , H2 , L2) , 0 , L2/2 )[0]

print(triple/doppie)


