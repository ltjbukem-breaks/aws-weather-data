# Clean Weather Data Lambda

Triggered by: Object being Put in the proj-weather-api/raw S3 bucket subfolder, .json file extension
- Bucket arn: arn:aws:s3:::proj-weather-api
- Event types: s3:ObjectCreated:Put

Purpose:
- Reads in raw .json file from fetch_weather_data lambda output
- Flattens json information, adds city/state/lat/lon metadata, fixes column datatypes, cleans column names
- Saves as parquet, stores in S3 proj-weather-api/curated bucket subfolder 

Output:
s3://proj-weather-api/curated/year=YYYY/month=MM/day=DD/weather_CITYNAME_STATE_YYYYMMDD_TIMESTAMP.parquet

Example:
s3://proj-weather-api/curated/year=2026/month=02/day=16/weather_Auburn_Kentucky_20260216_182938.parquet

Includes test_event.json as an example event input parameter to lambda_function.lambda_handler