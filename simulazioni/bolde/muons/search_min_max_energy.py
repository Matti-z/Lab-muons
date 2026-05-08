from classes import Muone,Scintillatore
from sim import edge_finding, intersection

import numpy as np
N = 1e6
Lx = 150
Ly = 90
z = 27

m_MU = 107

Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8

HAl = 7.2
HNaCl = 0

top_pos = (0 , 0 , Ha_2)
middle_pos = (0 , 0 , Hb_2)
bot_pos = (0 , 0 , 0)
Al_pos = (0 , 0 , HAl)
Na_pos = (0,0,0) #! CAMBIALA
thin_position = 1

top_name: str = "Minerva"
middle_name: str = "Partenope"
bot_name: str = "Giunone"


    

# Set thickness: 1 for thin, 3 for thick
thicknesses: list[int] = [4,4,4]
thicknesses[thin_position] = 2

bot_scintillator: Scintillatore = Scintillatore(80, thicknesses[0], 30, PDG="muons_statistics/muE_Polyvinyltoluene.txt" , density = 1.032 , name = bot_name)
middle_scintillator: Scintillatore = Scintillatore(80, thicknesses[1], 30, PDG="muons_statistics/muE_Polyvinyltoluene.txt" , density = 1.032 , name = middle_name)
top_scintillator: Scintillatore = Scintillatore(80, thicknesses[2], 30, PDG="muons_statistics/muE_Polyvinyltoluene.txt" , density = 1.032 , name = top_name)

Al = Scintillatore( 80 , 3 , 30 , "muons_statistics/muE_Aluminum.txt" , 2.699 , "Aluminum")
Na = Scintillatore( 80 , 5.1 , 30 , "muons_statistics/muE_Sodium_chloride.txt" , 2.170 , name="Sodium Chloride")
bot_scintillator.position(*bot_pos)
top_scintillator.position(*top_pos)
middle_scintillator.position(*middle_pos)
Al.position( *Al_pos)
Na.position( *Na_pos)


m: Muone = Muone(Lx , Ly, z)
m.shift_sp_coord( 40 , 15)

Emin = np.inf
Emax = 0

triple = 0

while triple < N:
    m.sp_coord()
    m.ang_coord()
    
    flag_B: bool = intersection(m, bot_scintillator)
    flag_T: bool = intersection(m, top_scintillator)
    flag_M: bool = intersection(m, middle_scintillator)



    E = 1

    if (flag_M & flag_T):
        # v1 , v2 = edge_finding(m , Al)
        # E= Al.energy_calculation(v1 , v2 , E)
        # v1 , v2 = edge_finding(m , middle_scintillator)
        # E= middle_scintillator.energy_calculation(v1 , v2 , E)
        v1 , v2 = edge_finding(m , top_scintillator)
        E= top_scintillator.energy_calculation(v1 , v2 , E)

        if E > Emax: Emax = E
        if E < Emin: Emin = E

        triple += 1
    
    
        


    perc: int = int(np.round(triple / N * 20))

    string: str = (
        "[" + "#" * perc + "-" * (20 - perc) + "]\t"
        + str(triple)
    )
    print("\r" + string, end="", flush=True)
print("\r" + " "*3*len(string) , end="", flush=True )

print("\n")
print(f"Tmin = {Emin}")
print(f"Tmax = {Emax}")
Emin_tot = Emin + m_MU
Emax_tot = Emax + m_MU
Pmin = np.sqrt(max(Emin_tot**2 - m_MU**2, 0))
Pmax = np.sqrt(max(Emax_tot**2 - m_MU**2, 0))
print(f"E_total(min) = {Emin_tot}")
print(f"p_rel(min) = {Pmin}")
print(f"E_total(max) = {Emax_tot}")
print(f"p_rel(max) = {Pmax}")
print()

