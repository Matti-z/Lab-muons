import csv
import sys

def remove_trailing_zeros_from_csv(input_file, output_file=None):
    """
    Read a CSV file and remove all trailing rows that contain only zeros.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file (defaults to input file)
    """
    if output_file is None:
        output_file = input_file
    
    # Read the CSV file
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Remove trailing rows with all zeros
    while rows and all(float(val) == 0.0 for val in rows[-1] if val):
        rows.pop()
    
    # Write back to file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Processed {input_file} and saved to {output_file}")

if __name__ == "__main__":
    input_csv = "Data/timestamp/2026-01-08.csv"  # Change to your CSV file path
    remove_trailing_zeros_from_csv(input_csv , input_csv)