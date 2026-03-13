from random import random
import numpy as np
#TODO al posto di montecarlo far andare un punto da +inf a -inf a step costanti e farlo andare diretto al centro del primo scintillatore

#! modificare la bot_scintillatorenerazione dei muoni, facendola al contrario: partire col 100% di doppie e vedere quali prendono il 3° e quali no


N = 1e8
L = 1e2
z = 26

Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8


class scintillatore:
    def __init__(self , l , h , p , name = ""):
        self.l = l
        self.h = h
        self.p = p
        self.name = name
        pass

    def position( self , x , y , z):
        self.x1 = x - self.l/2
        self.x2 = x + self.l/2
        self.y1 = y - self.p/2
        self.y2 = y + self.p/2
        self.z1 = z - self.h/2
        self.z2 = z + self.h/2


class muone:
    def __init__(self , L , z):
        self.x = L*random() - L/2
        self.y = L*random() - L/2
        self.z = z


    def angle_generation( self , S_b:scintillatore|None = None , S_t: scintillatore|None = None) :

        self.theta = np.pi * random()
        self.phi = np.pi * random()

        if type(S_b) is scintillatore and type(S_t) is scintillatore:
            if self.x< S_b.x1:
                self.theta = random()* (np.arctan((self.z - S_b.z1)/( S_b.x1 - self.x)) - np.arctan((self.z - S_t.z2)/( S_t.x2 - self.x))) + np.arctan((self.z - S_t.z2)/( S_t.x2 - self.x))
            if self.x > S_b.x2:
                self.theta = random()* (np.arctan((self.z - S_b.z1)/( S_b.x2 - self.x)) - np.arctan((self.z - S_t.z2)/( S_t.x1 - self.x))) + np.arctan((self.z - S_t.z2)/( S_t.x1 - self.x))
            if self.y < S_b.y1:
                self.phi = random()* (np.arctan((self.z - S_b.z1)/( S_b.y1 - self.y))- np.arctan((self.z - S_t.z2)/( S_t.y2 - self.y))) + np.arctan((self.z - S_t.z2)/( S_t.y2 - self.y))
            if self.y > S_b.y2:
                self.phi = random()* (np.arctan((self.z - S_b.z1)/( S_b.y2 - self.y))- np.arctan((self.z - S_t.z2)/( S_t.y1 - self.y))) + np.arctan((self.z - S_t.z2)/( S_t.y1 - self.y))
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

    

    if x1 < S.x1:
        if x2 > S.x1:
            bool_x = True
    elif (x1 <= S.x2) and (x1 >= S.x1):
        bool_x = True
    elif x1 > S.x2:
        if x2 < S.x2:
            bool_x = True
    
    if y1 < S.y1:
        if y2 > S.y1:
            bool_y = True
    elif (y1 <= S.y2) and (y1 >= S.y1):
        bool_y = True
    elif y1 > S.y2:
        if y2 < S.y2:
            bool_y = True


    return (bool_x & bool_y)



def sim(
    bot_pos: tuple[float, float, float],
    top_pos: tuple[float, float, float],
    middle_pos: tuple[float, float, float],
    thin_position: int = 1,  # 0=bottom, 1=middle, 2=top
    bot_name: str = "Giunone",
    top_name: str = "Minerva",
    middle_name: str = "Partenope"
) -> tuple[int, int, int]:
    n: int = 0
    # Set thickness: 1 for thin, 3 for thick
    thicknesses: list[int] = [3, 3, 3]
    if thin_position == 0:
        thicknesses[0] = 1
    elif thin_position == 1:
        thicknesses[1] = 1
    elif thin_position == 2:
        thicknesses[2] = 1

    bot_scintillator: scintillatore = scintillatore(80, thicknesses[0], 30, bot_name)
    top_scintillator: scintillatore = scintillatore(80, thicknesses[2], 30, top_name)
    middle_scintillator: scintillatore = scintillatore(80, thicknesses[1], 30, middle_name)

    bot_scintillator.position(*bot_pos)
    top_scintillator.position(*top_pos)
    middle_scintillator.position(*middle_pos)

    doppie: int = 0
    triple: int = 0
    flag: int = 0

    while n < N:
        m: muone = muone(L, z)
        m.angle_generation(bot_scintillator, middle_scintillator)
        flag_B: bool = intersection(m, bot_scintillator)
        flag_T: bool = intersection(m, top_scintillator)
        flag_M: bool = intersection(m, middle_scintillator)

        del m

        if flag_T | flag_B | flag_M:
            flag += 1
        if flag_T & flag_M:
            doppie += 1
        if flag_M & flag_T & flag_B:
            triple += 1

        perc: int = int(np.round(n / N * 20))

        string: str = (
            "[" + "#" * perc + "-" * (20 - perc) + "]\t"
            + str(triple) + "/" + str(doppie) + "\t\t" + str(flag)
        )
        print("\r" + string, end="", flush=True)
        n += 1
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
        m = muone( L , z)
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
        m = muone( L , z)
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




        