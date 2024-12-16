import httpx
import asyncio
from . import urls
async def fetch_scopus_data(base_url, api_key, params):
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if 'search-results' in data:
                search_results = data['search-results']
                entries = search_results.get('entry', [])

                if not isinstance(entries, list):
                    print("Warning: 'entry' is not a list.")
                    entries = []

                results = []
                for entry in entries:
                    title = entry.get('dc:title', 'No title')
                    authors_list = entry.get('author', [])
                    authors = [author.get('authname', 'Unknown Author') for author in authors_list]
                    summary = entry.get('dc:description', 'No summary available')
                    publication_date = entry.get('prism:coverDate', 'No date')
                    link = next((link.get('@href') for link in entry.get('link', []) if link.get('@rel') == 'scopus'), 'No link available')

                    results.append({
                        'title': title,
                        'authors': authors,
                        'summary': summary,
                        'date': publication_date,
                        'link': link
                    })

                return results
                    # 'total_results': search_results.get('opensearch:totalResults', '0'),
                    # 'items_per_page': search_results.get('opensearch:itemsPerPage', '0'),
                    
            else:
                print("Warning: 'search-results' not found in response.")
                return None

        except httpx.RequestError as e:
            print(f"Request failed: {e}")
            return None

async def search_scopus(query, api_key=urls.SCOPUS_SECRET, count=10, start=0, callback=None):
    base_url = urls.scopus
    
    params = {
        'query': query,
        'count': count,
        'start': start,
    }
    
    data = await fetch_scopus_data(base_url, api_key, params)
    if callback:
        callback(data)