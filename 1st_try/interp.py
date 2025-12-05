import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares

name = "giunone.csv"
# cut_up = 18
# cut_down = 3
cut_up = 0
cut_down = 100

def model_line( x:float , m:float , q:float)->float:
    return m*x+q




if __name__ == "__main__":


    # try to read with column names, fall back to plain numeric load
    try:
        data = np.genfromtxt(name, delimiter=",", names=True, dtype=None, encoding=None)
        print("Detected columns:", data.dtype.names)
        print("First rows:")
        for row in data[:5]:
            print(row)
        # example unpack if at least two named columns exist
        
        x = data[data.dtype.names[0]]
        y = data[data.dtype.names[1]]
        sy = data[data.dtype.names[2]]
        print(f"Loaded {x.size} points from columns {data.dtype.names[0]}, {data.dtype.names[1]}")
    except Exception:
        data = np.loadtxt(name, delimiter=",")
        print("Loaded numeric array with shape", data.shape)
        print("First rows:\n", data[:5])
        
        x, y ,sy = data[:, 0], data[:, 1], data[:,2]
        print(f"Using first two columns as x/y with {x.size} points")


    points = [ 0 , cut_down , cut_up , len(x)]
    # for i in range(1 , len(points)):
    #     cutted_x = x[points[i-1] , points[i]]
    #     cutted_y = y[points[i-1] , points[i]]
    #     cutted_sy = sy[points[i-1] , points[i]]
    #     ls = LeastSquares(cutted_x , cutted_y , cutted_sy , model_line)
    #     m = Minuit(ls , m=1 , q = 1)
    #     m.migrad()
    #     m.hesse()
    
    p_x = x[cut_down : cut_up]
    p_y = y[cut_down : cut_up]
    p_sy = sy[cut_down : cut_up]

    plt.errorbar(x,y,sy)
    plt.show()
    ls = LeastSquares( x , y , sy , model_line)
    m = Minuit( ls , m = 1 , q = 1)
    m.migrad()
    m.hesse()
    print(m)

    plt.errorbar( x , y , sy , fmt="o")
    plot_x = np.linspace( x[0] , x[-1])
    plot_y = model_line( plot_x , *m.values)
    plt.plot(plot_x , plot_y)
    plt.show()

    