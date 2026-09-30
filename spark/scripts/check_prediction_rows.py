from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckPredictionRows")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

path = "hdfs://namenode:8020/airpollution/cleaned/city_day"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(path)
)

total_rows = df.count()

aqi_available = df.filter(
    col("AQI").isNotNull()
).count()

bucket_available = df.filter(
    col("AQI_Bucket").isNotNull()
).count()

both_available = df.filter(
    col("AQI").isNotNull() &
    col("AQI_Bucket").isNotNull()
).count()

print()
print("==============================================")
print("       PREDICTION ROW CHECK")
print("==============================================")

print(f"Total rows: {total_rows}")
print(f"AQI available: {aqi_available}")
print(f"AQI_Bucket available: {bucket_available}")
print(f"Both AQI and AQI_Bucket available: {both_available}")

print()
print("==============================================")
print("       PREDICTION ROW CHECK COMPLETE")
print("==============================================")

spark.stop()