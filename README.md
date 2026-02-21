# AWS Weather Data API Project
This repo contains an outline for AWS infrastructure to select a random city from uscities.csv and use its longitude and latitude to retrieve weather data via [an API](https://api.weather.gov) based on a schedule, and to process it using AWS's cloud based DE tools. This project is to demonstrate familiarity with AWS DE tools, and to showcase connecting them together to create ingestion and analytic pipeline capabilities.

## Tools used: 
- **AWS Lambda** – Serverless data processing  
- **S3** – Storage for raw and curated data  
- **EventBridge** – Scheduled invocation of Lambda  
- **IAM** – Roles and permissions for Lambda and services  
- **Glue Crawler** – Automatically infer schema from Parquet  
- **Athena** – Querying structured data with SQL  

## Folder Overview: 
- **/images** – Contains screenshots and images used for this repo
- **/lambdas** – Contains subfolders with lambda python functions & test event .json files
- **/queries** – Contains SQL queries for use in Athena to generate sample summary statistics
- **/sample_data** – Contains example raw .json file preprocessed, and a .parquet post processing file 
- **/weather-config** – Contains uscities.csv, used in the random sampling of a city to retrieve the weather data

## Example Input & Output files: 
- **Input** – Raw .json file retrieved from the weather API, contains nested information
    - Example filename: raw_weather_Auburn_Kentucky_20260216_182938.json
![image](images/sample_input.png)

- **Output** – Parquet file which is a flattened version of the raw .json file, with additional metadata for city, state, latitude, and longitude. 
    - Example filename: cleaned_weather_Auburn_Kentucky_20260216_182938.parquet
![image](images/sample_output.png)

## Architecture Overview:

![image](images/architecture_diagram.png)

1. **EventBridge Rule**: Triggers `fetch_weather_data` Lambda daily. Basic automation for triggering the ingestion and cleaning of data based on a schedule.
![image](images/infra_eventbridge.png)

2. **Fetch Weather Data Lambda**: Pulls weather data from an API and saves raw JSON to S3 (`raw/` folder, partitioned by date).
![image](images/infra_fetchWeatherData.png)

3. **S3 ObjectCreated Trigger**: Invokes `clean_weather_data` Lambda automatically when new JSON arrives.
![image](images/infra_s3trigger.png)

4. **Clean Lambda**: Flattens JSON, adds metadata and saves as Parquet in `curated/` folder.
![image](images/infra_cleanWeatherData.png)

5. **Glue Crawler**: Crawls Parquet files and updates the Athena Data Catalog based on a daily schedule.
![image](images/infra_crawler.png)

6. **Athena**: Creates an external table with our data. Queries the curated dataset with SQL to show summary statistics on rain preciptation, average temperature for the week, and average wind speed & direction information.
![image](images/infra_athena.png)

## Notes
- This project was created using an AWS Free Tier account
- Data is partitioned by year/month/day in S3 for efficient Athena querying
- Lambda functions utilize layers for Python package dependencies

## File & Folder Structure:
```text
├── README.md
├── architecture-diagram.png
│
├── lambdas/
│   ├── fetch_weather_data/
│   │   ├── lambda_function.py
│   │   └── README.md
│   │
│   ├── clean_weather_data/
│   │   ├── lambda_function.py
│   │   ├── README.md
│   │   └── test_event.json
│   │ 
│   └── layers/
│       └── README.md
│
├── queries/
│   ├── create_view.sql
│   ├── avg_temp_by_city.sql
│   ├── avg_winddirection_speed_by_city.sql
│   └── top_city_by_precip_prob.sql
│
├── sample_data/
│   ├── raw_sample.json
│   └── cleaned_sample.json
│
└── weather-config/
    └── uscities.csv
```

## Example queries 

### avg_winddirection_speed_by_city.sql
This query aggregates by city, state, wind direction, and forecast week to show the average wind speed direction (MPH) based on each direction. 
![image](images/winddirection_query.png)

```sql
SELECT
    city,
    state,
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    winddirection,
    ROUND(AVG(CAST(regexp_extract(windspeed, '([0-9]+)', 1) AS INTEGER)), 2) AS avg_wind_speed_mph
FROM curated_weather_analytics
WHERE winddirection IS NOT NULL AND trim(winddirection) <> ''
GROUP BY city, state, forecast_date, forecast_date + INTERVAL '7' DAY, winddirection
ORDER BY avg_wind_speed_mph DESC;
```

### top_city_by_precip_prob.sql
This query aggregates by city, state, and forecast week to show top cities based on the average of preciptation for the week.
![image](images/precip_query.png)

```sql
SELECT
    city,
    state,
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    ROUND(AVG(probabilityofprecipitation_value), 2) AS avg_precip_probability
FROM curated_weather_analytics
WHERE probabilityofprecipitation_value IS NOT NULL
GROUP BY city, state, forecast_date, forecast_date + INTERVAL '7' DAY
ORDER BY avg_precip_probability DESC
LIMIT 10;
```

### top_city_by_precip_prob.sql
This query aggregates by city, state, and forecast week to show the average temperature, min, and max temperature in F for that week.
![image](images/avg_temp_query.png)

```sql
SELECT
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    city,
    state,
    ROUND(AVG(temperature), 2) AS avg_temperature_F,
    MAX(temperature) AS max_temperature_F,
    MIN(temperature) AS min_temperature_F
FROM curated_weather_analytics
GROUP BY forecast_date, forecast_date + INTERVAL '7' DAY, city, state
ORDER BY avg_temperature_F DESC;
```
