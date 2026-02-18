# Fetch Weather Data Lambda

Triggered by: EventBridge (daily schedule)

Purpose:
- Calls https://api.weather.gov via its API to retrieve a 7-day weather forecast for a city
- Stores raw JSON in S3 proj-weather-api/raw bucket subfolder

Output:
s3://proj-weather-api/raw/year=YYYY/month=MM/day=DD/weather_CITYNAME_STATE_YYYYMMDD_TIMESTAMP.json

Example:
s3://proj-weather-api/raw/year=2026/month=02/day=16/weather_Auburn_Kentucky_20260216_182938.json