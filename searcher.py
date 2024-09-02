# main.py
import asyncio
from scrapper import arxv, scopus, gschol

async def smart_searching(query):
    def print_result(result):
        if result:
           print(result)
           for text in result:
               print(text)
        else:
            print("No result returned.")

    async def run_search(search_func, *args):
        await search_func(*args, callback=print_result)

    # Menjalankan semua fungsi secara bersamaan
    await asyncio.gather(
        run_search(arxv.search_arxiv, query),
        run_search(scopus.search_scopus, query),
        run_search(gschol.search_google_scholar, query)
    )

# Menjalankan fungsi
if __name__ == "__main__":
    query = 'quantum mechanics'
    asyncio.run(smart_searching(query))
