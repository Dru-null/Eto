import asyncio
import os

import requests
from dotenv import load_dotenv

load_dotenv()
MAL_TOKEN = os.getenv("MAL_API_TOKEN")


async def malAnimeMainRequest(query):
    url = f"https://api.myanimelist.net/v2/anime?q={query}&limit=5"
    headers = {"X-MAL-CLIENT-ID": f"{MAL_TOKEN}"}
    response = await asyncio.to_thread(requests.get, url, headers=headers)

    response.raise_for_status()

    data = response.json()
    if data:
        id = matchResults(data["data"], query)
        if id is None:
            return
        return await malAnimeDetailsRequest(id)
    else:
        return None


async def malMangaMainRequest(query):
    url = f"https://api.myanimelist.net/v2/manga?q={query}&limit=5"
    headers = {"X-MAL-CLIENT-ID": f"{MAL_TOKEN}"}
    response = await asyncio.to_thread(requests.get, url, headers=headers)

    response.raise_for_status()

    data = response.json()
    if data:
        id = matchResults(data["data"], query)
        if id is None:
            return
        return await malMangaDetailsRequest(id)
    else:
        return None


async def malAnimeDetailsRequest(anime_id):
    if anime_id is None:
        return
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,mean,rank,popularity,status,genres,my_list_status,num_episodes,rating"
    headers = {"X-MAL-CLIENT-ID": f"{MAL_TOKEN}"}
    response = await asyncio.to_thread(requests.get, url, headers=headers)

    response.raise_for_status()

    data = response.json()
    if data:
        return data
    else:
        return


async def malMangaDetailsRequest(manga_id):
    if manga_id is None:
        return
    url = f"https://api.myanimelist.net/v2/manga/{manga_id}?fields=id,title,main_picture,start_date,end_date,mean,rank,popularity,status,genres,my_list_status,num_chapters,num_volumes,rating"
    headers = {"X-MAL-CLIENT-ID": f"{MAL_TOKEN}"}
    response = await asyncio.to_thread(requests.get, url, headers=headers)
    response.raise_for_status()

    data = response.json()
    if data:
        return data
    else:
        return


def matchResults(results, query):

    for result in results:
        if result["node"]["title"].lower() == query.lower():
            return result["node"]["id"]

    return
