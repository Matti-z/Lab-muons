from xml.etree.ElementTree import parse
from os.path import isfile
import matplotlib.pyplot as plt
from numpy import arange, array, savetxt, round
from pathlib import Path
from timestamp_calculator import timestamp_parser
from gc import collect
delta_val = 500
#TODO: Conversion sampling units -> time
#TODO: Convertion digital value -> volts
#! studiare CAEN wave pulse per vedere se da terminale funziona


def xml_digitizer_parser(xml_file_path:str = "" , csv_folder_path:str = "")->list:

    if not isfile(xml_file_path):
        raise FileNotFoundError(f"XML file not found: {xml_file_path}")
    tree = parse(xml_file_path)
    print("file parsed\n")
    root = tree.getroot()

    events = []
    digitizer = root.find("digitizer")
    frequency = float(digitizer.find("frequency").get("hz"))

    settings = root.find("settings")
    size = float(settings.find("window").get("size"))

    time = arange( size)/frequency

    event_id = root.findall("event")
    print("event_id done\n")
    id_max = event_id[-1].get("id")

    for event in event_id:
        trace = event.find("trace").text
        id = event.get("id")
        time_stamp = event.get("timestamp")
        clock_time = event.get("clocktime")

        perc: int = int(round(int(id) / int(id_max) * 30))
        string: str = (
            "[" + "#" * perc + "-" * (30 - perc) + "]\t" + id + "/" + id_max)
        print("\r" + string, end="", flush=True)
    
        event_list =  [int(x) for x in trace.split()]
        if (abs(min(event_list) - max(event_list)) > delta_val) and len(event_list) == 1024:
            csv_filename = str(csv_folder_path)+"/"+id+".csv"
            savetxt( csv_filename , event_list , delimiter=",", fmt='%d')
    del tree
    del root
    del event_list
    del event_id
    collect()
