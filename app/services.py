import httpx
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

async def get_news_from_api():
    url = f"https://newsapi.org/v2/everything?country=us&category=technology&apiKey={API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json() 

        return data.get("articles", [])

def get_news_from_rss(rss_url: str):
    feed = feedparser.parse(rss_url)

    articles = []

    for entry in feed.entries:
        title = getattr(entry, "title", "No Title")
        url = getattr(entry, "link", "")
        description = getattr(entry, "description", getattr(entry, "summary", ""))

        feed_title = getattr(feed.feed, "title", "RSS Source")  

        article_data = {
            "title": title,
            "description": description,
            "url": url,
            "source": {"name": feed_title}
        }

        articles.append(article_data)

    return articles
