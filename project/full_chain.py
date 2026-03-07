import subprocess
import os
from pathlib import Path
from root_to_timestamp import process_root_files, root_settings_to_csv

try:
    from drive_sync import sync_local_folder_to_drive
except ImportError:
    sync_local_folder_to_drive = None





default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
universal_dir = lambda path: default_dir + path





file = "multichannel_parser"
drive = True
xml_path = universal_dir("big_data/inverted_26_02_2026_16_57.xml")
xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
csv_folder = universal_dir("Data/timestamp/")
csv_settings_folder = universal_dir("Data/settings/")

print(xml_path)

root_path = universal_dir("big_data/root/"+xml_filename+"/")


os.makedirs(os.path.dirname(csv_folder), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)
os.makedirs(os.path.dirname(csv_settings_folder), exist_ok=True)

if file == "root_parser":
    result = subprocess.run([universal_dir("project/bin/root_parser"), xml_path, root_path], capture_output=False)
    if result.returncode != 0:
        print(result.stderr)
    process_root_files(root_path , csv_folder , xml_filename)
    root_settings_to_csv( root_path , csv_settings_folder , xml_filename)
elif file == "multichannel_parser" or file == "inverse_parser":
    result = subprocess.run([universal_dir("project/bin/" + file), xml_path, csv_folder , csv_settings_folder], capture_output=False)
    csv_path = csv_folder + "/" + xml_filename + ".csv"
    csv_settings_path = csv_settings_folder + "/" + xml_filename + "_cfg.csv"
else:
    raise KeyError("file is not one of the executable")
    

subprocess.run(['git', 'add', universal_dir("Data/timestamp/*") , universal_dir("Data/settings/*")], capture_output=False)
subprocess.run(['git', 'commit', '-m', 'Update timestamp data ' + xml_filename], capture_output=False)
subprocess.run(['git', 'push'], capture_output=False)



if sync_local_folder_to_drive is not None:
    sync_local_folder_to_drive()



