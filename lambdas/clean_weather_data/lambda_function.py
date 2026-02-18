import json
import boto3
import pandas as pd
import io
from urllib.parse import unquote_plus

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # Read raw JSON from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)

        # Flatten nested JSON
        df = pd.json_normalize(data['properties']['periods'])
        
        # Add city metadata
        df['city'] = data['city_metadata']['city']
        df['state'] = data['city_metadata']['state']
        df['latitude'] = data['city_metadata']['lat']
        df['longitude'] = data['city_metadata']['lon']

        # Fix data types
        df['startTime'] = pd.to_datetime(df['startTime'])
        df['endTime'] = pd.to_datetime(df['endTime'])
        df['temperature'] = df['temperature'].astype(int)

        # Clean column names (replace dots with underscores)
        df.columns = df.columns.str.replace('.', '_')

        # Convert to Parquet
        buffer = io.BytesIO()
        df.to_parquet(buffer, engine='pyarrow', index=False)
        buffer.seek(0)

        # Create curated path
        curated_key = key.replace('raw/', 'curated/').replace('.json', '.parquet')

        # Upload to S3
        s3.put_object(
            Bucket=bucket,
            Key=curated_key,
            Body=buffer.getvalue(),
            ContentType='application/octet-stream'
        )

        return {'statusCode': 200, 'body': f'Processed {key} to {curated_key}'}
    
    except Exception as e:
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
