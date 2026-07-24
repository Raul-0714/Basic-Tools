import numpy as np
import obspy

RAD2DEG = 180/np.pi
DEG2RAD = np.pi/180
R_earth = 6371.0

def Calculate_travel_distance(station_location, event_location, consider_depth=False):

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

    distance = R_earth * c
    if consider_depth:
        depth = event_location[2] + station_location[2] / 1000.0
        distance = np.sqrt(distance**2 + depth**2)
    
    return distance


def Calculate_interstation_azimuth(event_loc, sta1_loc, sta2_loc):
    event_lat = event_loc[0]
    event_lon = event_loc[1]
    sta1_lat = sta1_loc[0]
    sta1_lon = sta1_loc[1]
    sta2_lat = sta2_loc[0]
    sta2_lon = sta2_loc[1]
    _, A1, _ = obspy.geodetics.base.gps2dist_azimuth(event_lat, event_lon, sta1_lat, sta1_lon)
    _, A2, _ = obspy.geodetics.base.gps2dist_azimuth(event_lat, event_lon, sta2_lat, sta2_lon)
    interstation_azimuth = 0
    if (360 - abs(A1-A2)) <= abs(A1-A2):
        interstation_azimuth = (360 - abs(A1-A2))
    else:
        interstation_azimuth = abs(A1-A2)
    return interstation_azimuth


def rtp2xyz(r, theta, phi):
    x = r * np.cos(theta*DEG2RAD) * np.cos(phi*DEG2RAD)
    y = r * np.cos(theta*DEG2RAD) * np.sin(phi*DEG2RAD)
    z = r * np.sin(theta*DEG2RAD)
    return (x,y,z)


def xyz2rtp(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(z, np.sqrt(x**2 + y**2))
    phi = np.arctan2(y, x)

    theta = theta * RAD2DEG
    phi = phi * RAD2DEG

    return r, theta, phi


def anti_clockwise_rotate_x(x, y, z, theta):
    new_x = x
    new_y = y * np.cos(theta*DEG2RAD) + z * -np.sin(theta*DEG2RAD)
    new_z = y * np.sin(theta*DEG2RAD) + z * np.cos(theta*DEG2RAD)
    return new_x, new_y, new_z


def anti_clockwise_rotate_y(x, y, z, theta):
    new_x = x * np.cos(theta*DEG2RAD) + z * np.sin(theta*DEG2RAD)
    new_y = y
    new_z = x * -np.sin(theta*DEG2RAD) + z * np.cos(theta*DEG2RAD)
    return new_x, new_y, new_z


def anti_clockwise_rotate_z(x, y, z, theta):
    new_x = x * np.cos(theta*DEG2RAD) + y * -np.sin(theta*DEG2RAD)
    new_y = x * np.sin(theta*DEG2RAD) + y * np.cos(theta*DEG2RAD)
    new_z = z
    return new_x, new_y, new_z


def rtp_rotation(t,p,theta0,phi0,psi):
    # step 1: r,t,p -> x,y,z
    (x,y,z) = rtp2xyz(1.0,t,p)

    # step 2: anti-clockwise rotation with -phi0 along z-axis:   r0,t0,p0 -> r0,t0,0
    (x,y,z) = anti_clockwise_rotate_z(x,y,z,-phi0)

    # step 3: anti-clockwise rotation with theta0 along y-axis:  r0,t0,0 -> r0,0,0
    (x,y,z) = anti_clockwise_rotate_y(x,y,z,theta0)

    # # step 4: anti-clockwise rotation with psi along x-axis
    (x,y,z) = anti_clockwise_rotate_x(x,y,z,psi)

    # step 5: x,y,z -> r,t,p
    _, new_t, new_p = xyz2rtp(x,y,z)
    
    return new_t, new_p


def rtp_rotation_reverse(new_t,new_p,theta0,phi0,psi):
    # step 1: r,t,p -> x,y,z
    (x,y,z) = rtp2xyz(1.0,new_t,new_p)

    # step 2: anti-clockwise rotation with -psi along x-axis
    (x,y,z) = anti_clockwise_rotate_x(x,y,z,-psi)

    # step 3: anti-clockwise rotation with -theta0 along y-axis:  r0,0,0 -> r0,t0,0 
    (x,y,z) = anti_clockwise_rotate_y(x,y,z,-theta0)

    # step 4: anti-clockwise rotation with phi0 along z-axis:   r0,t0,0 -> r0,t0,p0 
    (x,y,z) = anti_clockwise_rotate_z(x,y,z,phi0)

    # step 5: x,y,z -> r,t,p
    _, t, p = xyz2rtp(x,y,z)
    
    return t, p


def Get_velocity_value_at(lon, lat, depth_idx, vel_model, vel_lons, vel_lats):

    def Linear_interpolation(x0, x1, v0, v1, x):
        if x1 == x0:
            return v0
        return v0 + (v1 - v0) * (x - x0) / (x1 - x0)


    def Is_in_the_region():
        is_in_the_region = True
        if lon > vel_lons[-1] or lon < vel_lons[0]:
            is_in_the_region = False
        if lat > vel_lats[-1] or lat < vel_lats[0]:
            is_in_the_region = False
        return is_in_the_region

    vel_at_depth = vel_model[depth_idx, :, :]

    # Find surrounding grid points for bilinear interpolation
    if Is_in_the_region():
        lon_idx1 = np.searchsorted(vel_lons, lon) - 1
        lon_idx2 = lon_idx1 + 1
        lon1 = vel_lons[lon_idx1]
        lon2 = vel_lons[lon_idx2]
        lat_idx1 = np.searchsorted(vel_lats, lat) - 1
        lat_idx2 = lat_idx1 + 1
        lat1 = vel_lats[lat_idx1]
        lat2 = vel_lats[lat_idx2]

        Q11 = vel_at_depth[lat_idx1, lon_idx1]
        Q21 = vel_at_depth[lat_idx1, lon_idx2]
        Q12 = vel_at_depth[lat_idx2, lon_idx1]
        Q22 = vel_at_depth[lat_idx2, lon_idx2]
        R1 = Linear_interpolation(lon1, lon2, Q11, Q21, lon)
        R2 = Linear_interpolation(lon1, lon2, Q12, Q22, lon)
        P = Linear_interpolation(lat1, lat2, R1, R2, lat)
    else:
        P = 0

    return P