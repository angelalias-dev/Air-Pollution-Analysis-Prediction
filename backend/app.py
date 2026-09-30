from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max as spark_max, min as spark_min, count, desc
import math


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AERIS Air Intelligence API",
    description="Backend API for the AERIS environmental intelligence dashboard",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# PATHS
# ============================================================

HDFS_PREDICTIONS = "hdfs://namenode:8020/airpollution/ml_predictions"

CITY_DETAILS_PATH = "file:///data/citydetails.csv"
AQI_PATH = "file:///data/city_day.csv"
WEATHER_PATH = "file:///data/weather_india.csv"
VEHICLE_PATH = "file:///data/vehicle_dataset.csv"

# ============================================================
# GLOBAL DATA
# ============================================================

spark = None

prediction_df = None
aqi_df = None
weather_df = None
vehicle_df = None
city_details_df = None


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():

    global spark
    global prediction_df
    global aqi_df
    global weather_df
    global vehicle_df
    global city_details_df

    print("Starting Spark...")

    spark = (
        SparkSession.builder
        .appName("AERIS-Backend")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")


    # --------------------------------------------------------
    # ML PREDICTIONS
    # --------------------------------------------------------

    print("Loading prediction data...")

    prediction_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(HDFS_PREDICTIONS)
    )

    prediction_df.cache()

    prediction_rows = prediction_df.count()

    print(f"Prediction rows: {prediction_rows}")


    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    print("Loading weather data...")

    weather_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(WEATHER_PATH)
    )

    weather_df.cache()

    weather_rows = weather_df.count()

    print(f"Weather rows: {weather_rows}")


    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    print("Loading vehicle data...")

    vehicle_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(VEHICLE_PATH)
    )

    vehicle_df.cache()

    vehicle_rows = vehicle_df.count()

    print(f"Vehicle rows: {vehicle_rows}")


    # --------------------------------------------------------
    # CITY DETAILS
    # --------------------------------------------------------

    print("Loading city details...")

    city_details_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(CITY_DETAILS_PATH)
    )

    city_details_df.cache()

    city_rows = city_details_df.count()

    print(f"City details rows: {city_rows}")


    # --------------------------------------------------------
    # ORIGINAL AQI DATASET
    # --------------------------------------------------------

    print("Loading AQI historical data...")

    aqi_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(AQI_PATH)
    )

    aqi_df.cache()

    aqi_rows = aqi_df.count()

    print(f"AQI rows: {aqi_rows}")


    print("All datasets loaded successfully.")


# ============================================================
# BASIC ROUTES
# ============================================================

@app.get("/")
def home():

    return {
        "project": "AERIS",
        "message": "Air Intelligence API is running",
        "status": "online",
        "version": "2.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "spark": spark is not None,
        "predictions_loaded": prediction_df is not None,
        "weather_loaded": weather_df is not None,
        "vehicle_loaded": vehicle_df is not None,
        "city_details_loaded": city_details_df is not None,
        "aqi_loaded": aqi_df is not None
    }


# ============================================================
# PROJECT INFORMATION
# ============================================================

@app.get("/project-info")
def project_info():

    prediction_count = prediction_df.count()

    city_count = (
        prediction_df
        .select("City")
        .distinct()
        .count()
    )

    return {
        "project": "AERIS",
        "full_name": "Atmospheric Environmental Research & Intelligence System",
        "cities": city_count,
        "prediction_records": prediction_count,
        "historical_aqi_records": aqi_df.count(),
        "weather_records": weather_df.count(),
        "vehicle_city_records": vehicle_df.count(),
        "model": "Random Forest Regression",
        "r2": 0.8308945176,
        "rmse": 60.61928705,
        "mae": 32.04053982
    }


# ============================================================
# PREDICTION SUMMARY
# ============================================================

@app.get("/prediction-summary")
def prediction_summary():

    return {
        "total_predictions": prediction_df.count(),
        "columns": prediction_df.columns
    }


# ============================================================
# OVERVIEW
# ============================================================

@app.get("/overview")
def overview():

    stats = (
        prediction_df
        .select(
            count("*").alias("records"),
            avg("AQI").alias("average_aqi"),
            avg("prediction").alias("average_predicted_aqi"),
            spark_max("AQI").alias("maximum_aqi"),
            spark_min("AQI").alias("minimum_aqi")
        )
        .collect()[0]
    )

    return {
        "records": int(stats["records"]),
        "average_aqi": round(float(stats["average_aqi"]), 2),
        "average_predicted_aqi": round(
            float(stats["average_predicted_aqi"]), 2
        ),
        "maximum_aqi": float(stats["maximum_aqi"]),
        "minimum_aqi": float(stats["minimum_aqi"])
    }


# ============================================================
# ALL CITIES
# ============================================================

@app.get("/cities")
def get_all_cities():

    rows = (
        prediction_df
        .groupBy("City")
        .agg(
            count("*").alias("records"),
            avg("AQI").alias("average_aqi"),
            avg("prediction").alias("average_predicted_aqi"),
            spark_max("AQI").alias("maximum_aqi"),
            spark_min("AQI").alias("minimum_aqi")
        )
        .orderBy(desc("average_aqi"))
        .collect()
    )

    cities = []

    for row in rows:

        cities.append({
            "city": row["City"],
            "records": int(row["records"]),
            "average_aqi": round(float(row["average_aqi"]), 2),
            "average_predicted_aqi": round(
                float(row["average_predicted_aqi"]), 2
            ),
            "maximum_aqi": float(row["maximum_aqi"]),
            "minimum_aqi": float(row["minimum_aqi"])
        })

    return {
        "cities": cities
    }


# ============================================================
# CITY ANALYSIS
# ============================================================

@app.get("/city/{city_name}")
def city_analysis_basic(city_name: str):

    city_df = prediction_df.filter(
        col("City") == city_name
    )

    if city_df.limit(1).count() == 0:

        return {
            "error": "City not found"
        }

    result = (
        city_df
        .select(
            count("*").alias("records"),
            avg("AQI").alias("average_aqi"),
            avg("prediction").alias("average_predicted_aqi"),
            spark_max("AQI").alias("maximum_aqi"),
            spark_min("AQI").alias("minimum_aqi")
        )
        .collect()[0]
    )

    return {
        "city": city_name,
        "records": int(result["records"]),
        "average_aqi": round(float(result["average_aqi"]), 2),
        "average_predicted_aqi": round(
            float(result["average_predicted_aqi"]), 2
        ),
        "maximum_aqi": float(result["maximum_aqi"]),
        "minimum_aqi": float(result["minimum_aqi"])
    }


# ============================================================
# TIMELINE
# ============================================================

@app.get("/timeline/{city_name}")
def city_timeline(city_name: str):

    city_df = prediction_df.filter(
        col("City") == city_name
    )

    if city_df.limit(1).count() == 0:

        return {
            "error": "City not found"
        }

    rows = (
        city_df
        .select(
            "Date",
            "AQI",
            "prediction",
            "AQI_Bucket"
        )
        .orderBy("Date")
        .collect()
    )

    data = []

    for row in rows:

        data.append({
            "date": str(row["Date"]),
            "aqi": (
                float(row["AQI"])
                if row["AQI"] is not None
                else None
            ),
            "predicted_aqi": (
                float(row["prediction"])
                if row["prediction"] is not None
                else None
            ),
            "category": row["AQI_Bucket"]
        })

    return {
        "city": city_name,
        "data": data
    }


# ============================================================
# TOP POLLUTED CITIES
# ============================================================

@app.get("/top-polluted")
def top_polluted():

    rows = (
        prediction_df
        .groupBy("City")
        .agg(
            avg("AQI").alias("average_aqi"),
            avg("prediction").alias("average_predicted_aqi"),
            count("*").alias("records")
        )
        .orderBy(desc("average_aqi"))
        .limit(10)
        .collect()
    )

    cities = []

    for row in rows:

        cities.append({
            "city": row["City"],
            "average_aqi": round(float(row["average_aqi"]), 2),
            "average_predicted_aqi": round(
                float(row["average_predicted_aqi"]), 2
            ),
            "records": int(row["records"])
        })

    return {
        "cities": cities
    }


# ============================================================
# CITY DETAILS DATASET
# ============================================================

@app.get("/city-details/{city_name}")
def city_details(city_name: str):

    df = city_details_df.filter(
        col("city") == city_name
    )

    if df.limit(1).count() == 0:

        return {
            "error": "City details not found"
        }

    row = df.collect()[0]

    return {
        "city": row["city"],
        "state": row["state"],
        "population": row["pop"],
        "population_density": row["pop_dens"],
        "area_km2": row["area_km2"]
    }


# ============================================================
# WEATHER SUMMARY
# ============================================================

@app.get("/weather-summary")
def weather_summary():

    result = (
        weather_df
        .select(
            count("*").alias("records"),
            avg("T2M").alias("average_temperature"),
            avg("RH2M").alias("average_humidity"),
            avg("PRECTOTCORR").alias("average_precipitation"),
            avg("WS2M").alias("average_wind_speed"),
            avg("PS").alias("average_pressure")
        )
        .collect()[0]
    )

    return {
        "records": int(result["records"]),
        "average_temperature": round(
            float(result["average_temperature"]), 2
        ),
        "average_humidity": round(
            float(result["average_humidity"]), 2
        ),
        "average_precipitation": round(
            float(result["average_precipitation"]), 2
        ),
        "average_wind_speed": round(
            float(result["average_wind_speed"]), 2
        ),
        "average_pressure": round(
            float(result["average_pressure"]), 2
        )
    }


# ============================================================
# WEATHER BY CITY
# ============================================================

@app.get("/weather/{city_name}")
def weather_city(city_name: str):

    df = weather_df.filter(
        col("City") == city_name
    )

    if df.limit(1).count() == 0:

        return {
            "error": "Weather data not found"
        }

    result = (
        df
        .select(
            count("*").alias("records"),
            avg("T2M").alias("temperature"),
            avg("RH2M").alias("humidity"),
            avg("PRECTOTCORR").alias("precipitation"),
            avg("WS2M").alias("wind_speed"),
            avg("PS").alias("pressure")
        )
        .collect()[0]
    )

    return {
        "city": city_name,
        "records": int(result["records"]),
        "temperature": round(float(result["temperature"]), 2),
        "humidity": round(float(result["humidity"]), 2),
        "precipitation": round(
            float(result["precipitation"]), 2
        ),
        "wind_speed": round(
            float(result["wind_speed"]), 2
        ),
        "pressure": round(
            float(result["pressure"]), 2
        )
    }


# ============================================================
# VEHICLE SUMMARY
# ============================================================

@app.get("/vehicle-summary")
def vehicle_summary():

    rows = vehicle_df.collect()

    total_by_year = {}

    years = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020"
    ]

    for year in years:

        total = 0

        for row in rows:

            value = row[year]

            if value is not None:

                try:
                    total += float(value)
                except:
                    pass

        total_by_year[year] = total

    return {
        "cities": vehicle_df.count(),
        "years": total_by_year
    }


# ============================================================
# VEHICLE DATA BY CITY
# ============================================================

@app.get("/vehicle/{city_name}")
def vehicle_city(city_name: str):

    df = vehicle_df.filter(
        col("City") == city_name
    )

    if df.limit(1).count() == 0:

        return {
            "error": "Vehicle data not found"
        }

    row = df.collect()[0]

    years = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020"
    ]

    data = []

    for year in years:

        value = row[year]

        if value is not None:

            try:
                value = float(value)
            except:
                value = 0

        else:
            value = 0

        data.append({
            "year": int(year),
            "vehicles": value
        })

    return {
        "city": city_name,
        "data": data
    }


# ============================================================
# VEHICLE-AQI RELATIONSHIP
# ============================================================

def get_vehicle_aqi(city_name: str):

    vehicle_result = vehicle_df.filter(
        col("City") == city_name
    )

    aqi_result = prediction_df.filter(
        col("City") == city_name
    )

    if (
        vehicle_result.limit(1).count() == 0
        or
        aqi_result.limit(1).count() == 0
    ):

        return {
            "city": city_name,
            "data": []
        }

    vehicle_row = vehicle_result.collect()[0]

    aqi_rows = (
        aqi_result
        .groupBy("Date")
        .agg(
            avg("AQI").alias("average_aqi")
        )
        .orderBy("Date")
        .collect()
    )

    years = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020"
    ]

    result = []

    for year in years:

        vehicle_value = vehicle_row[year]

        if vehicle_value is None:
            vehicle_value = 0

        try:
            vehicle_value = float(vehicle_value)
        except:
            vehicle_value = 0

        yearly_aqi = []

        for row in aqi_rows:

            date_string = str(row["Date"])

            if date_string.startswith(year):

                if row["average_aqi"] is not None:

                    yearly_aqi.append(
                        float(row["average_aqi"])
                    )

        if len(yearly_aqi) > 0:

            average_aqi = sum(yearly_aqi) / len(yearly_aqi)

        else:

            average_aqi = 0

        result.append({
            "year": int(year),
            "vehicles": vehicle_value,
            "average_aqi": round(average_aqi, 2)
        })

    return {
        "city": city_name,
        "data": result
    }


@app.get("/vehicle-aqi/{city_name}")
def vehicle_aqi(city_name: str):

    return get_vehicle_aqi(city_name)


# ============================================================
# 2026 FORECAST
# ============================================================

@app.get("/forecast/{city_name}")
def forecast_2026(city_name: str):

    city_df = prediction_df.filter(
        col("City") == city_name
    )

    if city_df.limit(1).count() == 0:

        return {
            "error": "City not found"
        }

    # --------------------------------------------------------
    # Get yearly AQI averages
    # --------------------------------------------------------

    rows = (
        city_df
        .select("Date", "AQI")
        .orderBy("Date")
        .collect()
    )

    yearly_values = {}

    for row in rows:

        if row["AQI"] is None:
            continue

        date_string = str(row["Date"])

        year = date_string[:4]

        try:
            year = int(year)
            aqi_value = float(row["AQI"])
        except:
            continue

        if year not in yearly_values:

            yearly_values[year] = []

        yearly_values[year].append(aqi_value)


    historical = []

    for year in sorted(yearly_values.keys()):

        values = yearly_values[year]

        if len(values) == 0:
            continue

        average_value = sum(values) / len(values)

        historical.append({
            "year": year,
            "aqi": round(average_value, 2)
        })


    # --------------------------------------------------------
    # Need enough data for forecast
    # --------------------------------------------------------

    if len(historical) < 2:

        return {
            "city": city_name,
            "historical": historical,
            "forecast": [],
            "message": "Not enough historical data for forecast."
        }


    # --------------------------------------------------------
    # Simple linear trend
    #
    # This is a trend-based forecast.
    # It is NOT the Random Forest model.
    # --------------------------------------------------------

    x_values = [
        item["year"]
        for item in historical
    ]

    y_values = [
        item["aqi"]
        for item in historical
    ]


    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)


    numerator = 0
    denominator = 0

    for x, y in zip(x_values, y_values):

        numerator += (
            (x - x_mean)
            *
            (y - y_mean)
        )

        denominator += (
            (x - x_mean) ** 2
        )


    if denominator == 0:

        slope = 0

    else:

        slope = numerator / denominator


    intercept = (
        y_mean
        -
        slope * x_mean
    )


    # --------------------------------------------------------
    # Generate 2026 prediction
    # --------------------------------------------------------

    predicted_2026 = (
        slope * 2026
        +
        intercept
    )


    # IMPORTANT:
    # Use Python min/max, NOT Spark max/min.
    predicted_2026 = max(
        0,
        float(predicted_2026)
    )


    predicted_2026 = round(
        predicted_2026,
        2
    )


    # --------------------------------------------------------
    # Generate yearly forecast points
    # --------------------------------------------------------

    forecast = []

    for year in range(2021, 2027):

        predicted = (
            slope * year
            +
            intercept
        )

        # IMPORTANT:
        # Python max() is now safe because we did not import
        # Spark max as "max".
        predicted = max(
            0,
            float(predicted)
        )

        forecast.append({
            "year": year,
            "predicted_aqi": round(
                predicted,
                2
            )
        })


    return {
        "city": city_name,
        "method": "Historical linear trend",
        "historical": historical,
        "forecast": forecast,
        "forecast_2026": predicted_2026,
        "trend_slope": round(
            float(slope),
            4
        )
    }


# ============================================================
# COMPLETE CITY ANALYSIS
# ============================================================

@app.get("/city-analysis/{city_name}")
def city_analysis(city_name: str):

    # --------------------------------------------------------
    # AQI
    # --------------------------------------------------------

    aqi_data = prediction_df.filter(
        col("City") == city_name
    )

    if aqi_data.limit(1).count() == 0:

        return {
            "error": "City not found"
        }


    aqi_result = (
        aqi_data
        .select(
            count("*").alias("records"),
            avg("AQI").alias("average_aqi"),
            avg("prediction").alias(
                "average_predicted_aqi"
            ),
            spark_max("AQI").alias("maximum_aqi"),
            spark_min("AQI").alias("minimum_aqi")
        )
        .collect()[0]
    )


    # --------------------------------------------------------
    # CITY DETAILS
    # --------------------------------------------------------

    city_details_result = city_details_df.filter(
        col("city") == city_name
    )


    city_details = {}

    if city_details_result.limit(1).count() > 0:

        row = city_details_result.collect()[0]

        city_details = {
            "state": row["state"],
            "population": row["pop"],
            "population_density": row["pop_dens"],
            "area_km2": row["area_km2"]
        }


    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    weather_result = weather_df.filter(
        col("City") == city_name
    )


    weather = {}

    if weather_result.limit(1).count() > 0:

        row = (
            weather_result
            .select(
                avg("T2M").alias("temperature"),
                avg("RH2M").alias("humidity"),
                avg("PRECTOTCORR").alias(
                    "precipitation"
                ),
                avg("WS2M").alias("wind_speed"),
                avg("PS").alias("pressure")
            )
            .collect()[0]
        )

        weather = {
            "temperature": round(
                float(row["temperature"]),
                2
            ),
            "humidity": round(
                float(row["humidity"]),
                2
            ),
            "precipitation": round(
                float(row["precipitation"]),
                2
            ),
            "wind_speed": round(
                float(row["wind_speed"]),
                2
            ),
            "pressure": round(
                float(row["pressure"]),
                2
            )
        }


    # --------------------------------------------------------
    # VEHICLES
    # --------------------------------------------------------

    vehicle_data = get_vehicle_aqi(
        city_name
    )


    # --------------------------------------------------------
    # RETURN EVERYTHING
    # --------------------------------------------------------

    return {
        "city": city_name,

        "aqi": {
            "records": int(
                aqi_result["records"]
            ),
            "average": round(
                float(aqi_result["average_aqi"]),
                2
            ),
            "predicted_average": round(
                float(
                    aqi_result[
                        "average_predicted_aqi"
                    ]
                ),
                2
            ),
            "maximum": float(
                aqi_result["maximum_aqi"]
            ),
            "minimum": float(
                aqi_result["minimum_aqi"]
            )
        },

        "city_details": city_details,

        "weather": weather,

        "vehicle_aqi": vehicle_data
    }


# ============================================================
# DATASET INFORMATION
# ============================================================

@app.get("/datasets")
def datasets():

    return {
        "datasets": [

            {
                "name": "city_day.csv",
                "purpose": "Historical AQI and pollutant observations",
                "records": aqi_df.count(),
                "columns": aqi_df.columns
            },

            {
                "name": "citydetails.csv",
                "purpose": "Population, density and geographical information",
                "records": city_details_df.count(),
                "columns": city_details_df.columns
            },

            {
                "name": "weather_india.csv",
                "purpose": "Historical weather conditions",
                "records": weather_df.count(),
                "columns": weather_df.columns
            },

            {
                "name": "vehicle_dataset.csv",
                "purpose": "City-wise vehicle population",
                "records": vehicle_df.count(),
                "columns": vehicle_df.columns
            },

            {
                "name": "ml_predictions",
                "purpose": "Machine learning AQI predictions",
                "records": prediction_df.count(),
                "columns": prediction_df.columns
            }

        ]
    }


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
def shutdown():

    global spark

    if spark is not None:

        print("Stopping Spark...")

        spark.stop()

        spark = None
