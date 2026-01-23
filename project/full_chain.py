import subprocess
import os
from pathlib import Path
from root_to_timestamp import process_root_files
from drive_sync import sync_local_folder_to_drive



default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
universal_dir = lambda path: default_dir + path

xml_path = universal_dir("big_data/21_01_2024_17_42.xml")
xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
csv_path = universal_dir("Data/timestamp/"+xml_filename+".csv")



root_path = universal_dir("big_data/root/"+xml_filename+"/")


os.makedirs(os.path.dirname(csv_path), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)

# Best approach for calling ./parser with arguments
result = subprocess.run([universal_dir("project/parser_mac"), xml_path, root_path], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
process_root_files(root_path , csv_path)

subprocess.run(['git', 'add', universal_dir("Data/timestamp/*")], capture_output=True)
subprocess.run(['git', 'commit', '-m', 'Update timestamp data ' + xml_filename], capture_output=True)
subprocess.run(['git', 'push'], capture_output=True)



# copy files to drive, if not configure, comment it out
sync_local_folder_to_drive()


