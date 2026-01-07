from xml.etree.ElementTree import parse
from os.path import isfile
import matplotlib.pyplot as plt
from numpy import arange, array, savetxt, round



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
    event_list = root.findall("event")
    id_max = event_list[-1].get("id")

    for event in event_list:
        trace = event.find("trace").text
        id = event.get("id")
        time_stamp = event.get("timestamp")
        clock_time = event.get("clocktime")

        perc: int = int(round(id / id_max * 20))
        string: str = (
            "[" + "#" * perc + "-" * (20 - perc) + "]\t")
        print("\r" + string, end="", flush=True)
    
        event_list =  [int(x) for x in trace.split()]
        csv_filename = "/Users/ibolde/coding/big_data/natale/"+id+".csv"
        savetxt( csv_filename , event_list , delimiter=",", fmt='%d')
    
    

if __name__ == "__main__":
    xml_digitizer_parser("/Users/ibolde/Desktop/buon_anno.xml")
