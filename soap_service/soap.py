# -*- coding: utf-8 -*-

from spyne import rpc, ServiceBase, Integer, Unicode, Float, String, Service
from spyne.model.complex import ComplexModel
from spyne.model.fault import Fault
from spyne.model.primitive import Mandatory

from soap_service import handlers


class AuthHeader(ComplexModel):
    __namespace__ = 'soap'
    UserName = Mandatory.Unicode
    Token = Mandatory.Unicode


class StockService(Service):

    @rpc(Unicode(encoding='utf-8'), Float(ge=0.0), _in_header=(AuthHeader,), _operation_name='CreateStock',
         _returns=Float)
    def create_stock(ctx, StockName, StockPrice):
        user_name = ctx.in_header.UserName
        token = ctx.in_header.Token
        if all([user_name, token]):
            result = handlers.create_stock(user_name, token, StockName, StockPrice)
            if result['result']:
                return result['message']
            raise Fault(result['side'], result['message'])
        raise Fault('Client', 'Нет прав доступа')

    @rpc(Unicode(encoding='utf-8'), _operation_name='GetStockPrice', _returns=Float)
    def get_stock_price(ctx, StockName):
        result = handlers.get_stock_price(StockName)
        if result['result']:
            return result['message']
        raise Fault(result['side'], result['message'])

    @rpc(Unicode(encoding='utf-8'), Float(ge=0.0), _in_header=(AuthHeader,), _operation_name='SetStockPrice',
         _returns=Integer)
    def set_stock_price(ctx, StockName, Price):
        user_name = ctx.in_header.UserName
        token = ctx.in_header.Token
        if all([user_name, token]):
            result = handlers.set_stock_price(user_name, token, StockName, Price)
            if result['result']:
                return result['message']
            raise Fault(result['side'], result['message'])
        raise Fault('Client', 'Нет прав доступа.')


class UserService(ServiceBase):

    @rpc(Unicode, Unicode, _operation_name='Login', _returns=String)
    def login(ctx, User, Password):
        result = handlers.login(User, Password)
        if result['result']:
            return result['message']
        raise Fault(result['side'], result['message'])

    @rpc(Unicode, Unicode, _operation_name='Register', _returns=String)
    def register(ctx, UserName, Password):
        result = handlers.create_user(UserName, Password)
        if result['result']:
            return result['message']
        raise Fault(result['side'], result['message'])

    @rpc(Unicode, Unicode, _operation_name='ChangePassword', _returns=String, _in_header=(AuthHeader,))
    def change_password(ctx, UserName, Password):
        token = ctx.in_header.Token
        user_name = ctx.in_header.UserName
        if all([user_name, token]):
            result = handlers.change_password(UserName, Password, token)
            if result['result']:
                return result['message']
            raise Fault(result['side'], result['message'])
        raise Fault('Client', 'Нет прав доступа.')
