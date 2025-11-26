from xml.etree.ElementTree import parse
from os.path import isfile


def xml_digitizer_parser(path:str = "")->list:

    if not isfile(path):
        raise FileNotFoundError(f"XML file not found: {path}")
    tree = parse("prova_xml.xml")
    root = tree.getroot()

    for event in root.findall("event"):
        trace = event.find("trace").text
        id = event.get("id")
        time_stamp = event.get("timestamp")
        clock_time = event.get("clocktime")
        
        return [int(x) for x in trace.split()]
    

if __name__ == "__main__":
    print(xml_digitizer_parser("prova_xml.xml"))