from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CreatePredictionData")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/cleaned/city_day"
output_path = "hdfs://namenode:8020/airpollution/prediction/city_day"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

prediction_df = df.filter(
    col("AQI").isNotNull() &
    col("AQI_Bucket").isNotNull()
)

print()
print("==============================================")
print("       CREATING PREDICTION DATASET")
print("==============================================")

print(f"Original cleaned rows: {df.count()}")
print(f"Prediction rows: {prediction_df.count()}")

prediction_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print()
print("Prediction dataset saved to:")
print(output_path)

print()
print("==============================================")
print("       PREDICTION DATASET COMPLETE")
print("==============================================")

spark.stop()