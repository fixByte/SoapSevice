# -*- coding: utf-8 -*-
from soap_service.storage import db


def get_stock_price(name):
    price = db.stock_price_by_name(name)
    return price


def set_stock_price(name, price):
    result = db.stock_edit_by_name(name, price)
    return result
