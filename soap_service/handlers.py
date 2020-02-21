# -*- coding: utf-8 -*-
from soap_service.storage import db


def change_password(user_name, password, token):
    if has_permissions(user_name, token):
        token = db.user_change_password(user_name, password)
        return get_message(True, token)

    return get_message(False, 'Нет прав доступа.', 'Client')

def create_stock(user_name, token, stock_name, stock_price):
    if has_permissions(user_name, token):
        result = db.stock_create(stock_name, stock_price)
        if result:
            return get_message(True, result)
        return get_message(False, 'Уже существует', 'Server')


def create_user(user_name, password):
    result = db.user_create(user_name, password)
    if result:
        return get_message(False, 'Пользователь уже существует', 'Server')
    return get_message(True, 'Пользователь создан.')


def get_message(result=False, message='', side=''):
    return dict(result=result, message=message, side=side)


def get_stock_price(name):
    price = db.stock_price_by_name(name)
    if price:
        return get_message(True, price)
    return get_message(False, 'Запись не найдена.', 'Server')


def has_permissions(user_name, token):
    permissions = db.user_has_permissions(user_name, token)
    if permissions:
        return True
    return False


def login(user_name, password):
    token = db.user_login(user_name, password)
    if token:
        return get_message(True, token)
    return get_message(False, 'Неверные логин или пароль.', 'Client')


def set_stock_price(user_name, token, name, price):
    if has_permissions(user_name, token):
        result = db.stock_edit_by_name(name, price)
        if result:
            return get_message(True, result)
        return get_message(False, 'Запись не найдена.', 'Server')
    return get_message(False, 'Нет прав доступа.', 'Client')
