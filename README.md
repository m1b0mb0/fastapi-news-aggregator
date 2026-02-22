# News Aggregator API

## Short Description
An asynchronous REST API built with FastAPI that automatically aggregates news from RSS feeds and external APIs, normalizes the data, and provides secure access through JWT authentication. 

## Technologies
* `Python`
* `FastAPI`
* `SQLAlchemy`
* `SQLite`
* `Bcrypt & Python-JOSE`
* `APScheduler`
* `HTTPX`
* `Python-Dateutil`

## Features
* **Automated Data Scraping:** Periodically fetches and updates news in the background without blocking the main thread.
* **Secure Authentication:** Complete user registration and login flow using secure JWT (JSON Web Tokens) and bcrypt password hashing.
* **Smart Data Normalization:** Automatically parses diverse, complex date formats from different RSS/API sources and standardizes them to UTC, preventing timezone conflicts.
* **Interactive Documentation:** Auto-generated Swagger UI for easy API testing and integration.

## Process
I started developing this API by designing the core SQLAlchemy database models for users and news articles. I used FastAPI's dependency injection to efficiently manage database sessions and maintain clean routing. After securing the endpoints with JWT authentication I built the asynchronous scraping logic. I designed a custom datetime parsing utility using `dateutil` to handle inconsistent formats across various RSS feeds and APIs, ensuring all incoming data is strictly normalized to UTC. Finally, I integrated `APScheduler` and `httpx` to handle the periodic, background fetching of new articles without blocking the main API thread.

## Running the Project

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a .env file in the root directory and add your secure keys: `SECRET_KEY=your_super_secret_key` `ALGORITHM=HS256` `NEWS_API_KEY=your_news_api_key`
4. Run the server: `uvicorn app.main:app --reload`
5. Open `http://127.0.0.1:8000/docs` in your browser
