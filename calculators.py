import numpy as np

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

