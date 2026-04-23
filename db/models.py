from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    entity = Column(String)
    attribute = Column(String)
    value = Column(String)
    embedding = Column(JSON)
