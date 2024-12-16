import httpx
import asyncio
from . import urls

async def fetch_paper_details(query, limit=10, retries=3, delay=5, callback=None, api_key=urls.SEMANTIC_SECRET):
    query_params = {
        'query': query,
        'limit': limit,
        'fields': 'title,year,abstract,authors.name'
    }
    headers = {
        'x-api-key': f'{api_key}',

    }
    url = urls.sscholar
    
    for attempt in range(retries):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=query_params, headers=headers)
                
                if response.status_code == 200:
                    response_json = response.json()
                    
                    paper_details_list = []

                    # Extract the necessary information from the data field
                    for paper in response_json.get('data', []):
                        paper_details = {
                            'title': paper.get('title', 'No title'),
                            'authors': [author.get('name', 'Unknown Author') for author in paper.get('authors', [])],
                            'year': paper.get('year', 'No year'),
                            'summary': paper.get('abstract', 'No summary available')
                        }
                        paper_details_list.append(paper_details)

                    # Call the callback function if provided
                    if callback:
                        callback(paper_details_list)
                    
                    return paper_details_list 
                
                elif response.status_code == 429:  # Too Many Requests
                    print("Rate limit exceeded. Retrying...")
                    await asyncio.sleep(delay)  # Wait before retrying
                
                else:
                    print(f"Unexpected status code {response.status_code}.")
                    return None  # Return None in case of unexpected status code
            
            except httpx.RequestError as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)  # Wait before retrying

    print("Max retries exceeded.")
    return None  # Return None if all retries fail

