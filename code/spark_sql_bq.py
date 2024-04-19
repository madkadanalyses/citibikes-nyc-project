import argparse
import pyspark
from pyspark.sql import SparkSession

parser = argparse.ArgumentParser()

parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--mode', required=True)
parser.add_argument('--temp_bucket', required=True)
args = parser.parse_args()

input = args.input
output = args.output
mode = args.mode
temp_bucket = args.temp_bucket

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', temp_bucket)

df = spark.read.parquet(input)

df.registerTempTable('citibike_tripsdata')

df_result = spark.sql("""
SELECT *
FROM
    citibike_tripsdata;        
""")

df_result.write.format('bigquery') \
    .option('table', output) \
    .option("partitionField", 'start_time') \
    .option("partitionType", 'DAY') \
    .option("clusteredFields", 'user_type') \
    .mode(mode) \
    .save()