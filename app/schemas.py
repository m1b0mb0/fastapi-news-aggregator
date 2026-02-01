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


class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_atributes = True

class Token(BaseModel):
    access_token: str
    token_type: str