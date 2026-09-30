from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckMissingCleaned")
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
print("       MISSING VALUES IN CLEANED DATA")
print("==============================================")

for column_name in df.columns:
    missing_count = df.filter(
        col(f"`{column_name}`").isNull()
    ).count()

    print(f"{column_name}: {missing_count}")

print()
print("==============================================")
print("       MISSING VALUE CHECK COMPLETE")
print("==============================================")

spark.stop()