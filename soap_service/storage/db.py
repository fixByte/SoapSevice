# -*- coding: utf-8 -*-
import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Float, Integer, Sequence, String, ForeignKey, DateTime
from sqlalchemy.exc import DBAPIError, DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def _postgresql_engine():
    host = os.environ.get('DB_HOST', '127.0.0.1')
    port = os.environ.get('DB_PORT', '5432')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    if all([user, password, db_name]):
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        return engine
    raise DatabaseError('Не возможно подключиться к базе данных. Проверьте учётные данные',
                        params=[user, password, db_name],
                        orig=None
                        )


def _select_db():
    db_type = os.environ.get('DB_TYPE')
    if db_type == 'postgres':
        return _postgresql_engine()
    else:
        return _sqlite_engine()


def _sqlite_engine():
    db_path = os.environ.get('DB_PATH', os.path.dirname(os.path.realpath(__file__)))
    db_name = os.environ.get('DB_NAME', 'app.db')
    db_path = os.path.join(db_path, db_name)
    engine = create_engine(f'sqlite:///{db_path}')
    return engine


current_engine = _select_db()


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


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, Sequence('token_id_seq'), primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    expires = Column(DateTime)
    uid = Column(String)

    def __str__(self):
        return f'<Token:{self.user}. Expires: {self.expires}>'


def init_db():
    engine = current_engine
    Base.metadata.create_all(engine)


@contextmanager
def session():
    factory = sessionmaker(bind=current_engine)
    current_session = factory()
    try:
        yield current_session
        current_session.commit()
    except DBAPIError:
        current_session.rollback()
        raise
    finally:
        current_session.close()


def stock_create(name, price):
    with session() as s:
        stock = s.query(Stock).filter_by(name=name).first()
        if stock:
            return False
        else:
            stock = Stock(name=name, price=price)
            s.add(stock)
            return stock.name


def stock_edit_by_name(name, value):
    with session() as s:
        stock = s.query(Stock).filter_by(name=name).first()
        if stock:
            stock.price = value
            s.add(stock)
            return stock.price
    return None


def stock_price_by_name(name):
    with session() as s:
        stock = s.query(Stock).filter_by(name=name).first()
        if stock:
            return stock.price
    return None


def user_change_password(user_name, password):
    with session() as s:
        user = s.query(User).filter_by(name=user_name).first()
        user.password = password
        s.add(user)
        user_token_remove(user.id)
        return user_token(user.id)


def user_create(name, password):
    with session() as s:
        if s.query(User).filter_by(name=name).first():
            return True
        user = User(name=name, password=password)
        s.add(user)



def user_login(name, password):
    with session() as s:
        user = s.query(User.id, User.password).filter_by(name=name).first()
        if user:
            if user.password == password:
                 return user_token(user.id)


def user_has_permissions(user_name, token_uid):
    with session() as s:
        user = s.query(User.id).filter_by(name=user_name).first()
        if user:
            if s.query(Token).filter_by(user=user.id, uid=token_uid).first():
                return True


def user_token(user_id):
    with session() as s:
        token = s.query(Token.uid).filter_by(user=user_id).first()
        if token:
            return token.uid
        else:
            uid = str(uuid.uuid4())
            expires = datetime.now() + timedelta(days=10)
            token = Token(user=user_id, expires=expires, uid=uid)
            s.add(token)
            return token.uid


def user_token_remove(user_id):
    with session() as s:
        token = s.query(Token).filter_by(user=user_id).first()
        s.delete(token)
