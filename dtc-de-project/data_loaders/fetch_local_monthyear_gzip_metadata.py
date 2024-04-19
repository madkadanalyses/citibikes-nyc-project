from mage_ai.io.file import FileIO
import os
import pandas as pd
from typing import List
from typing import Dict
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    input_files_info = []
    years_list = list(range(2020, 2024))
    
    for year in years_list:
        for i in range(12):
            month = str(i+1).zfill(2)
            
            file_name = f"{year}{month}-citibike-tripdata.csv.gz"
            directory = f"/home/src/data/"
            file_path = f"{directory}/{file_name}"

            input_files_info.append(dict(file_name=f'{file_name}', file_path=f'{file_path}', year=f'{year}', month=f'{month}',))


    return [input_files_info]
