from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter

from soap_service.soap import StockService, UserService


app_service = Application([StockService, UserService],
                          tns='soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11(),
                          name='SoapService'
                          )

application = WsgiApplication(app_service)

if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, application)
    server.serve_forever()