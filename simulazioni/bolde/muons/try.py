from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
from typing import Callable
from random import random
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt



MATH_ERROR = 1e-14

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


# Calculate area using the Shoelace formula
def shoelace_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2



class scintillatore:
    def __init__(self , lenght , height , depth , name = ""):
        self.lenght = lenght
        self.height = height
        self.depth = depth
        self.name = name

        # init position in origin
        self.position(0 , 0 , 0)

        pass

    def position( self , x , y , z):
        self.x1 = x - self.lenght/2
        self.x2 = x + self.lenght/2
        self.y1 = y - self.depth/2
        self.y2 = y + self.depth/2
        self.z1 = z - self.height/2
        self.z2 = z + self.height/2


class muone:
    def __init__(self , L , z):
        self.x = L*random() - L/2
        self.y = L*random() - L/2
        self.z = z

    def position(self , x , y):
        self.x = x
        self.y = y


    def angle_generation( self , theta , phi) :

        self.theta = theta
        self.phi = phi


if __name__ == '__main__':
    a = scintillatore( 100, 1 , 100)
    b = scintillatore( 100 , 1 , 100)
    b.position( 0 , 75 , 3)
    m = muone(1 , 7)
    m.angle_generation(np.pi/2 , np.pi/2)

    position_matrix = np.array([ np.array([(i/40 , j/40) for i in range(-6000 , 6001 , 1)]) for j in range(-6000 , 6001, 1)])

    vertex = []
    already_on = False
    for j in range( len(position_matrix)):
        for i in range(len(position_matrix[j])):
            m.position(*position_matrix[i,j])
            if intersection(m , a) & intersection(m, b):
                if not already_on:
                    vertex.append(position_matrix[i,j])
                    already_on = True
            else:
                if already_on:
                    already_on = False
                    vertex.append(position_matrix[i,j])

    print( vertex[0])
    print( vertex[1])
    print( vertex[-2])
    print( vertex[-1])
    

    area = shoelace_area([vertex[0], vertex[1], vertex[-1], vertex[-2]])
    print(f"Area: {area}")


    m.position(50-1e-14 , 0)
    print(intersection(m , a))

    xs, ys = zip(*vertex)
    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys, s=4, alpha=0.8, color="gray")
    plt.plot(
        [vertex[0][0], vertex[1][0], vertex[-1][0], vertex[-2][0], vertex[0][0]],
        [vertex[0][1], vertex[1][1], vertex[-1][1], vertex[-2][1], vertex[0][1]],
        color="orange"
    )

    plt.title("Muon Intersection Boundary")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))

    # plt.minorticks_on()
    plt.grid(True, which="major", linestyle="-", alpha=0.5)
    plt.grid(True, which="minor", linestyle="--", alpha=0.25)
    plt.tick_params(axis="both", which="major", labelsize=9)
    plt.tick_params(axis="both", which="minor", labelsize=7)

    plt.show()

    