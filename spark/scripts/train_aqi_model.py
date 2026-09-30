from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

spark = (
    SparkSession.builder
    .appName("AQIPredictionModel")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://namenode:8020/airpollution/prediction/imputed_city_day"
model_path = "hdfs://namenode:8020/airpollution/ml_model/aqi_random_forest"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print()
print("==============================================")
print("       SPARK ML - AQI PREDICTION")
print("==============================================")

print(f"Total rows: {df.count()}")

# Rename PM2.5 because the dot causes problems in Spark ML
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

data = assembler.transform(df).select(
    "features",
    "AQI"
)

train_data, test_data = data.randomSplit(
    [0.8, 0.2],
    seed=42
)

print(f"Training rows: {train_data.count()}")
print(f"Testing rows: {test_data.count()}")

rf = RandomForestRegressor(
    featuresCol="features",
    labelCol="AQI",
    numTrees=100,
    seed=42
)

model = rf.fit(train_data)

predictions = model.transform(test_data)

print()
print("========== SAMPLE PREDICTIONS ==========")

predictions.select(
    "AQI",
    "prediction"
).show(10, truncate=False)

rmse_evaluator = RegressionEvaluator(
    labelCol="AQI",
    predictionCol="prediction",
    metricName="rmse"
)

mae_evaluator = RegressionEvaluator(
    labelCol="AQI",
    predictionCol="prediction",
    metricName="mae"
)

r2_evaluator = RegressionEvaluator(
    labelCol="AQI",
    predictionCol="prediction",
    metricName="r2"
)

rmse = rmse_evaluator.evaluate(predictions)
mae = mae_evaluator.evaluate(predictions)
r2 = r2_evaluator.evaluate(predictions)
print()
print("========== FEATURE IMPORTANCE ==========")

feature_importance = model.featureImportances

for i, feature_name in enumerate(feature_columns):
    print(f"{feature_name}: {feature_importance[i]}")
print()
print("========== MODEL EVALUATION ==========")
print(f"RMSE: {rmse}")
print(f"MAE: {mae}")
print(f"R2: {r2}")

model.write().overwrite().save(model_path)

print()
print("Model saved to:")
print(model_path)

print()
print("==============================================")
print("       SPARK ML TRAINING COMPLETE")
print("==============================================")

spark.stop()