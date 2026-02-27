import subprocess
import os
from pathlib import Path
from root_to_timestamp import process_root_files, root_settings_to_csv





default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
universal_dir = lambda path: default_dir + path





invertito = True
drive = False
xml_path = universal_dir("big_data/error_prop_100ns.xml")
xml_filename = xml_path.split('/')[-1].removesuffix(".xml")
csv_folder = universal_dir("Data/timestamp/")
csv_settings_folder = universal_dir("Data/settings/")



root_path = universal_dir("big_data/root/"+xml_filename+"/")


os.makedirs(os.path.dirname(csv_folder), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)
os.makedirs(os.path.dirname(csv_settings_folder), exist_ok=True)

if invertito:
    result = subprocess.run([universal_dir("project/root_parser"), xml_path, root_path], capture_output=False)
    if result.returncode != 0:
        print(result.stderr)
    process_root_files(root_path , csv_folder , xml_filename)
    root_settings_to_csv( root_path , csv_settings_folder , xml_filename)
else:
    result = subprocess.run([universal_dir("project/csv_parser"), xml_path, csv_folder , csv_settings_folder], capture_output=False)
    csv_path = csv_folder + "/" + xml_filename + ".csv"
    csv_settings_path = csv_settings_folder + "/" + xml_filename + "_cfg.csv"

subprocess.run(['git', 'add', universal_dir("Data/timestamp/*") , universal_dir("Data/settings/*")], capture_output=False)
subprocess.run(['git', 'commit', '-m', 'Update timestamp data ' + xml_filename], capture_output=False)
subprocess.run(['git', 'push'], capture_output=False)


if drive:
    from drive_sync import sync_local_folder_to_drive
    sync_local_folder_to_drive()


