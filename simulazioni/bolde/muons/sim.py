from random import random
import numpy as np
from scipy.stats import norm
from scipy.integrate import trapezoid
import pandas as pd

from typing import Callable

#! modificare la bot_scintillatorenerazione dei muoni, facendola al contrario: partire col 100% di doppie e vedere quali prendono il 3° e quali no


N = 1e5
Lx = 3e2
Ly = 1e2
z = 27

Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8

muon_dist_approx = lambda size=1: norm.rvs(loc = np.pi/2 , scale = 3 , size  = size)

def HoM( pdf: Callable , approx: Callable):
    y = random()
    x = approx()
    if( y < pdf(x)): return x
    return HoM(pdf , approx)

def muon_dist( x ):
    return np.sin(x)**2

class Scintillatore:
    def __init__(self , lenght , height , depth , name = ""):
        self.lenght = lenght
        self.height = height
        self.depth = depth
        self.name = name
        pass

    def position( self , x , y , z):
        self.x1 = x - self.lenght/2
        self.x2 = x + self.lenght/2
        self.y1 = y - self.depth/2
        self.y2 = y + self.depth/2
        self.z1 = z - self.height/2
        self.z2 = z + self.height/2
        
class Materiale(Scintillatore):
    def __init__(self , lenght , height , depth , PDG_file, density , name = "", ):
        super().__init__(lenght , height , depth , name)
        self.PDG = PDG_file
        self.density = density
        self.__setup_radiation_lenght()

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
        self.radiation_lenght = [ trapezoid(1/self.sp[:i] , self.T[:i]) for i in range(1 , len(self.sp))]

    def energy_calculation( self , in_point, out_point , energy):
        distance = np.sum( [(in_point[i] - out_point[i])**2 for i in range(3)])
        if energy in self.T:

        



    

class Muone:
    def __init__(self , Lx = None , Ly = None, z = None , theta=None , phi=None , position = False , angle = False):
        # store modes and optionally initialize position/angle
        self._position_mode = bool(position)
        self._angle_mode = bool(angle)

        # optionally set initial spatial coordinates
        if not np.isnan([Lx , Ly, z]).any():# type: ignore 
            # call the public method which dispatches to the selected mode
            self.sp_coord(Lx, Ly, z)

        # optionally set initial angles
        if not np.isnan([Lx , Ly, z]).any():# type: ignore 
            # call the public method which dispatches to the selected mode
            self.ang_coord(theta, phi)


    def __random_position(self , Lx , Ly , z):
        self.x = Lx*random() - Lx/2
        self.y = Ly*random() - Ly/2
        self.z = z

    def __determinate_position(self , x , y , z):
        self.x = x
        self.y = y 
        self.z = z

    def sp_coord(self, *args, **kwargs):
        if self._position_mode:
            return self.__determinate_position(*args, **kwargs)
        return self.__random_position(*args, **kwargs)

    def __angle_generation( self , S_b:Scintillatore|None = None , S_t: Scintillatore|None = None) :

        self.theta = HoM( muon_dist , muon_dist_approx)
        self.phi = HoM( muon_dist , muon_dist_approx)
        pass

    def __determinate_angle(self, theta , phi):
        self.theta = theta
        self.phi = phi

    def ang_coord(self, *args, **kwargs):
        if self._angle_mode:
            return self.__determinate_angle(*args, **kwargs)
        return self.__angle_generation(*args, **kwargs)



def projection( m , z):
    dx = (m.z-z) / np.tan( m.theta )
    dy = (m.z-z) / np.tan( m.phi)
    x1 = m.x + dx
    y1 = m.y + dy
    return x1 , y1

def intersection( m: Muone , S: Scintillatore):

    bool_x = False
    bool_y = False
    x1,y1 = projection( m , S.z1)
    x2,y2 = projection( m , S.z2)

    
    # Left to right pass through the side of the scintillator
    if x1 < S.x1:
        if x2 > S.x1:
            bool_x = True
    # Enter from the top, it's already in the scintillator
    elif (x1 <= S.x2) and (x1 >= S.x1):
        bool_x = True

    # Right to Left pass through the side of the scintillator
    elif x1 > S.x2:
        if x2 < S.x2:
            bool_x = True

    

    # Top to Bottom pass through the side of the scintillator
    if y1 < S.y1:
        if y2 > S.y1:
            bool_y = True

    # Enter from the top, it's already in the scintillator
    elif (y1 <= S.y2) and (y1 >= S.y1):
        bool_y = True

    # Bottom to Top pass through the side of the scintillator
    elif y1 > S.y2:
        if y2 < S.y2:
            bool_y = True

    return (bool_x & bool_y)

def energy_evaluation( m: Muone , Giunone: Scintillatore,  Minerva: Scintillatore, materiale: Materiale)

def sim(
    top_pos: tuple[float, float, float],
    middle_pos: tuple[float, float, float],
    bot_pos: tuple[float, float, float],
    thin_position: int = 1,  # 0=bottom, 1=middle, 2=top
    top_name: str = "Minerva",
    middle_name: str = "Partenope",
    bot_name: str = "Giunone"
) -> tuple[int, int, int]:
    # Set thickness: 1 for thin, 3 for thick
    thicknesses: list[int] = [4,4,4]
    if thin_position == 0:
        thicknesses[0] = 2
    elif thin_position == 1:
        thicknesses[1] = 2
    elif thin_position == 2:
        thicknesses[2] = 2

    bot_scintillator: Scintillatore = Scintillatore(80, thicknesses[0], 30, bot_name)
    middle_scintillator: Scintillatore = Scintillatore(80, thicknesses[1], 30, middle_name)
    top_scintillator: Scintillatore = Scintillatore(80, thicknesses[2], 30, top_name)
    
    bot_scintillator.position(*bot_pos)
    top_scintillator.position(*top_pos)
    middle_scintillator.position(*middle_pos)

    doppie: int = 0
    triple: int = 0
    flag: int = 0

    while doppie < N:
        m: Muone = Muone(Lx , Ly, z)
        m.ang_coord(bot_scintillator, middle_scintillator)
        
        flag_B: bool = intersection(m, bot_scintillator)
        flag_T: bool = intersection(m, top_scintillator)
        flag_M: bool = intersection(m, middle_scintillator)

        del m

        if (flag_T | flag_B | flag_M):
            flag += 1
        if (flag_T & flag_B):
            doppie += 1
        if (flag_M & flag_T & flag_B):
            triple += 1
            energy_evaluation( m , top_scintillator , middle_scintillator)

        perc: int = int(np.round(doppie / N * 20))

        string: str = (
            "[" + "#" * perc + "-" * (20 - perc) + "]\t"
            + str(triple) + "/" + str(doppie)
        )
        print("\r" + string, end="", flush=True)
    print("\r" + " "*3*len(string) , end="", flush=True )
    return doppie, triple, flag



if __name__ == "__main__":


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
    n = 0
    G = Scintillatore( 80 , 3 , 30 , "Giunone")
    M = Scintillatore( 80 , 1 , 30 , "Minerva")
    P = Scintillatore( 80 , 3 , 30 , "Partenope")

    G.position( 0 , 0 , 0)
    M.position( 0 , 0 , Hb_2)
    P.position( 0 , 0 , Ha_2)

    doppie = 0
    triple = 0
    flag = 0

    while( n < N):
        m = Muone( Lx , Ly , z)
        m.ang_coord( G , P)
        iG = intersection( m , G)
        iM = intersection( m , M)
        iP = intersection( m , P)


        if iM | iG | iP:
            flag+=1
        if iM & iG:
            doppie += 1
        if iP & iM & iG:
            triple +=1


        perc = int(np.round(n/N * 20))

        string = "[" + "#"*perc + "-"*(20 - perc) + "]\t" + str(triple) +"/"+str(doppie)+"\t\t"+ str(flag)
        print("\r" + string, end="", flush=True)
        n+=1
    print("\n confibot_scintillatorurazione PMbot_scintillator\t", triple/doppie)
    # print( flabot_scintillator , "\n")

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
    n = 0
    P = Scintillatore( 80 , 3 , 30 , "Partenope")
    G = Scintillatore( 80 , 3 , 30 , "bot_scintillatoriunone")
    M = Scintillatore( 80 , 1 , 30 , "Minerva")

    G.position( 0 , 0 , 0)
    P.position( 0 , 0 , Hb_2)
    M.position( 0 , 0 , Ha_2)

    flag = 0
    doppie = 0
    triple = 0

    while( n < N):
        m = Muone( Lx , Ly , z)
        m.ang_coord( G , M)
        iG = intersection( m , G)
        iP = intersection( m , P)
        iM = intersection( m , M)

        del m

        if iM | iG | iP:
            flag+=1
        if iG & iP:
            doppie += 1
        if (iP & iM) & iG:
            triple +=1


        perc = int(np.round(n/N * 20))

        string = "[" + "#"*perc + "-"*(20 - perc) + "]\t" + str(triple) +"/"+str(doppie)
        print("\r" + string, end="", flush=True)
        n+=1
    print(" \n confibot_scintillatorurazione MPbot_scintillator: \t", triple/doppie)
    # print( flabot_scintillator , "\n")




        