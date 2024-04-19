from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import pandas as pd
import os
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/dtc-de-project-32a2d69c356c.json"

bucket_name = 'dtc-de-project-madkad'
project_id = 'dtc-de-project-madkad'

table_name = "citibike-tripdata"

root_path = f"{bucket_name}/{table_name}"

schema = pa.schema([
    pa.field('start_time', pa.timestamp('ms')),
    pa.field('end_time', pa.timestamp('ms')),
    pa.field('start_station_id', pa.float64()),
    pa.field('start_station_name', pa.string()),
    pa.field('start_station_latitude', pa.float64()),
    pa.field('start_station_longitude', pa.float64()),
    pa.field('end_station_id', pa.float64()),
    pa.field('end_station_name', pa.string()),
    pa.field('end_station_latitude', pa.float64()),
    pa.field('end_station_longitude', pa.float64()),
    pa.field('user_type', pa.string()),
    pa.field('calculated_duration', pa.float64())])

@data_exporter
def export_data_to_google_cloud_storage(df: pd.DataFrame, **kwargs) -> None:
    df["start_date"] = df["start_time"].dt.date

    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem() 

    pq.write_to_dataset(
        table,
        root_path = root_path,
        partition_cols = ["start_date"],
        filesystem = gcs,
        coerce_timestamps='ms'
    )