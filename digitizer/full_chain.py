import os
import subprocess
from pathlib import Path

try:
    from drive_sync import sync_local_folder_to_drive
except ImportError:
    sync_local_folder_to_drive = None


default_dir = str(Path(".").resolve()).split("/Lab-muons")[0] + "/Lab-muons/"
universal_dir = lambda path: default_dir + path

a = [
    "s_f_0306.xml",
    "s_f_2505.xml",
    "s_f_2605_bis.xml",
    "s_f_2605.xml",
    "s_f_2905_bis.xml",
    "s_f_2905.xml",
]

print(os.listdir(universal_dir("big_data/asimmetrie")))

f = "s_f_2505.xml"
file = "muon_precession_parser"
drive = True
xml_path = universal_dir("big_data/asimmetrie/" + f)
xml_filename = xml_path.split("/")[-1].removesuffix(".xml")
csv_folder = universal_dir("Data/timestamp/")
csv_settings_folder = universal_dir("Data/settings/")

root_path = universal_dir("big_data/root/" + xml_filename + "/")

os.makedirs(os.path.dirname(csv_folder), exist_ok=True)
os.makedirs(os.path.dirname(xml_path), exist_ok=True)
os.makedirs(os.path.dirname(root_path), exist_ok=True)
os.makedirs(os.path.dirname(csv_settings_folder), exist_ok=True)

subprocess.run(
    [
        universal_dir("digitizer/bin/" + file),
        xml_path,
        csv_folder,
        csv_settings_folder,
    ],
    capture_output=False,
)

subprocess.run(
    [
        "git",
        "add",
        universal_dir("Data/timestamp/*"),
        universal_dir("Data/settings/*"),
    ],
    capture_output=False,
)
subprocess.run(
    ["git", "commit", "-m", "Update timestamp data " + xml_filename],
    capture_output=False,
)
subprocess.run(["git", "push"], capture_output=False)

if sync_local_folder_to_drive is not None:
    sync_local_folder_to_drive()
