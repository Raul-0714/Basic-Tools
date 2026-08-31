import os, glob
import datetime

def get_data_dict(event_dir, event_time, event_mag=None):
    
    def Form_event_dir():

        def Decide_magnitude_group(magnitude):
            magnitude_bin = ['0.00-0.99', '1.00-1.99', '2.00-2.99', '3.00-3.99',
                     '4.00-4.99', '5.00-5.99', '6.00-6.99', '7.00-7.99', '8.00-8.99', '9.00-9.99']
            index_in_bin = int(magnitude // 1)
            magnitude_group = magnitude_bin[index_in_bin]
            return magnitude_group
        

        def Decide_date_code(time):
            code = f"{time.year:04d}{time.month:02d}{time.day:02d}"
            return code

        
        event_origin_time_str = event_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        date_code = Decide_date_code(event_time)
        
        dir = ''
        if event_mag:
            event_mag_group = Decide_magnitude_group(event_mag)
            dir = os.path.join(event_dir, date_code, event_mag_group, event_origin_time_str)
        else:
            dir = os.path.join(event_dir, date_code)

        return dir
        

    data_dict = {}
    data_directory = Form_event_dir()
    st_paths = sorted(glob.glob(os.path.join(data_directory, '*')))
    for st_path in st_paths:
        fname = os.path.basename(st_path)
        net_sta = '.'.join(fname.split('.')[0:2])
        if net_sta in data_dict:
            data_dict[net_sta].append(st_path)
        else:
            data_dict[net_sta] = [st_path]
    to_delete_stations = [net_sta for net_sta in data_dict if len(data_dict[net_sta]) != 3]
    for net_sta in to_delete_stations:
        data_dict.pop(net_sta)
    
    return data_dict


def Form_oneday_catalog_for(catalog, date):
    sub_catalog = {
        'event_id': [],
        'time': [],
        'latitude': [],
        'longitude': [],
        'depth': [],
        'magnitude': []
    }
    for i in range(len(catalog['time'])):
        event_time = catalog['time'][i]
        if event_time.date == date.date:
            sub_catalog['event_id'].append(catalog['event_id'][i])
            sub_catalog['time'].append(event_time)
            sub_catalog['latitude'].append(catalog['latitude'][i])
            sub_catalog['longitude'].append(catalog['longitude'][i])
            sub_catalog['depth'].append(catalog['depth'][i])
            sub_catalog['magnitude'].append(catalog['magnitude'][i])
    return sub_catalog


def Generate_date_list(start_date_string, end_date_string):
    start_time_date = datetime.datetime.strptime(start_date_string, "%Y%m%d")
    end_time_date = datetime.datetime.strptime(end_date_string, "%Y%m%d")
    date_list = []

    time_date = start_time_date

    while time_date < end_time_date:
        date_list.append(time_date.strftime("%Y%m%d"))
        time_date = time_date + datetime.timedelta(days=1)

    return date_list
