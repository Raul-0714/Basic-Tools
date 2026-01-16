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


def Convert_polar_to_lat_lon(origin, distance_km, azimuth_rad):
    R = 6371.0

    lat1 = np.radians(origin[0])
    lon1 = np.radians(origin[1])

    angular_distance = distance_km / R
    azimuth = azimuth_rad
    lat2 = np.arcsin(np.sin(lat1) * np.cos(angular_distance) +
                     np.cos(lat1) * np.sin(angular_distance) * np.cos(azimuth))
    lon2 = lon1 + np.arctan2(np.sin(azimuth) * np.sin(angular_distance) * np.cos(lat1),
                             np.cos(angular_distance) - np.sin(lat1) * np.sin(lat2))
    lat2 = np.degrees(lat2)
    lon2 = np.degrees(lon2)
    return (lat2, lon2)
