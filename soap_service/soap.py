# -*- coding: utf-8 -*-

from spyne import rpc, ServiceBase, Integer, Unicode, Float, ComplexModel, String
from spyne.model.fault import Fault
from soap_service import handlers


class AuthHeader(ComplexModel):
    UserName = Unicode
    Session = Unicode


class StockService(ServiceBase):

    @rpc(Unicode(encoding='utf-8'), _operation_name='GetStockName', _returns=Float)
    def get_stock_name(ctx, StockName):
        result = handlers.get_stock_price(StockName)
        if not result:
            raise Fault('Client', 'Запись не найдена')
        return result

    @rpc(Unicode(encoding='utf-8'), Float(ge=0.0), _operation_name='SetStockPrice', _returns=Integer)
    def set_stock_price(ctx, StockName, Price):
        result = handlers.set_stock_price(StockName, Price)
        if result:
            raise Fault('Client', 'Невозможно изменить запись. Запись не найдена')
        return result


class UserService(ServiceBase):

    @rpc(Unicode, Unicode, _operation_name='Login', _returns=Unicode)
    def login(ctx, User, Password):
        return ''

    @rpc(Unicode, Unicode, _operation_name='Register', _returns=String)
    def register(ctx, UserName, Password):
        return ''

    @rpc(Unicode, _operation_name='ChangePassword', _returns=String, _in_header=(AuthHeader,))
    def change_password(ctx, Password):
        return ''