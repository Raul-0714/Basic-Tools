import os


def Output_station_list(stations, folder, output_file):
    with open(os.path.join(folder, output_file), 'w') as f:
        f.write('Index,Station Name,Latitude,Longitude,Elevation,Scaling_factor\n')
        for i in range(len(stations['index'])):
            f.write(f"{stations['index'][i]},{stations['station_name'][i]},{stations['latitude'][i]},"
                    f"{stations['longitude'][i]},{stations['elevation'][i]},{stations['scaling_factor'][i]}\n")