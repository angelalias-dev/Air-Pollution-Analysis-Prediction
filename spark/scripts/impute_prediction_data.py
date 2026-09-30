from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when

spark = (
    SparkSession.builder
    .appName("ImputePredictionData")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/prediction/city_day"
output_path = "hdfs://namenode:8020/airpollution/prediction/imputed_city_day"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

median_values = {
    "PM2.5": 48.23,
    "PM10": 95.79,
    "NO": 9.8,
    "NO2": 21.82,
    "NOx": 23.35,
    "NH3": 16.1,
    "CO": 0.92,
    "SO2": 9.15,
    "O3": 30.91,
    "Benzene": 1.27,
    "Toluene": 3.45,
    "Xylene": 1.37
}

print()
print("==============================================")
print("       IMPUTING MISSING VALUES")
print("==============================================")

for column_name, median_value in median_values.items():
    df = df.withColumn(
        column_name,
        when(
            col(f"`{column_name}`").isNull(),
            lit(median_value)
        ).otherwise(
            col(f"`{column_name}`")
        )
    )

print(f"Rows after imputation: {df.count()}")

df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print()
print("Imputed dataset saved to:")
print(output_path)

print()
print("==============================================")
print("       IMPUTATION COMPLETE")
print("==============================================")

spark.stop()