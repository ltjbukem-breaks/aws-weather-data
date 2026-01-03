# Script Name: ingest_weather.py
# Description: Ingests weather data via an API from NOAA (https://www.weather.gov/documentation/services-web-api)
# Author: Alistair A.

import pandas as pd
import requests
import json

# Test retrieve from API
test_url = "https://api.weather.gov/points/38.8894,-77.0352"

response_API = requests.get(test_url)

data = response_API.text

parsed_data = json.loads(data)

parsed_data.keys()

parsed_data['properties']['forecast']

# Pull the URL from the properties/forecast json
forecast_url = parsed_data['properties']['forecast']

forecast_response = requests.get(forecast_url)

forecast_data = forecast_response.text

forecast_parsed_data = json.loads(forecast_data)

# Convert to pd.DataFrame
df = pd.json_normalize(forecast_parsed_data)

df.columns

forecast_parsed_data.keys()
forecast_parsed_data['properties'].keys()
forecast_parsed_data['properties']['periods'] # This has each day of the week

# Saving as .JSON for easier viewing
with open("weather.json", "w", encoding="utf-8") as f:
    json.dump(forecast_parsed_data, f)

# Testing converting the weekly forecast into a pd.dataframe
# Still has some sublists but can at least store this as S3, then clean up in Glue
df_periods = pd.DataFrame(forecast_parsed_data['properties']['periods'])
df_periods.columns

df_periods['startTime']
df_periods['endTime']
df_periods['temperature']
df_periods['shortForecast']
df_periods['probabilityOfPrecipitation'][3]['value']
