from mage_ai.io.file import FileIO
import os
from time import time
import gzip
import pandas as pd
import io
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

datatypes = {'start_station_id': float, 
       'start_station_name': str,
       'start_station_latitude': float,
       'start_station_longitude': float,
       'end_station_id': float,
       'end_station_name': str,
       'end_station_latitude': float,
       'end_station_longitude': float, 
       'user_type': str, 
       'calculated_duration': float
       }
parse_dates = ['start_time', 'end_time']

@data_loader
def load_data(df, *args, **kwargs):
    metadata = []
    file_path = df['file_path']
    file_name_csv = df['file_name']
    year = df['year']
    month = df['month']
    metadata.append(dict(object_key=f'{file_path}', year=f'{year}', month=f'{month}'))
            
    df = pd.read_csv(file_path, sep=',', compression='gzip', dtype=datatypes, parse_dates=parse_dates)

    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'