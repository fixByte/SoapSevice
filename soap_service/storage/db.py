# -*- coding: utf-8 -*-
import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Float, Integer, Sequence, String, ForeignKey, DateTime
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

class UserSession(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, Sequence('session_id_seq'), primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    expires = Column(DateTime)
    uid = Column(String)

    def __str__(self):
        return f'<Session:{self.user}. Expires: {self.expires}>'

def init_db():
    engine = _sqlite_engine()
    Base.metadata.create_all(engine)

@contextmanager
def session():
    factory = sessionmaker(bind=current_engine)
    session = factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def stock_create(name, price):
    with session() as s:
        Stock(name=name, price=price)


def stock_edit_by_name(name, value):
    with session() as s:
        stock = s.query(Stock).filter_by(name=name).first()
        if stock:
            stock.price = value
            s.add(stock)
            return 0
    return 1


def stock_price_by_name(name):
    with session() as s:
        stock = s.query(Stock).filter_by(name=name).first()
        if stock:
            return stock.price
    return None


def user_create(name, password):
    with session() as s:
        if s.query(User).filter_by(name=name).first():
            return 1
        user = User(name=name, password=password)
        s.add(user)

def user_login(name, password):
    with session() as s:
        user = s.query(User.id, User.password).filter_by(name=name).first()
        if user:
            if user.password == password:
                u_session = user_session(user.id)
                return u_session

def user_has_permissions(user_name, session_uid):
    with session() as s:
        user = s.query(User.id).filter_by(name=user_name).first()
        if user:
            if s.query(UserSession).filter_by(user=user.id, uid=session_uid).first():
                return True

def user_session(user_id):
    with session() as s:
        session_uid = s.query(UserSession.uid).filter_by(user=user_id).first()
        if session_uid:
            return session_uid.uid
        else:
            uid = str(uuid.uuid4())
            expires = datetime.now() + timedelta(days=10)
            user_session = UserSession(user=user_id, expires=expires, uid=uid)
            s.add(user_session)
            return user_session.uid
