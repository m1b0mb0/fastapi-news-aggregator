import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

async def get_news_from_api():
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json() 

        return data.get("articles", [])