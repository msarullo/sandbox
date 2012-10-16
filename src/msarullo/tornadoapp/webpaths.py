'''
Created on Oct 3, 2012

@author: msarullo
'''

from msarullo.tornadoapp.handlers import default, websockettest, nextapi, static

handlers = [
        (r'/editions', static.StaticHandler, dict(page="mockeditions.json", mimeType='application/json')),
        (r'/collections', static.StaticHandler, dict(page="mockcollections.json", mimeType='application/json')),
        (r'/items', static.StaticHandler, dict(page="mockitems.json", mimeType='application/json')),

        (r'/static/jquery.js', static.StaticHandler, dict(page="jquery-1.6.4.js", mimeType='application/javascript')),
        (r'/nextapi/query', nextapi.NextAPIQueryHandler),
        (r'/nextapi', static.StaticHandler, dict(page="nextapi.html", alwaysReload=False)),
        (r'/websockettest', websockettest.WebSocketTestHandler),
        (r'/websocket', websockettest.WebSocketHandler),
        (r'/', default.DefaultHandler),
    ]
