from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("VerifyCleanedCityDay")
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
print("       CLEANED DATA VERIFICATION")
print("==============================================")

print(f"Cleaned row count: {df.count()}")

print()
print("Columns:")
print(df.columns)

print()
print("==============================================")
print("       VERIFICATION COMPLETE")
print("==============================================")

spark.stop()