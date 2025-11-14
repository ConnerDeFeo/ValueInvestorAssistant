import json
import requests
from user_auth import get_auth_header

def get_available_10k_filings(event, context):
    query = event.get("queryStringParameters", {}) or {}
    auth_header = get_auth_header()

    try:
        cik = query["cik"]
        headers = {
            'User-Agent': 'Conner DeFeo ninjanerozz@gmail.com'
        }

        cik_padded = cik.zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

        response = requests.get(url, headers=headers)
        data = response.json()

        filings = data['filings']['recent']
        ten_k_filings = []
        for i, form in enumerate(filings['form']):
            if form == '10-K':
                filing_info = {
                    'accessionNumber': filings['accessionNumber'][i],
                    'filingDate': filings['filingDate'][i],
                    'primaryDocument': filings['primaryDocument'][i],
                }
                ten_k_filings.append(filing_info)
        return {
            "statusCode": 200,
            "body": json.dumps(ten_k_filings),
            "headers": auth_header
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal Server Error: {e}"}),
            "headers": auth_header
        }