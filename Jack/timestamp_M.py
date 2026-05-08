import numpy as np
import scipy
from xml.dom import minidom
import matplotlib.pyplot as plt

f=250e6  # Hz
treshold= 120 # mV


if __name__ == "__main__":
    timestamp=[]    
    dom = minidom.parse('Minerva_pure_signal.xml')
    elements = dom.getElementsByTagName('trace')
    #print(f"There are {len(elements)} items")
    #print(elements[0].toxml()[19:-10])

    data=[]

    for el in elements:
    
    
        temp = np.array([float(s) for s in el.toxml()[19:-10].replace(',', ' ').split()])
        x = np.arange(len(temp))

        mean = np.mean(temp)
        tr_converted = mean - treshold * (mean - 1165)/(500)
        
        for i in x:
            if temp[i] < tr_converted:
                temp = temp[i:]
                x= np.arange(len(x[i:]))
                break



        for i in x[13:]:

            if temp[i] < tr_converted:
                timestamp.append(i/f) # seconds
                if temp[i] < tr_converted:
                    i += 1

        '''print(timestamp)

        plt.plot(x/f, temp)
        plt.hlines(tr_converted, 0, x[-1]/f, colors='g')
        
        for ts in timestamp:
            plt.vlines(ts, ymin=min(temp), ymax=max(temp), color='r')
        plt.show()'''
    
    timestamp = np.array(timestamp)
    np.savetxt('timestamps_M.txt', timestamp)
        