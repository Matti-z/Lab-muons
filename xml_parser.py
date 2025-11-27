from xml.etree.ElementTree import parse
from os.path import isfile
import matplotlib.pyplot as plt


#TODO: Conversion sampling units -> time
#TODO: Convertion digital value -> volts

def xml_digitizer_parser(path:str = "")->list:

    if not isfile(path):
        raise FileNotFoundError(f"XML file not found: {path}")
    tree = parse("prova_xml.xml")
    root = tree.getroot()

    events = []

    for event in root.findall("event"):
        trace = event.find("trace").text
        id = event.get("id")
        time_stamp = event.get("timestamp")
        clock_time = event.get("clocktime")
        events.append([int(x) for x in trace.split()])
        
    return events
    

if __name__ == "__main__":
    a =xml_digitizer_parser("prova_xml.xml")
    plt.plot(a)
    plt.show()