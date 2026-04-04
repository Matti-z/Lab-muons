from sim import sim

from pathlib import Path

dir_path = Path(__file__).parent.resolve()



Ha_1 = 12.8
Hb_1 = 8.4

Ha_2 = 23
Hb_2 = 12.8

Ha_3 = 25.3
Hb_3 = 12.8

g = "giunone"
m = "minerva"
p = "partenope"

if __name__ == "__main__":
    top_coordinates = [( 0 , 0 , Ha_1) , (0 , 0 , Ha_2) , (0 , 0 , Ha_3)]
    mid_coordinates = [( 0 , 0 , Hb_1) , (0 , 0 , Hb_2) , (0 , 0 , Hb_3)]
    low_coordinates = [( 0 , 0 , 0) , (0 , 0 , 0) , (0 , 0 , 0)]
    minerva_position = [ 2 , 1 , 1]
    configuration = [[m , g , p ] , [g , m , p] , [g , m , p]]
    acronym = ["mgp" , "gmp" , "gmp"]
    shift_vector = [ 0 , 15 , 30 , 45 , 60 , 70]
    

    csv_file = dir_path / "muon_distribution_simulation_results.csv"
    fieldnames = ['configuration', 'Tx', 'Ty' , 'Tz', 'Mx', 'My' , 'Mz' , 'Bx' , 'By' , 'Bz' , 'doppie', 'triple', 'flag']

    # Write header once at the start
    with open(csv_file, mode='w', newline='') as f:
        f.write(','.join(fieldnames) + '\n')

    for i in range(len(top_coordinates)):
        for delta in shift_vector:
            mid_coord = list(mid_coordinates[i])
            mid_coord[0] = delta
            doppie, triple, flag = sim( top_coordinates[i] , tuple(mid_coord) , low_coordinates[i] , minerva_position[i] , *configuration[i])
            row = [
                ' '.join(acronym[i]),
                str(top_coordinates[i][0]), str(top_coordinates[i][1]), str(top_coordinates[i][2]),
                str(delta), str(mid_coordinates[i][1]), str(mid_coordinates[i][2]),
                str(low_coordinates[i][0]), str(low_coordinates[i][1]), str(low_coordinates[i][2]),
                str(doppie),
                str(triple),
                str(flag)
            ]
            # Append each row after simulation
            with open(csv_file, mode='a', newline='') as f:
                f.write(','.join(row) + '\n')
