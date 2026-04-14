from random import random
import numpy as np
from scipy.stats import norm
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

muon_dist_approx = norm(np.pi/2 , 2)
muon_dist = lambda x: np.where((x > 0) & (x<np.pi) , np.sin(x)**(2/3), 0)

def HoM( pdf: Callable , approx):
    y = random()
    x = approx.rvs()
    if( y < pdf(x)): return x
    return HoM(pdf , approx)

class scintillatore:
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

class muone:
    def __init__(self , Lx , Ly , z):
        self.x = Lx*random() - Lx/2
        self.y = Ly*random() - Ly/2
        self.z = z

    def angle_generation( self , S_b:scintillatore|None = None , S_t: scintillatore|None = None) :

        self.theta = HoM( muon_dist , muon_dist_approx)
        self.phi = HoM( muon_dist , muon_dist_approx)

        # if type(S_b) is scintillatore and type(S_t) is scintillatore:
        #     if self.x< S_b.x1:
        #         self.theta = random()* (np.arctan((self.z - S_b.z1)/( S_b.x1 - self.x)) - np.arctan((self.z - S_t.z2)/( S_t.x2 - self.x))) + np.arctan((self.z - S_t.z2)/( S_t.x2 - self.x))
        #     if self.x > S_b.x2:
        #         self.theta = random()* (np.arctan((self.z - S_b.z1)/( S_b.x2 - self.x)) - np.arctan((self.z - S_t.z2)/( S_t.x1 - self.x))) + np.arctan((self.z - S_t.z2)/( S_t.x1 - self.x))
        #     if self.y < S_b.y1:
        #         self.phi = random()* (np.arctan((self.z - S_b.z1)/( S_b.y1 - self.y))- np.arctan((self.z - S_t.z2)/( S_t.y2 - self.y))) + np.arctan((self.z - S_t.z2)/( S_t.y2 - self.y))
        #     if self.y > S_b.y2:
        #         self.phi = random()* (np.arctan((self.z - S_b.z1)/( S_b.y2 - self.y))- np.arctan((self.z - S_t.z2)/( S_t.y1 - self.y))) + np.arctan((self.z - S_t.z2)/( S_t.y1 - self.y))
        pass



def projection( m , z):
    dx = (m.z-z) / np.tan( m.theta )
    dy = (m.z-z) / np.tan( m.phi)
    x1 = m.x + dx
    y1 = m.y + dy
    return x1 , y1

def intersection( m: muone , S: scintillatore):

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

    bot_scintillator: scintillatore = scintillatore(80, thicknesses[0], 30, bot_name)
    middle_scintillator: scintillatore = scintillatore(80, thicknesses[1], 30, middle_name)
    top_scintillator: scintillatore = scintillatore(80, thicknesses[2], 30, top_name)
    
    bot_scintillator.position(*bot_pos)
    top_scintillator.position(*top_pos)
    middle_scintillator.position(*middle_pos)

    doppie: int = 0
    triple: int = 0
    flag: int = 0

    while doppie < N:
        m: muone = muone(Lx , Ly, z)
        m.angle_generation(bot_scintillator, middle_scintillator)
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
    G = scintillatore( 80 , 3 , 30 , "Giunone")
    M = scintillatore( 80 , 1 , 30 , "Minerva")
    P = scintillatore( 80 , 3 , 30 , "Partenope")

    G.position( 0 , 0 , 0)
    M.position( 0 , 0 , Hb_2)
    P.position( 0 , 0 , Ha_2)

    doppie = 0
    triple = 0
    flag = 0

    while( n < N):
        m = muone( Lx , Ly , z)
        m.angle_generation( G , P)
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
    P = scintillatore( 80 , 3 , 30 , "Partenope")
    G = scintillatore( 80 , 3 , 30 , "bot_scintillatoriunone")
    M = scintillatore( 80 , 1 , 30 , "Minerva")

    G.position( 0 , 0 , 0)
    P.position( 0 , 0 , Hb_2)
    M.position( 0 , 0 , Ha_2)

    flag = 0
    doppie = 0
    triple = 0

    while( n < N):
        m = muone( Lx , Ly , z)
        m.angle_generation( G , M)
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




        