# Citibike NYC Data Plumbing

## Description
This project utilises public data from the [Citibike bicycle sharing system](https://citibikenyc.com/) in New York City, USA.  It is currently privately owned by Lyft; the company makes aggregated monthly rides data available [here](https://s3.amazonaws.com/tripdata/index.html)


## Problem Description
New York City is one of the most densely populated areas in the world.  This density can make moving around in the city, whether as a resident or as a tourist, a significant issue.  One of the methods the City's Department of Transportation (DOT) has sought to use, in a sustainable, environmentally friendly and accessible manner, is by introducing the bike share programme in 2013.
This project aims to build a complete data pipeline that fetches data from the publicly available data store, apply transformation steps to clean and apply a structure that will allow for data visualization and analyses.

## Technology Stack

* Terraform: Infrastructure as Code tool
* GCP Cloud Storage: Data Lake
* Mage.ai: Data Orchestration tool
* GCP Dataproc Pyspark: Data transformation and modeling
* GCP BigQuery: Data Warehouse
* GCP Looker studio: Business Intelligence tool for Visualizations

## Pipeline Architecture

![Alt text](https://github.com/madkadanalyses/DataTalksClub_DataEngg_January_2024_Homework/blob/main/Project/%E2%80%8EData_Arch_KN.%E2%80%8E001.png?raw=true "data architecture")


## Data Description

| Column Name  | Description |
| ------------- |:-------------:|
| start_time    | time of start of bicycle ride     |
| end_time      | time of end of bicycle ride     |
| start_station_name | name of starting bicycle station     |
| start_station_id | id of starting bicycle station     |
| end_station_name | name of ending bicycle station     |
| end_station_id | id of ending bicycle station |
| start_station_latitude | latitude of starting bicycle station |
| start_station_longitude | longtitude of starting bicycle station |
| end_station_latitude | latitude of ending bicycle station|
| end_station_longitude | longtitude of ending bicycle station |
| user_type | whether user is member or casual user |
| calculated_duration | calculation of time in seconds of the bicycle ride |

Data has been cleaned and transformed to the above essential columns, given the [split format](https://citibikenyc.com/system-data) of historical data.

## Replication

* Fork this repository to your local
* Start a new project on GCP, create a service account with Storage Admin, Storage Object Admin, BigQuery Admin, Dataproc Admin as privileges.
* Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
* Download keys and assign it to the _GOOGLE_APPLICATION_CREDENTIALS_ env-var
* Set up infrastructure on Google Cloud using [Terraform](https://youtu.be/Y2ux7gq3Z0o).  Make changes to the [variable names](https://youtu.be/PBi0hHjLftk) as required.
* Set up Mage.ai orchestrator by downloading docker image and setting up as mentioned in their [quickstart guide](https://docs.mage.ai/getting-started/setup)
* Run the shell script in the pipeline named *shell_script_for_downloading_yearly_data* for downloading yearly data into local.  This step is required given the volume and structure of the data.
* Run the python scripts in the pipeline named *convert_yearly_data_to_month_year_compressed_files* to convert the yearly data into month-year format.  This step also cleans and transforms the data into the format required for visualization.
* Run the *iterate_local_input_gzip_to_gcs_parquet* containing dynamic blocks to export data to a GCS bucket as partitioned parqet files.  In the pipeline metadata.yaml change the concurrency config to
```
concurrency_config: {block_run_limit: 1}
```
to iterate over the data sequentially.  It is a less memory constraining method, and causes fewer errors.
* Upload the *spark_sql_bq.py* script to a different bucket from the one with the parquet files.  Create a new BQ table for the data, and a dataproc cluster for the transfer from bucket to data warehouse. Below is an example of the command to trigger dataproc
```
gcloud dataproc jobs submit pyspark \
    --cluster=your-dataproc-cluster-name \
    --region=region-for-dataproc-cluster \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar \ #actual_jar_name_for_latest_connector 
    gs://location_of_pyspark_script.py \
    -- \
        --input=gs://location_of_bucket_with_partitioned_parquet_files \
        --output=bq_dataset_name.table_name \
        --mode=errors \
        --temp_bucket=temp_bucket_name
```
* Once dataproc job is successful, navigate to bigquery table created and check data quality with a few queries. Pyspark script would have created a date partitioned user_type clustered DWH table.
* Navigate to Looker Studio once convinced of data quality in the previous step, and create a few visualizations to check for temporal patterns in bicycle ride activity, aggregate rides, split by user types and so on.  Below is a simple dashboard created for the project:
![Alt text](https://github.com/madkadanalyses/DataTalksClub_DataEngg_January_2024_Homework/blob/main/Project/Citibikes-NYC_Bicycle_Rides_Project.png?raw=true "project data dashboard")
It appears that there is a seasonality to bicycle usage in New York, and a majority of rides are by members, who are likely residents of the city.

To Dos:
* Some parts of the current pipeline needs shell scripts, which currently cannot be triggered in sequence in the data orchestrator. Once the functionality is available the pipeline updated for full automation.
* Data for the current year is uploaded as monthly zipped files, which is different from the historical data, uploaded as yearly zipped files. A supplementary pipeline will be developed to backfill the current year's monthly data and include a date based trigger for incremental updates of new data uploads.
* To add tests
* To integrate CI/CD processes