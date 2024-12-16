import httpx
import asyncio
import xml.etree.ElementTree as ET

def parse_arxiv_response(response_text):
    papers = []
    root = ET.fromstring(response_text)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        pdf_url = next((link.attrib['href'] for link in entry.findall('{http://www.w3.org/2005/Atom}link') if link.attrib.get('title', '').lower() == 'pdf'), 'No PDF URL')
        published_date = entry.find('{http://www.w3.org/2005/Atom}published').text

        papers.append({
            'title': title,
            'authors': authors,
            'summary': summary,
            'date': published_date,
            'link': pdf_url
        })

    return papers



async def search_arxiv(query, max_results=5, filter='all', callback=None):
    query_encoded = '+'.join(query.split())
    url = f'http://export.arxiv.org/api/query?search_query={filter}:{query_encoded}&start=0&max_results={max_results}'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            result = parse_arxiv_response(response.text)
            if callback:
                callback(result)
        else:
            print(f'Error: {response.status_code}')
            if callback:
                callback(None)

