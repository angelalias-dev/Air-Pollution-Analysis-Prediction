from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CalculateMedians")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

path = "hdfs://namenode:8020/airpollution/prediction/city_day"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(path)
)

numeric_columns = [
    "PM2.5",
    "PM10",
    "NO",
    "NO2",
    "NOx",
    "NH3",
    "CO",
    "SO2",
    "O3",
    "Benzene",
    "Toluene",
    "Xylene"
]

print()
print("==============================================")
print("       MEDIAN VALUES")
print("==============================================")

for column_name in numeric_columns:
    median_value = df.select(
    col(f"`{column_name}`")
).approxQuantile(
    f"`{column_name}`",
    [0.5],
    0.01
)[0]
    print(f"{column_name}: {median_value}")

print()
print("==============================================")
print("       MEDIAN CALCULATION COMPLETE")
print("==============================================")

spark.stop()