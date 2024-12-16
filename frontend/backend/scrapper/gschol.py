import httpx
import asyncio
from bs4 import BeautifulSoup
import urllib.parse
from . import urls

async def fetch_google_scholar_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            parse_google_scholar_response(response.text)
            return response.text
        else:
            print(f'Error: {response.status_code}')
            return None

def parse_google_scholar_response(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    results = []
    
    for item in soup.find_all('div', class_='gs_ri'):
        title = item.find('h3', class_='gs_rt').text if item.find('h3', class_='gs_rt') else 'No title'
        link = item.find('h3', class_='gs_rt').a['href'] if item.find('h3', class_='gs_rt').a else 'No link'
        snippet = item.find('div', class_='gs_rs').text if item.find('div', class_='gs_rs') else 'No snippet'

        
        metadata = item.find('div', class_='gs_a').text if item.find('div', class_='gs_a') else 'No metadata'
        authors, publication_date = parse_metadata(metadata)

        results.append({
            'title': title,
            'authors': authors,
            'summary': snippet,
            'date': publication_date,
            'link': link
        })

    return results

def parse_metadata(metadata):
    authors = 'No authors'
    publication_date = 'No publication date'
    parts = metadata.split('-')

    if len(parts) > 0:
        authors = parts[0].strip()

    if len(parts) > 1:

        date_parts = parts[-1].split()
        for part in date_parts:
            if part.isdigit() and len(part) == 4: 
                publication_date = part
                break

    return authors, publication_date

async def search_google_scholar(query, callback=None):
    query_encoded = urllib.parse.quote(query)
    url = urls.gschol + query_encoded

    response_text = await fetch_google_scholar_data(url)
    if response_text:
        results = parse_google_scholar_response(response_text)
        if callback:
            callback(results)
    else:
        if callback:
            callback(None)
