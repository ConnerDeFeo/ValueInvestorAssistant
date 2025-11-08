import boto3
import json
from user_auth import get_auth_header

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('comparison_jobs') # type: ignore

def get_comparison_status(event, context):
    query_params = event.get('queryStringParameters', {})
    auth_header = get_auth_header()
    
    try:
        job_id = query_params['jobId']
        response = table.get_item(Key={'job_id': job_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': 'Job ID not found'
            }
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item']),
            'headers': auth_header
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Missing or invalid parameters: {str(e)}',
            'headers': auth_header
        }