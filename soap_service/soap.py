# -*- coding: utf-8 -*-

from spyne import rpc, ServiceBase, Integer, Unicode, Float
from spyne.model.fault import Fault
from soap_service import handlers


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
