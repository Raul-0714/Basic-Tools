import numpy as np


def Calculate_travel_distance(station_location, event_location, consider_depth=False):
    R = 6371.0

    station_lat = station_location[0]
    station_lon = station_location[1]
    event_lat = event_location[0]
    event_lon = event_location[1]

    lat1, lon1, lat2, lon2 = map(np.radians, [station_lat, station_lon, event_lat, event_lon])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    distance = R * c
    if consider_depth:
        depth = event_location[2]
        distance = np.sqrt(distance**2 + depth**2)
    
    return distance
