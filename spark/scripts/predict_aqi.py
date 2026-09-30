from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressionModel

spark = (
    SparkSession.builder
    .appName("AQIPrediction")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/prediction/imputed_city_day"
model_path = "hdfs://namenode:8020/airpollution/ml_model/aqi_random_forest"
output_path = "hdfs://namenode:8020/airpollution/ml_predictions"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

# Rename PM2.5 for Spark ML
df = df.withColumnRenamed("PM2.5", "PM25")

feature_columns = [
    "PM25",
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

assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features"
)

data = assembler.transform(df)

# Load trained Random Forest model
model = RandomForestRegressionModel.load(model_path)

# Generate predictions
predictions = model.transform(data)

result = predictions.select(
    "City",
    "Date",
    "AQI",
    "AQI_Bucket",
    "prediction"
)

print()
print("==============================================")
print("       AQI PREDICTIONS")
print("==============================================")

print(f"Total predictions: {result.count()}")

print()
print("========== SAMPLE PREDICTIONS ==========")

result.show(20, truncate=False)

# Save predictions
result.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print()
print("Predictions saved to:")
print(output_path)

print()
print("==============================================")
print("       PREDICTION COMPLETE")
print("==============================================")

spark.stop()