from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: str
    source: str 
    url: str

class NewsResponse(NewsBase):
    id: int

    class Config:
        from_atributes = True

class NewsCreate(NewsBase):
    pass