from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, count

spark = (
    SparkSession.builder
    .appName("CityAQIAnalysis")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/ml_predictions"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print()
print("==============================================")
print("       CITY-WISE AQI ANALYSIS")
print("==============================================")

city_analysis = (
    df.groupBy("City")
    .agg(
        count("*").alias("Records"),
        avg("AQI").alias("Average_AQI"),
        avg("prediction").alias("Average_Predicted_AQI"),
        max("AQI").alias("Maximum_AQI"),
        min("AQI").alias("Minimum_AQI")
    )
    .orderBy("Average_AQI", ascending=False)
)

city_analysis.show(30, truncate=False)

print()
print("==============================================")
print("       CITY ANALYSIS COMPLETE")
print("==============================================")

spark.stop()