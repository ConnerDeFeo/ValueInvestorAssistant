import httpx

# Fetch 10-K filing from SEC EDGAR
async def fetch_10k_from_sec(url: str):
    headers = {
        "User-Agent": "Conner DeFeo ninjanerozz@gmail.com"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, follow_redirects=True)
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch: {response.status_code}")