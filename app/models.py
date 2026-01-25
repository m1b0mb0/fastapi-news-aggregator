from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    source = Column(String)
    url = Column(Text, unique=True)