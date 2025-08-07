import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    upc = Column(String, unique=True)
    mpn = Column(String)
    source_url = Column(String, nullable=False)
    retailer = Column(String, nullable=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Product(name='{self.name}', price='{self.price}', retailer='{self.retailer}')>"
