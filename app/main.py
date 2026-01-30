from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas, services
from datetime import timezone
from dateutil import parser

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(scrape_and_save, trigger="interval", minutes=15)
    scheduler.start()
    print("----- The scheduler is running -----")

    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_date(date: str):
    dt = parser.parse(date)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.astimezone(timezone.utc)

@app.get("/")
def root():
    return {"message": "News Aggregator is running"}

@app.post("/news", response_model=schemas.NewsResponse)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    
    db_news = models.News(
        title=news.title,
        content=news.content,
        source=news.source,
        url=news.url,
        published_at = news.published_at
    )
    
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    return db_news 

@app.get("/news", response_model=list[schemas.NewsResponse])
def read_news(title:str = None, source:str = None, db:Session = Depends(get_db)):
    query = db.query(models.News)
    if title is not None:
       query = query.filter(models.News.title.contains(title))
    
    if source is not None:
       query = query.filter(models.News.source.contains(source))
    
    return query.all()
    

@app.get("/news/{news_id}", response_model=schemas.NewsResponse)
def read_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news = db.query(models.News).filter(models.News.id == news_id).first()

    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    
    return news

@app.delete("/news/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db_news = db.query(models.News).filter(models.News.id == news_id).first()

    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")

    db.delete(db_news)
    db.commit()

    return {"message": "News deleted"}

@app.post("/scrape-news")
async def scrape_news():
    await scrape_and_save()
    return {"message": "Running the update"}

async def scrape_and_save():
    with SessionLocal() as db:

        try:
            api_data = await services.get_news_from_api()
        except Exception as e:
            print(f"NewsAPI error: {e}")
            api_data = []
        
        rss_links = [
            "https://www.theverge.com/rss/index.xml",
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "https://itc.ua/ua/feed/"
        ]

        all_data = []

        for url in rss_links:
            all_data += services.get_news_from_rss(url)

        all_data += api_data

        print(f"{len(all_data)} news items retrieved. Checking for duplicates...")

        if not all_data:
            print("No news found.")
            return

        count = 0
        for article in all_data:
            existing_news = db.query(models.News).filter(models.News.url == article["url"]).first()
            if existing_news:
                continue

            source_name = article["source"]["name"]
            if not source_name:
                source_name = "Unknown"

            new_news = models.News(
                title = article["title"],
                content = article["description"] or "",
                source = source_name,
                url = article["url"],
                published_at = parse_date(article["publishedAt"])
            )

            db.add(new_news)
            db.flush()
            count += 1
        
        db.commit()
        print("News updated!")