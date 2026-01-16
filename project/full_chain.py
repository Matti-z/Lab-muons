import subprocess
import os
from root_to_timestamp import process_root_files

xml_path = "/home/nobolde/coding/Lab-muons/big_data/16_1_2026_16_55.xml"
xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
csv_path = "/home/nobolde/coding/Lab-muons/Data/timestamp/"+xml_filename+".csv"



root_path = "/home/nobolde/coding/Lab-muons/big_data/root/"+xml_filename+"/"


os.makedirs(os.path.dirname(csv_path), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)

# Best approach for calling ./parser with arguments
result = subprocess.run(['/home/nobolde/coding/Lab-muons/project/parser', xml_path, root_path], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
process_root_files(root_path , csv_path)