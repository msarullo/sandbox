'''
Created on Oct 3, 2012

@author: msarullo
'''

from msarullo.tornadoapp.handlers import default, websockettest, nextapi

handlers = [
        (r'/nextapi', nextapi.NextAPIHandler),
        (r'/websockettest', websockettest.WebSocketTestHandler),
        (r'/websocket', websockettest.WebSocketHandler),
        (r'/', default.DefaultHandler),
    ]
