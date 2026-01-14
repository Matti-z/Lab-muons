from xml_parser import xml_digitizer_parser
import timestamp_calculator
import delete_zeros
from datetime import datetime

path_file_scope = '9_1_26_16_00.xml'
path_file_csv = 'Lab-muons/csv'
path_file_output = 'Lab-muons/Data/timestamp'

if __name__ == "__main__":
    xml_digitizer_parser(path_file_scope , path_file_csv)
    print("\nXML parsed and CSV files created.")
    timestamp_calculator.timestamp_parser( path_file_csv , path_file_output, path_file_scope.removesuffix('.xml') + '.csv' )
    print("\nTimestamps extracted and saved.")
    delete_zeros.remove_trailing_zeros_from_csv( path_file_output+ '/' + path_file_scope.removesuffix('.xml') + '.csv' )