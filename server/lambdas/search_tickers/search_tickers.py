import json
import os

TICKER_FILE = os.path.join(os.path.dirname(__file__), 'tickers.json')
with open(TICKER_FILE) as f:
    ALL_TICKERS = json.load(f)

def search_tickers(event, context):
    query = event.get('queryStringParameters', {})
    try:
        search_term = query.get('q', '').upper()
        if not search_term:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Query parameter "q" is required.'})
            }
        # Search for tickers that match the search term
        results = []
        for ticker, info in ALL_TICKERS.items():
            if search_term in ticker or search_term in info.get('name', '').upper():
                results.append({
                    'ticker': ticker,
                    'name': info.get('name', ''),
                    'exchange': info.get('exchange', '')
                })
        return {
            'statusCode': 200,
            'body': json.dumps({'results': results[:10]})  # return top 10 results
        }
    except Exception as e:
        print("Error in search_tickers:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }