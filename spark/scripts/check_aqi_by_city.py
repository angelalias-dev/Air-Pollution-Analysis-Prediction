from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

spark = (
    SparkSession.builder
    .appName("CheckAQIByCity")
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

print()
print("==============================================")
print("       AQI AVAILABILITY BY CITY")
print("==============================================")

(
    df.groupBy("City")
      .agg(
          count("AQI").alias("AQI_available"),
          count("*").alias("Total_records")
      )
      .withColumn(
          "AQI_missing",
          col("Total_records") - col("AQI_available")
      )
      .orderBy("City")
      .show(30, truncate=False)
)

print()
print("==============================================")
print("       AQI CITY CHECK COMPLETE")
print("==============================================")

spark.stop()