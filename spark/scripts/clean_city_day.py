from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("AirPollutionDataCleaning")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/city_day.csv"
output_path = "hdfs://namenode:8020/airpollution/cleaned/city_day"

print()
print("==============================================")
print("        AIR POLLUTION DATA CLEANING")
print("==============================================")

# LOAD RAW DATA
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print()
print("Original row count:", df.count())

# REMOVE EXACT DUPLICATE ROWS
df_clean = df.dropDuplicates()

print("Row count after removing duplicates:", df_clean.count())

# SAVE CLEANED DATA
(
    df_clean.write
    .mode("overwrite")
    .option("header", "true")
    .csv(output_path)
)

print()
print("Cleaned dataset saved to:")
print(output_path)

print()
print("==============================================")
print("          CLEANING COMPLETE")
print("==============================================")

spark.stop()