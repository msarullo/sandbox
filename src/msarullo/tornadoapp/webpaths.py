'''
Created on Oct 3, 2012

@author: msarullo
'''

from msarullo.tornadoapp.handlers import default

handlers = [
        (r'/websocket', default.WebSocketHandler),
        (r'/', default.DefaultHandler),
    ]
