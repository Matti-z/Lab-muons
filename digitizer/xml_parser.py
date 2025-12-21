from xml.etree.ElementTree import parse
from os.path import isfile
import matplotlib.pyplot as plt
from numpy import arange


#TODO: Conversion sampling units -> time
#TODO: Convertion digital value -> volts
#! studiare CAEN wave pulse per vedere se da terminale funziona


def xml_digitizer_parser(path:str = "")->list:

    if not isfile(path):
        raise FileNotFoundError(f"XML file not found: {path}")
    tree = parse(path)
    root = tree.getroot()

    events = []
    digitizer = root.find("digitizer")
    frequency = float(digitizer.find("frequency").get("hz"))

    settings = root.find("settings")
    size = float(settings.find("window").get("size"))

    time = arange( size)/frequency


    for event in root.findall("event"):
        trace = event.find("trace").text
        id = event.get("id")
        time_stamp = event.get("timestamp")
        clock_time = event.get("clocktime")
        
        events.append([int(x) for x in trace.split()])
    
    return events , time , frequency
    

if __name__ == "__main__":
    a , b , c=xml_digitizer_parser("prova_xml.xml")

    for i in a:
        plt.plot(b , i)
        plt.show()
