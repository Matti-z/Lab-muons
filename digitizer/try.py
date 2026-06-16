import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np


tree = ET.parse("digitizer/dMinerva_22_05_2026_8_54.xml")
root = tree.getroot()
# print(root.tag)

for child in root:
    if child.tag == "event":
        token = 0
        for a in child:
            
            if a.tag == "trace":
                b = [ int(p) + 1000*token for p in a.text.split()]
                plt.plot(b , label = f"{token}")
                token +=1
        plt.vlines(len(b)-300 , ymin = 0 , ymax=6000)
        plt.legend()
        plt.show()