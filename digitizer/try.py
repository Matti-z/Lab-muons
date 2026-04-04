import os
import sys


def rename_csv_files(directory):
    """Rename all .csv files to _cfg.csv in the given directory."""
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return
    
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            old_path = os.path.join(directory, filename)
            new_filename = filename.replace('.csv', '_cfg.csv')
            new_path = os.path.join(directory, new_filename)
            
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":    
    rename_csv_files("Data/settings")