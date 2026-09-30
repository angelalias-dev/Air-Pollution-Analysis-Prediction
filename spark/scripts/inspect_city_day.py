from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max

spark = (
    SparkSession.builder
    .appName("AirPollutionDataInspection")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/city_day.csv"

print()
print("==============================================")
print("       AIR POLLUTION DATA INSPECTION")
print("==============================================")

# LOAD DATA
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print()
print("========== SCHEMA ==========")
df.printSchema()

# TOTAL ROW COUNT
total_rows = df.count()

print()
print("========== TOTAL ROW COUNT ==========")
print(f"Total rows: {total_rows}")

# CITY COUNT
city_count = df.select("City").distinct().count()

print()
print("========== CITY COUNT ==========")
print(f"Number of cities: {city_count}")

# CITY-WISE RECORD COUNT
print()
print("========== CITY-WISE RECORD COUNT ==========")

(
    df.groupBy("City")
      .count()
      .orderBy(col("count").desc())
      .show(30, truncate=False)
)

# DATE RANGE
date_range = df.select(
    min("Date").alias("min_date"),
    max("Date").alias("max_date")
).collect()[0]

print()
print("========== DATE RANGE ==========")
print(f"Minimum date: {date_range['min_date']}")
print(f"Maximum date: {date_range['max_date']}")

# MISSING VALUES
print()
print("========== MISSING VALUES ==========")

for column_name in df.columns:
    missing_count = df.filter(
        col(f"`{column_name}`").isNull()
    ).count()

    print(f"{column_name}: {missing_count}")

# DUPLICATE ROWS
print()
print("========== DUPLICATE ROWS ==========")

duplicate_rows = total_rows - df.dropDuplicates().count()

print(f"Duplicate rows: {duplicate_rows}")

# AQI AVAILABILITY
aqi_available = df.filter(
    col("AQI").isNotNull()
).count()

aqi_missing = df.filter(
    col("AQI").isNull()
).count()

print()
print("========== AQI AVAILABILITY ==========")
print(f"AQI available: {aqi_available}")
print(f"AQI missing: {aqi_missing}")

# AQI BUCKET AVAILABILITY
aqi_bucket_available = df.filter(
    col("AQI_Bucket").isNotNull()
).count()

aqi_bucket_missing = df.filter(
    col("AQI_Bucket").isNull()
).count()

print()
print("========== AQI BUCKET AVAILABILITY ==========")
print(f"AQI Bucket available: {aqi_bucket_available}")
print(f"AQI Bucket missing: {aqi_bucket_missing}")

# SAMPLE DATA
print()
print("========== SAMPLE DATA ==========")

df.show(5, truncate=False)

# FINISH
print()
print("==============================================")
print("           INSPECTION COMPLETE")
print("==============================================")

spark.stop()