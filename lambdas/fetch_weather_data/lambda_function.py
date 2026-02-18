import json
import os
import boto3
import requests
import random
from datetime import datetime
from io import StringIO
import csv

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # 1. Get configuration
        bucket_name = os.environ['S3_BUCKET_NAME']
        cities_file = os.environ.get('CITIES_FILE', 'weather-config/uscities.csv')
        
        # 2. Read cities CSV from S3
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=cities_file)
        csv_data = csv_obj['Body'].read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(csv_data))
        cities = list(csv_reader)
        
        # 3. Pick random city
        city = random.choice(cities)
        lat = city['lat']
        lon = city['lng']
        city_name = city['city']
        state = city['state_name']

        # 4. Call weather API with lat/lon
        url = f"https://api.weather.gov/points/{lat},{lon}"

        response_API = requests.get(url)
        data = response_API.text
        metadata = json.loads(data)
        forecast_url = metadata['properties']['forecast']
        forecast_response = requests.get(forecast_url)
        forecast_data = json.loads(forecast_response.text)
        
        # Add city metadata to the JSON
        forecast_data['city_metadata'] = {
            'city': city_name,
            'state': state,
            'lat': lat,
            'lon': lon
        }
        
        # 5. Create partitioned path: raw/year=YYYY/month=MM/day=DD/
        now = datetime.now()
        partition_path = f"raw/year={now.year}/month={now.month:02d}/day={now.day:02d}"
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        file_name = f"{partition_path}/weather_{city_name}_{state}_{timestamp}.json"
        
        # 6. Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(forecast_data),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Data saved to {file_name} for {city_name}, {state}')
        }
    except Exception as e:
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}