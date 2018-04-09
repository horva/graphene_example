from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine

class PersonModel(Base):
    __tablename__ = 'person'
    name = Column(String)
    age = Column(Integer)
    uuid = Column(Integer, primary_key=True)
    Articles = relationship("ArticleModel")

class ArticleModel(Base):
    __tablename__ = 'article'
    uuid = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey("person.uuid"))

# Base.metadata.create_all(engine)
Base.prepare(engine)
