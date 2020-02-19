# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine, Column, Float, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.environ.get('DB_PATH', '')
DB_NAME = os.environ.get('DB_NAME', 'app.db')

Base = declarative_base()


def _sqlite_engine():
    db_path = os.path.join(DB_PATH, DB_NAME)
    engine = create_engine(f'sqlite:///{db_path}')
    return engine


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, Sequence('stock_id_seq'), primary_key=True)
    name = Column(String(100))
    price = Column(Float)

    def __str__(self):
        return f'<Stock: {self.name}({self.price})>'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String)

    def __str__(self):
        return f'<User: {self.name}>'

def init_db():
    engine = _sqlite_engine()
    Base.metadata.create_all(engine)
