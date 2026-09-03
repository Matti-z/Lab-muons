import os
import subprocess
from pathlib import Path

# try:
#     from drive_sync import sync_local_folder_to_drive
# except ImportError:
#     sync_local_folder_to_drive = None


default_dir = str(Path(".").resolve()).split("/Lab-muons")[0] + "/Lab-muons/"
universal_dir = lambda path: default_dir + path
# list of xml files (converted from inline filenames)


big_data = universal_dir("big_data/asymm/")
print("\n")
print(big_data)


file = "xml_csv_parser_multichannel"
file = "muon_precession_parser"
drive = True

c = [big_data + "s_f_1707.xml" , big_data + "s_f_2407.xml" , big_data + "s_f_2707.xml" ,]

for i in c:
    xml_path = i
    xml_filename = xml_path.split("/")[-1].removesuffix(".xml")
    csv_folder = universal_dir("Data/timestamp/")
    csv_settings_folder = universal_dir("Data/settings/")

    os.makedirs(os.path.dirname(csv_folder), exist_ok=True)
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

    # if sync_local_folder_to_drive is not None:
    #     sync_local_folder_to_drive()
