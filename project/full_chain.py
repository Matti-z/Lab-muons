import subprocess
import os
from pathlib import Path
from root_to_timestamp import process_root_files, root_settings_to_csv
# from drive_sync import sync_local_folder_to_drive



default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
universal_dir = lambda path: default_dir + path

xml_path = universal_dir("big_data/11_02_2026_17_52.xml")
xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
csv_path = universal_dir("Data/timestamp/"+xml_filename+".csv")
csv_settings_path = universal_dir("Data/settings/"+ xml_filename + ".csv")



root_path = universal_dir("big_data/root/"+xml_filename+"/")


os.makedirs(os.path.dirname(csv_path), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)
os.makedirs(os.path.dirname(csv_settings_path), exist_ok=True)


result = subprocess.run([universal_dir("project/parser"), xml_path, root_path], capture_output=False)
if result.returncode != 0:
    print(result.stderr)
process_root_files(root_path , csv_path)
root_settings_to_csv( root_path , csv_settings_path)

subprocess.run(['git', 'add', universal_dir("Data/timestamp/*") , universal_dir("Data/settings/*")], capture_output=False)
subprocess.run(['git', 'commit', '-m', 'Update timestamp data ' + xml_filename], capture_output=False)
subprocess.run(['git', 'push'], capture_output=False)



# copy files to drive, if not configure, comment it out
# sync_local_folder_to_drive()


