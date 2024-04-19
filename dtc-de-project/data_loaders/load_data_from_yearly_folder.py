from mage_ai.io.file import FileIO
import os
from time import time
from collections import defaultdict
import pandas as pd
import datetime
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def list_csv_files(dir):
    list_of_filenames = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]
        if (len(files) > 0):                                                                                          
            for file in files:
                if (".csv" in file):
                    list_of_filenames.append(os.path.join(subdir, file))
                    
    return list_of_filenames

old_format_columnnames = {"starttime": "start_time", "stoptime": "end_time", "start_station_id": "start_station_id", "start_station_name": "start_station_name",
       "start_station_latitude": "start_station_latitude", "start_station_longitude": "start_station_longitude", "end_station_id": "end_station_id",
       "end_station_name": "end_station_name", "end_station_latitude": "end_station_latitude", "end_station_longitude": "end_station_longitude",
        "usertype": "user_type", "calculated_duration": "calculated_duration"}

new_format_columnnames = {"started_at": "start_time", "ended_at": "end_time",
       "start_station_name": "start_station_name", "start_station_id": "start_station_id", "end_station_name": "end_station_name",
       "end_station_id": "end_station_id", "start_lat": "start_station_latitude", "start_lng": "start_station_longitude", 
        "end_lat": "end_station_latitude", "end_lng": "end_station_longitude",
       "member_casual": "user_type", "calculated_duration": "calculated_duration"}


@data_loader
def load_data_from_file(*args, **kwargs):
    filepath = '/home/src/data'

    List = list_csv_files(filepath)
    Dict = defaultdict(list)

    for elem in List:
        key = elem[-30:-24]
        Dict[key].append(elem)

    for key, value in Dict.items():
        print(key)
        if ("a/" not in key) and ("-" not in key):
            format_change_threshold = datetime.datetime(int(key[:4]),int(key[4:]),int("1")) >= datetime.datetime(2021,1,31)
            print(format_change_threshold)
            if format_change_threshold:
                bicycle_datatypes = {
                    'ride_id': str,
                    'rideable_type': str,
                    'start_station_name': str,
                    'start_station_id': str,
                    'end_station_name': str,
                    'end_station_id': str,
                    'start_lat': float,
                    'start_lng': float,
                    'end_lat': float,
                    'end_lng': float,
                    'member_casual': str
                    }
                parse_dates = ['started_at','ended_at']
            else:
                bicycle_datatypes = {
                'tripduration': pd.Int64Dtype(),
                'start station id': float,
                'start station name': str,
                'start station latitude': float,
                'start station longitude': float,
                'end station id': float,
                'end station name': str,
                'end station latitude': float,
                'end station longitude': float,
                'bikeid': pd.Int64Dtype(),
                'usertype': str,
                'birth year': pd.Int64Dtype(),
                'gender': str
                    }
                parse_dates = ['starttime','stoptime']
            print(f"concatenating datasets for {key} year-month")
            time_start = time()
            df = pd.concat([pd.read_csv(f, dtype=bicycle_datatypes, parse_dates=parse_dates) for f in value],ignore_index=True)
            if "starttime" in df.columns:
                df.columns = [x.replace(' ', '_') for x in df.columns]
                df = df.drop_duplicates(subset=['bikeid', 'starttime', 'stoptime'], keep='first')
                df = df[~df["start_station_latitude"].isna()]
                df["calculated_duration"] = (pd.to_datetime(df["stoptime"]) - pd.to_datetime(df["starttime"])).dt.total_seconds()
                df.replace({"usertype": {"Subscriber": "member", "Customer": "casual"}}, inplace=True)
                df.drop(columns=["birth_year", "gender", "tripduration", "bikeid"], inplace=True)
                df.rename(columns=old_format_columnnames, inplace=True)
            elif "started_at" in df.columns:
                df = df.drop_duplicates(subset=['ride_id'])
                df = df[~df["start_lat"].isna()]
                df.drop(columns=["ride_id", "rideable_type"], inplace=True)
                df["calculated_duration"] = (pd.to_datetime(df["ended_at"]) - pd.to_datetime(df["started_at"])).dt.total_seconds()
                df.rename(columns=new_format_columnnames, inplace=True)
            else:
                pass
            
            df = df[pd.to_numeric(df['start_station_id'], errors='coerce').notna()]
            df = df[pd.to_numeric(df['end_station_id'], errors='coerce').notna()]
            df.to_csv(f"/home/src/data/{key}-citibike-tripdata.csv.gz", header=True, index=False, compression="gzip")
            time_end = time()
            print(f"wrote out gzip file for {key} folder")
            print('took %.3f seconds' % (time_end - time_start))
