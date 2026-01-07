import ROOT
from xml_parser import xml_digitizer_parser

#TODO ancora da realizzare, voglio capire qual è il modo migliore per salvare i dati


def save_array_to_root(array, filename, treename="tree", branchname="data"):
    """Save a numpy array to a ROOT file."""
    file = ROOT.TFile(filename, "UPDATE")
    tree = ROOT.TTree(treename, treename)
    
    # Create a branch and fill it with array data
    branch = tree.Branch(branchname, array, f"{branchname}[{len(array)}]/D")
    tree.Fill()
    
    tree.Write()
    file.Close()