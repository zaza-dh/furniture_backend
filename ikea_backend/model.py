from ikea_backend.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.types import Date


class Articles(Base):
    __tablename__ = "Articles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    stock = Column(Integer)

class Products(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Float, default=0)

class ProductComponents(Base):
    __tablename__ = "ProductComponents"

    id = Column(Integer, primary_key=True)
    prod_id = Column(Integer,ForeignKey('Products.id'))
    art_id = Column(Integer, ForeignKey('Articles.id') )
    amount = Column(Integer)
