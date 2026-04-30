from random import random
import numpy as np
from scipy.stats import norm
from scipy.integrate import trapezoid
import pandas as pd

from typing import Callable

muon_dist_approx = norm(np.pi/2 , 2)
muon_dist = lambda x: np.where((x > 0) & (x<np.pi) , np.sin(x)**(2/3), 0)

def HoM( pdf: Callable , approx):
    y = random()
    x = approx.rvs()
    if( y < pdf(x)): return x
    return HoM(pdf , approx)

def muon_dist( x ):
    return np.sin(x)**2



class Materiale:
    def __init__(self , PDG_file, density ):
        self.PDG = PDG_file
        self.density = density
        self.__setup_radiation_lenght()
        pass

    def __import_file( self):
        df = pd.read_csv(
            self.PDG,
            sep=r"\s+",
            skiprows=10,
            header=None,
            names=["T", "p", "Ionization", "brems", "pair", "photonuc", "Radloss", "dE/dx", "CSDA Range", "delta", "beta", "dE/dx_R"]
        )
        df = df[(df["CSDA Range"] != 'Muon')]
        df = df[(df["CSDA Range"] != 'Minimum')]
        df = df.astype({
            "T": float,
            "p": float,
            "Ionization": float,
            "brems": float,
            "pair": float,
            "photonuc": float,
            "Radloss": float,
            "dE/dx": float,
            "CSDA Range": float,
            "delta": float,
            "beta": float,
            "dE/dx_R": float,
        })
        self.df = df

    def __setup_radiation_lenght(self):
        self.__import_file()
        self.T = self.df["T"].to_numpy() # kinetic energy
        self.sp = self.density * self.df["dE/dx"].to_numpy() # stopping power
        self.radiation_lenght = np.array([ trapezoid(1/self.sp[:i] , self.T[:i]) for i in range(1 , len(self.sp))])
        self.radiation_lenght = np.insert( self.radiation_lenght , 0 , 0)

    
    def __create_point( self, x: np.ndarray , y: np.ndarray , x0: float):
        if x0 in x:
            # check if point is already inside the array
            y0 = y[x == x0]
            return y0
        else:
            # interpolate linearly to evaluate the point
            i2 = np.where( (x - x0) > 0, x , np.inf).argmin()
            i1 = i2-1

            m = (y[i1] - y[i2])/(x[i1] - x[i2])
            a = y[i1] - m*x[i1]
            return m*x0 + a

    def energy_calculation( self , in_point, out_point , energy):
        distance = np.sum( [(in_point[i] - out_point[i])**2 for i in range(3)])
        
        starting_point = self.__create_point( self.T , self.radiation_lenght , energy)
        ending_point = starting_point + distance

        if ending_point < 0:
            return 0
        
        ending_energy = self.__create_point( self.radiation_lenght , self.T , ending_point)
        return ending_energy


class Scintillatore(Materiale):
    def __init__(self , lenght , height , depth , PDG = None , density = None ,  name = "" ):
        self.lenght = lenght
        self.height = height
        self.depth = depth
        self.name = name
        # Call parent initializer only when PDG (file path) and density are provided
        if isinstance(PDG, str) and (density is not None):
            super().__init__(PDG, density)
        pass
            

    def position( self , x , y , z):
        self.x1 = x - self.lenght/2
        self.x2 = x + self.lenght/2
        self.y1 = y - self.depth/2
        self.y2 = y + self.depth/2
        self.z1 = z - self.height/2
        self.z2 = z + self.height/2
        


    

class Muone:
    def __init__(self , Lx:float = 0 , Ly:float = 0, z:float = 0 , theta=None , phi=None , position = False , angle = False):
        # store modes and optionally initialize position/angle
        self._position_mode = bool(position)
        self._angle_mode = bool(angle)

        self.shift_x = 0
        self.shift_y = 0
        self.shift_z = 0

        self.Lx = Lx
        self.Ly = Ly
        self.z = z + self.shift_z

        # optionally set initial spatial coordinates
        if Lx is not None or Ly is not None or z is not None:
            # call the public method which dispatches to the selected mode
            self.sp_coord(Lx, Ly, z)

        # optionally set initial angles
        if theta is not None or phi is not None:
            # call the public method which dispatches to the selected mode
            self.ang_coord(theta, phi)
        pass


    def __random_position(self):
        self.x = self.Lx*random() - self.Lx/2 + self.shift_x
        self.y = self.Ly*random() - self.Ly/2 + self.shift_y

    def __determinate_position(self , x , y , z):
        self.x = x
        self.y = y 
        self.z = z

    def sp_coord(self, x = None , y = None , z = None):
        if self._position_mode or (x is not None or y is not None or z is not None): 
            return self.__determinate_position(x , y, z)
        return self.__random_position()
    
    def shift_sp_coord( self  , x= 0 , y= 0 , z= 0):
        self.shift_x = x
        self.shift_y = y
        self.shift_z = z 
        

    def __angle_generation( self) :

        self.theta = HoM( muon_dist , muon_dist_approx)
        self.phi = HoM( muon_dist , muon_dist_approx)
        pass

    def __determinate_angle(self, theta , phi):
        self.theta = theta
        self.phi = phi

    def ang_coord(self, theta = None, phi= None):
        if self._angle_mode or (theta is not None or phi is not None):
            return self.__determinate_angle(theta , phi)
        return self.__angle_generation()

