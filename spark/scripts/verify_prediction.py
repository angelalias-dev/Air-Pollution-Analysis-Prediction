from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("VerifyPredictionData")
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

print()
print("==============================================")
print("       PREDICTION DATA VERIFICATION")
print("==============================================")

print(f"Prediction row count: {df.count()}")

print()
print("Columns:")
print(df.columns)

print()
print("Sample rows:")
df.show(5, truncate=False)

print()
print("==============================================")
print("       PREDICTION VERIFICATION COMPLETE")
print("==============================================")

spark.stop()