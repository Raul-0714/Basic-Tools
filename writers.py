import os


def Output_station_list(stations, folder, output_file):
    with open(os.path.join(folder, output_file), 'w') as f:
        f.write('Index,Station Name,Latitude,Longitude,Elevation,Scaling_factor\n')
        for i in range(len(stations['index'])):
            f.write(f"{stations['index'][i]},{stations['station_name'][i]},{stations['latitude'][i]},"
                    f"{stations['longitude'][i]},{stations['elevation'][i]},{stations['scaling_factor'][i]}\n")
            

def Output_phases(phases, folder, output_file, phase_file_type='TomoATT-Input', phase_type='P'):

    def Extract_time_info(event_time):
    # Extract time information from the event time
    # Event time is an UTCDateTime object
        year = event_time.year
        month = event_time.month
        day = event_time.day
        hour = event_time.hour
        minute = event_time.minute
        second = event_time.second
        microsecond = event_time.microsecond
        total_second = second + microsecond / 1e6
        return year, month, day, hour, minute, total_second


    if phase_file_type == 'TomoATT-Input':
        for i in range(len(phases['event_time'])):
            id_src = i + 1
            event_time = phases['event_time'][i]
            id_event = phases['event_id'][i]
            year, month, day, hour, minute, total_second = Extract_time_info(event_time)
            lat, lon, dep = phases['event_location'][i]
            mag = phases['event_magnitude'][i]
            num_recs = len(phases['phase_stations'][i])
            with open(os.path.join(folder, output_file), 'a') as f:
                f.write(f"{id_src} {year} {month} {day} {hour} {minute} {total_second:.4f} {lat:.4f} {lon:.4f} {dep:.2f} {mag:.2f} {num_recs} {id_event}\n")
                for j in range(num_recs):
                    station_name = phases['phase_stations'][i][j]
                    P_travel_time = phases['P_travel_times'][i][j]
                    if P_travel_time is None:
                        print(f"Warning: P arrival time is None for event {id_event} at station {station_name}. Skipping this record.")

                        continue
                    sta_lat, sta_lon, sta_ele = phases['station_locations'][i][j]
                    id_rec = j + 1
                    f.write(f"{id_src} {id_rec} {station_name} {sta_lat:.4f} {sta_lon:.4f} {sta_ele:.4f} {phase_type} {P_travel_time:.3f}\n")





    