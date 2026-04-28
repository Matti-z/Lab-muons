from random import random
import numpy as np
from scipy.stats import norm
from scipy.integrate import trapezoid
import pandas as pd

from typing import Callable
from classes import Muone, Scintillatore

#! modificare la bot_scintillatorenerazione dei muoni, facendola al contrario: partire col 100% di doppie e vedere quali prendono il 3° e quali no


N = 1e5
Lx = 5e2
Ly = 5e2
z = 27

Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8




def projection( m , z):
    dx = (m.z-z) / np.tan( m.theta )
    dy = (m.z-z) / np.tan( m.phi)
    x1 = m.x + dx
    y1 = m.y + dy
    return x1 , y1

def find_points( m:Muone , S:Scintillatore):
    x1,y1 = projection( m , S.z1)
    x2,y2 = projection( m , S.z2)
    return (x1,y1,S.z1) , (x2,y2,S.z2)    


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
    
def inverse_line( y , m , a):
    return (y - a)/m   

def is_inside( point:tuple[float,float,float] , x_range , y_range, z_range):
    range_list = [x_range , y_range , z_range]
    return all([range_list[i][0] < point[i] < range_list[i][1] for i in range(3)])

def edge_finding( muone:Muone , S: Scintillatore):
    
    starting_point, ending_point = find_points(muone , S)
    
    x_range = ( S.x1 , S.x2)
    y_range = ( S.y1 , S.y2)
    z_range = (S.z1 , S.z2)

    m = ( np.diff(x_range)/np.diff(z_range) , np.diff(y_range)/ np.diff(z_range))
    a = (x_range[0] - m[0]*z_range[0] , y_range[0] - m[1]*z_range[0])

    z_x = lambda x: inverse_line( x , m[0] , a[0])
    z_y = lambda y: inverse_line( y , m[1], a[1])

    y_x = lambda x: m[1]*z_x(x) + a[1]
    x_y = lambda y: m[0]* z_y(y) + a[0]
    
    x_edges = [ [x , y_x(x) , z_x(x)] for x in x_range]
    y_edges = [ [x_y(y), y , z_y(y)] for y in y_range]
    z_edges = [ [l[0] , l[1] , l[2]] for l in [starting_point , ending_point]]

    list_possible_vertex = np.concatenate(( x_edges , y_edges , z_edges ))

    valid_vertex = []

    for vertex in list_possible_vertex:
        if is_inside( vertex , x_range, y_range, z_range):
            valid_vertex.append(vertex)

    if len(valid_vertex) != 2: raise ValueError("Non funziona :-( , len= "+str(len(valid_vertex)))
    return valid_vertex[0] , valid_vertex[1]








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
    thicknesses[thin_position] = 2

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




        