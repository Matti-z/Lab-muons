from random import *
import numpy as np

#TODO al posto di montecarlo far andare un punto da +inf a -inf a step costanti e farlo andare diretto al centro del primo scintillatore

#! modificare la generazione dei muoni, facendola al contrario: partire col 100% di doppie e vedere quali prendono il 3° e quali no


N = 1e7
L = 1e3
z = 26

H1 = 23
H2 = 13


class scintillatore:
    def __init__(self , l , h , p):
        self.l = l
        self.h = h
        self.p = p
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


    def angle_gen( self , S:scintillatore = 0) :

        self.theta = np.pi * random()
        self.phi = np.pi * random()


        if S is scintillatore:
            if self.x< S.x1:
                self.theta = random()* np.arctan((self.z - S.z1)/( S.x1 - self.x))
            if self.x > S.x2:
                self.theta = random()* np.arctan((self.z - S.z1)/( S.x2 - self.x))
            if self.y < S.y1:
                self.phi = random()* np.arctan((self.z - S.z1)/( S.y1 - self.y))
            if self.y > S.y2:
                self.phi = random()* np.arctan((self.z - S.z1)/( S.y2 - self.y))
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
    elif x1 < S.x2:
        bool_x = True
    if x1 > S.x2:
        if x2 < S.x2:
            bool_x = True
    
    if y1 < S.y1:
        if y2 > S.y1:
            bool_y = True
    elif y1 < S.y2:
        bool_y = True
    if y1 > S.y2:
        if y2 < S.y2:
            bool_y = True
    

    return (bool_x & bool_y)






if __name__ == "__main__":
    n = 0
    P = scintillatore( 80 , 4 , 30)
    G = scintillatore( 80 , 4 , 30)
    M = scintillatore( 80 , 2 , 30)

    G.position( 0 , 0 , 0)
    P.position( 0 , 0 , H1)
    M.position( 0 , 0 , H2)

    doppie = 0
    triple = 0

    while( n < N):
        m = muone( L , z)
        m.angle_gen( G )
        iG = intersection( m , G)
        iM = intersection( m , M)
        iP = intersection( m , P)

        if iM & iP:
            doppie += 1
        if (iP & iM) & iG:
            triple +=1


        perc = int(np.round(n/N * 20))
        #string = "[" + "="*perc + "-"*(20 - perc) + "]" + "\tratio: " + (str((triple/doppie)*100) if doppie != 0 else "0") +  "%\t"+ str(doppie) +"\t/"+str(triple)
        string = "[" + "="*perc + "-"*(20 - perc) + "]\t" + str(triple) +"/"+str(doppie)
        print("\r" + string, end="", flush=True)
        n+=1
    print("/n", triple/doppie)




        