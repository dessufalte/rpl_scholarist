import requests

api_key = 'sreN1kVSOg1mLkcc39k9o7scvBZhsRRUrepAsDDc'

def search_semantic_scholar(query):
    url = 'https://api.semanticscholar.org/v1/paper/search'
    params = {
        'query': query,
        'limit': 5
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f'Error: {response.status_code}')
        return []

def get_paper_metadata(paper_id):
    url = f'https://api.semanticscholar.org/v1/paper/{paper_id}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error: {response.status_code}')
        return {}


query = 'machine learning'
search_results = search_semantic_scholar(query)

# Menampilkan hasil pencarian
for paper in search_results:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(author['name'] for author in paper.get('authors', []))}")
    print(f"Year: {paper.get('year', 'No year available')}")
    print(f"Abstract: {paper.get('abstract', 'No abstract available')}")
    print(f"URL: {paper.get('url', 'No URL available')}\n")

# Mengambil metadata untuk artikel tertentu
if search_results:
    paper_id = search_results[0]['paperId']
    metadata = get_paper_metadata(paper_id)
    print("Detailed Metadata:")
    print(metadata)
