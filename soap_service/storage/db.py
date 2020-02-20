# -*- coding: utf-8 -*-
import os

from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Float, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.environ.get('DB_PATH', os.path.dirname(os.path.realpath(__file__)))
DB_NAME = os.environ.get('DB_NAME', 'app.db')

Base = declarative_base()


def _sqlite_engine():
    db_path = os.path.join(DB_PATH, DB_NAME)
    engine = create_engine(f'sqlite:///{db_path}')
    return engine

current_engine = _sqlite_engine()

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

@contextmanager
def session():
    session = sessionmaker()
    session.configure(bind=current_engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def _get_session():
    engine = _sqlite_engine()
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def stock_create(name, price):
    session = _get_session()
    stock = Stock(name=name, price=price)
    session.add(stock)
    session.commit()


def stock_edit_by_name(name, value):
    session = _get_session()
    stock = session.query(Stock).filter_by(name=name).first()
    if stock:
        stock.price = value
        session.add(stock)
        session.commit()
        return 0
    return 1


def stock_price_by_name(name):
    session = _get_session()
    stock = session.query(Stock).filter_by(name=name).first()
    if stock:
        return stock.price
    return None


def user_create(name, password):
    session = _get_session()
    if session.query(User).filter_by(name=name).first():
        return 1
    user = User(name=name, password=password)
    session.add(user)
    session.commit()
