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
        stock1 = body['stock1']  # Expecting {accessionNumber, filingDate, primaryDocument}
        stock2 = body['stock2']  # Expecting {accessionNumber, filingDate, primaryDocument}
        sections = body['sections'] # Sections to compare

        if not sections:
            raise ValueError("Sections parameter is required")
    
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
                'stock1': stock1,
                'stock2': stock2,
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