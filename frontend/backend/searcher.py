import asyncio
import json
from .scrapper import arxv, scopus, gschol, semanticc

async def smart_searching(query):
    data_list = []

    def collect_result(result, source):
        if result:
            for text in result:
                title = text.get('title')
                authors = text.get('authors')
                summary = text.get('summary')
                publication_date = text.get('date')
                link = text.get('link')
                data_list.append(
                    {
                        'title': title,
                        'authors': authors,
                        'summary': summary,
                        'date': publication_date,
                        'link': link,
                        'source': source  # Menandai sumber
                    }
                )

    async def run_search(search_func, source, *args):
        try:
            # Menerapkan batas waktu 10 detik untuk setiap pencarian
            await asyncio.wait_for(search_func(*args, callback=lambda result: collect_result(result, source)), timeout=10.0)
        except asyncio.TimeoutError:
            print(f"Timeout while fetching data from {source}")

    await asyncio.gather(
        run_search(arxv.search_arxiv, 'arXiv', query),
        # run_search(scopus.search_scopus, 'Scopus', query),
        run_search(gschol.search_google_scholar, 'Google Scholar', query),
        run_search(semanticc.fetch_paper_details, 'Semantic Scholar', query),
    )

    return data_list  # Mengembalikan sebagai objek Python

def run_smart_searching(query):
    combined_results = asyncio.run(smart_searching(query))
    print(combined_results)
    return combined_results

