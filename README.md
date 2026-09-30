# Air Pollution Analysis and Prediction in Indian Cities

An end-to-end Big Data and Machine Learning project for analyzing air pollution and predicting Air Quality Index (AQI) across Indian cities.

## 📌 Project Overview

Air pollution is a major environmental and public-health concern in India. This project uses Big Data technologies and Machine Learning to process air-quality data, analyze pollution patterns, and generate AQI predictions.

The project combines **Hadoop, HDFS, Apache Spark, PySpark, Spark ML, Docker, and FastAPI** into an end-to-end data processing and prediction pipeline.

## 🎯 Objectives

* Analyze air pollution data from Indian cities.
* Clean and preprocess the collected datasets.
* Handle missing values in the data.
* Prepare data for Machine Learning.
* Train a Machine Learning model for AQI prediction.
* Generate AQI predictions.
* Provide processed prediction data through a backend API.
* Build the complete environment using Docker.

## 🛠️ Technologies Used

| Technology   | Purpose                                     |
| ------------ | ------------------------------------------- |
| Python       | Data processing and application development |
| PySpark      | Large-scale data processing                 |
| Apache Spark | Distributed processing and Machine Learning |
| Spark ML     | AQI prediction model                        |
| Hadoop HDFS  | Distributed data storage                    |
| Docker       | Containerization and environment management |
| FastAPI      | Backend API                                 |
| Spark SQL    | Data querying and processing                |

## 🏗️ Project Architecture

```text
                         Raw Datasets
                              │
                              ▼
                         Hadoop / HDFS
                              │
                              ▼
                     Apache Spark / PySpark
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
            Data Cleaning           Data Analysis
                  │
                  ▼
          Missing Value Handling
                  │
                  ▼
          Prediction Dataset
                  │
                  ▼
            Spark ML Model
                  │
                  ▼
             AQI Predictions
                  │
                  ▼
             FastAPI Backend
```

## 📂 Datasets

The project uses multiple datasets related to Indian cities and environmental conditions:

* `city_day.csv` — daily air-quality measurements.
* `weather_india.csv` — weather-related information.
* `vehicle_dataset.csv` — vehicle-related information.
* `citydetails.csv` — city information.

The raw datasets are not included in this repository to avoid committing large data files.

## 🔄 Data Processing Pipeline

### 1. Data Inspection

The raw air-quality dataset is inspected to understand:

* Number of rows and columns
* Available features
* Missing values
* Data types
* AQI-related information

### 2. Data Cleaning

The air-quality data is cleaned using PySpark.

The cleaned dataset is stored in HDFS:

```text
/airpollution/cleaned/city_day
```

### 3. Prediction Dataset

A separate dataset is prepared for Machine Learning prediction:

```text
/airpollution/prediction/city_day
```

### 4. Missing Value Imputation

Missing values in the prediction dataset are handled before model training.

The imputed dataset is stored at:

```text
/airpollution/prediction/imputed_city_day
```

### 5. Machine Learning

A Spark ML pipeline is used to prepare the features and train the AQI prediction model.

The trained model is then used to generate predictions.

Prediction results are stored in:

```text
/airpollution/ml_predictions
```

## 🚀 Running the Project

### Prerequisites

* Docker Desktop
* Git
* Windows Subsystem for Linux 2 (WSL2)

### Start the Docker Environment

Open PowerShell:

```powershell
cd C:\AirPollutionProject\docker
docker compose up -d
```

Check the running containers:

```powershell
docker ps
```

The main services are:

* Hadoop NameNode
* Hadoop DataNode
* Spark Master
* Spark Worker
* FastAPI Backend

### Backend

The FastAPI backend runs on:

```text
http://localhost:8000
```

## 📁 Project Structure

```text
AirPollutionProject/
│
├── backend/
│   ├── app.py
│   └── Dockerfile
│
├── docker/
│   ├── docker-compose.yml
│   └── hadoop-config/
│
├── frontend/
│
├── spark/
│   └── scripts/
│       ├── inspect_city_day.py
│       ├── clean_city_day.py
│       ├── verify_cleaned.py
│       ├── check_missing_cleaned.py
│       ├── calculate_medians.py
│       ├── create_prediction_data.py
│       ├── impute_prediction_data.py
│       ├── verify_prediction.py
│       ├── check_missing_prediction.py
│       ├── train_aqi_model.py
│       ├── predict_aqi.py
│       ├── check_prediction_rows.py
│       └── city_aqi_analysis.py
│
├── .gitignore
└── README.md
```

## 🔍 HDFS Data Locations

Cleaned air-quality data:

```text
/airpollution/cleaned/city_day
```

Prediction dataset:

```text
/airpollution/prediction/city_day
```

Imputed prediction dataset:

```text
/airpollution/prediction/imputed_city_day
```

Machine Learning predictions:

```text
/airpollution/ml_predictions
```

## 📊 Machine Learning Workflow

```text
Imputed Dataset
      │
      ▼
Feature Selection
      │
      ▼
Vector Assembly
      │
      ▼
Model Training
      │
      ▼
Trained AQI Model
      │
      ▼
Prediction
      │
      ▼
AQI Prediction Results
```

## 🌐 Backend

The backend is implemented using **FastAPI** and **PySpark**.

It loads the processed prediction data along with supporting weather, vehicle, and city information and provides the processed information through API endpoints.

## 🐳 Docker Architecture

The project uses Docker containers to create a reproducible Big Data environment.

```text
                    Docker Network
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
   NameNode          DataNode         Spark Master
                                           │
                                           ▼
                                      Spark Worker
                                           │
                                           ▼
                                      FastAPI Backend
```

## 📌 Future Improvements

* Improve AQI prediction accuracy through additional feature engineering.
* Compare multiple Machine Learning algorithms.
* Add interactive visualizations and dashboards.
* Improve API functionality.
* Add real-time or regularly updated air-quality data.
* Deploy the application to a cloud environment.

## 👩‍💻 Project

Developed as a Big Data and Machine Learning project focused on air pollution analysis and AQI prediction in Indian cities.
