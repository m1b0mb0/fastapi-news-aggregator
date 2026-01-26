from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas, services

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(scrape_and_save, trigger="interval", minutes=15)
    scheduler.start()
    print("----- Планувальник запущено -----")

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

@app.get("/")
def root():
    return {"message": "News Aggregator is running"}

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
        raise HTTPException(status_code=404, detail="Новину не знайдено")
    
    return news

@app.post("/scrape-news")
async def scrape_news():
    await scrape_and_save()
    return {"message": "Запуск оновлення"}

async def scrape_and_save():
    with SessionLocal() as db:
        print("Починаємо завантаження...")

        try:
            api_data = await services.get_news_from_api()
        except Exception as e:
            print(f"Помилка NewsAPI: {e}")
            api_data = []
        
        rss_url = "https://www.theverge.com/rss/index.xml"
        rss_data = services.get_news_from_rss(rss_url)

        all_data = api_data + rss_data

        print(f"Отримано {len(all_data)} новин. Перевіряємо дублікати...")

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
                url = article["url"]
            )

            db.add(new_news)
            count += 1
        
        db.commit()
        print("Новини оновлено!")