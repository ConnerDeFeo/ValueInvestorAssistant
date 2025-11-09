# compare_10k_filings Lambda (API endpoint)
import json
import boto3
import uuid
from user_auth import post_auth_header
from dynamo import put_item

lambda_client = boto3.client('lambda')

def compare_10k_filings(event, context):
    body = json.loads(event['body'])
    auth_header = post_auth_header()

    try:
        url1 = body['url1']
        url2 = body['url2']
        sections = body['sections'] # Sections to compare
    
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Store initial job status
        put_item('comparison_jobs', {
            'job_id': job_id,
            'status': 'PROCESSING',
        })
        
        # Invoke async worker Lambda
        lambda_client.invoke(
            FunctionName='compare_10k_filings_worker',
            InvocationType='Event',
            Payload=json.dumps({
                'jobId': job_id,
                'url1': url1,
                'url2': url2,
                'sections': sections
            })
        )
        
        return {
            'statusCode': 202,  # Accepted
            'headers': auth_header,
            'body': json.dumps(job_id)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': auth_header,
            'body': json.dumps({'error': f'Missing parameter: {str(e)}'})
        }