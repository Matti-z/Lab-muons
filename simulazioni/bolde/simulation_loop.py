from sim import sim
import csv


Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8



if __name__ == "__main__":
    height_array = [ [12.8, 8.4, 0], [23, 12.8, 0], [25.3, 12.8, 0] ]
    pos_x_array = [ [0, 0, 0] for _ in range(3) ]
    pos_y_array = [ [0, 0, 0] for _ in range(3) ]

    xyz_array = []
    shift_array = [0, 15, 30, 45, 60, 75]

    for pos_x_row, pos_y_row, height_row in zip(pos_x_array, pos_y_array, height_array):
        # Original entry
        base_entry = [ [x, y, h] for x, y, h in zip(pos_x_row, pos_y_row, height_row) ]
        # Create copies with x coordinate of the second entry set to each value in shift_array
        for shift in shift_array:
            modified_entry = [list(coord) for coord in base_entry]  # Deep copy
            modified_entry[1][0] = shift  # Set x of second entry
            xyz_array.append(modified_entry)
    print( len(xyz_array))
    data_dict ={
        'configuration': [],
        'coordinates': [],
        'doppie': [],
        'triple': [],
        'flag': []
    }

    csv_file = "simulation_results.csv"
    fieldnames = ['configuration', 'coordinates[TtB][x,y,z]', 'doppie', 'triple', 'flag']

    # Write header once at the start
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    for config in xyz_array:
        thin_pos = 1
        configuration = ["p", "m", "g"]
        if config[0][2] == 12.8:
            thin_pos = 2
            configuration = ["m", "p/g", "g/p"]
        doppie, triple, flag = sim((config[2]), (config[1]), (config[0]), thin_pos, *configuration)
        row = {
            'configuration': ' '.join(configuration),
            'coordinates': config,
            'doppie': doppie,
            'triple': triple,
            'flag': flag
        }
        # Append each row after simulation
        with open(csv_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)
