from pydantic import BaseModel
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    content: str
    source: str 
    url: str
    published_at: datetime

class NewsResponse(NewsBase):
    id: int

    class Config:
        from_atributes = True

class NewsCreate(NewsBase):
    pass