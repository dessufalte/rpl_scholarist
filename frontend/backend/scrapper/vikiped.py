import requests
from . import urls

def search_wikipedia(query, api_key=urls.WIKI_SECRET):

    base_url = urls.vikiapi
    
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'utf8': 1,
        'srlimit': 5 
    }
    
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    try:
        
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_wikipedia_response(response_json):
    if response_json is None:
        return []

    papers = []
    search_results = response_json.get('query', {}).get('search', [])

    for result in search_results:
        papers.append({
            'title': result.get('title'),
            'snippet': result.get('snippet'),
            'pageid': result.get('pageid')
        })

    return papers

def get_wikipedia_page(page_id, api_key=None):
    base_url = urls.vikiapi
 
    params = {
        'action': 'query',
        'format': 'json',
        'pageids': page_id,
        'prop': 'extracts',
        'explaintext': 1
    }
    
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    try:

        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

api_key = urls.WIKI_SECRET
query = 'machine learning'
response_json = search_wikipedia(query, api_key)

if response_json:
    pages = parse_wikipedia_response(response_json)
    
    for page in pages:
        print(f"Title: {page['title']}")
        print(f"Snippet: {page['snippet']}\n")
        
       
        page_detail = get_wikipedia_page(page['pageid'], api_key)
        if page_detail:
            page_extract = page_detail.get('query', {}).get('pages', {}).get(str(page['pageid']), {}).get('extract', 'No extract available')
            print(f"Extract: {page_extract}\n")
