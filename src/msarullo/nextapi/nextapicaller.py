'''
Created on Oct 9, 2012

@author: msarullo
'''

import logging
from tornado.httpclient import AsyncHTTPClient

#from tornado.web import HTTPError

#import httplib
#from json import JSONDecoder
#from nextapimodel import NextAPICollection

def qs(str):
    return '"' + str.strip('\'"') + '"'

class NextRequest(object):
    def __init__(self, host, port, method, resource):
        self.method = method
        self.uri = "/" + resource

        if 443 == port:
            self.url = "https://" + host
        else:
            self.url = "http://" + host
            if 80 != port:
                self.url += ":" + str(port)
        self.url += self.uri

    def __str__(self):
        return '{"method":'+qs(self.method)+',"uri":'+qs(self.uri)+',"url":'+qs(self.url)+'}'
    

class NextResponse(object):
    status = 0
    reason = "Call not yet issued"
    headers = []
    body = ""

    def read(self, resp):
        self.status = resp.code
        self.reason = resp.error.message if resp.error else 'UNKNOWN'
        self.headers = resp.headers if resp.headers else []
        self.body = resp.body if resp.body else '{}'

    def __str__(self):
        headers = '['
        for headerName, headerValue in self.headers.iteritems():
            if len(headers) > 2:
                headers+=','
            headers += '{"name":'+qs(headerName)+',"value":'+qs(headerValue)+'}'
            headerName = None
                
        headers += ']'
        return '{"status":'+str(self.status)+',"reason":'+qs(self.reason)+',"headers":'+headers+',"body":'+self.body+'}'

class NextAPICall(object):
    def __init__(self, host, port, method, resource):
        self.req = NextRequest(host, port, method, resource)
        self.resp = NextResponse()
    
    def __str__(self):
        return '{"req":'+str(self.req)+',"resp":'+str(self.resp)+'}'
    
    
class NextAPICaller(object):

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.apiHost = kwargs["host"] if "host" in kwargs else "localhost"
        self.apiPort = int(kwargs["port"] if "port" in kwargs else "80")

    def onGet(self, resp):
        self.call.resp.read(resp)
        self.logger.debug("Request for URL (%s) returned response %d - %s", self.call.req.url, self.call.resp.status, self.call.resp.reason)
        self.callback(self.call)
        
    def get(self, resource, callback):
        self.call = NextAPICall(self.apiHost, self.apiPort, "GET", resource)
        self.callback = callback

        self.logger.debug("Requesting URL:  %s", self.call.req.url)
#        try:
        client = AsyncHTTPClient()
        client.fetch(self.call.req.url, callback=self.onGet)
#        except HTTPError as err:
#            self.call.resp.status = err.code
#            self.call.resp.reason = err.message
#            self.callback(self.call)
        

#    def getCollections(self):
#        conn = httplib.HTTPConnection(self.apiHost)
#        conn.request("GET", "/collections")
#
#        resp = conn.getresponse()
#        logging.debug("Request for collections returned response %d - %s\n", resp.status, resp.reason)
#
#        decoder = JSONDecoder()
#        body = decoder.decode(resp.read())
#        conn.close()
#        
#        collections = []
#        for collection in body['collections']:
#            logging.debug('found collection:  %s', collection['id'])
#            collections.append(NextAPICollection(collection))
#
#        return collections
#
#
#if __name__ == '__main__':
#    logging.basicConfig(
#        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#        datefmt='%Y-%m-%d %H:%M:%S',
#        level=logging.DEBUG)
#
#    api = NextAPICaller(host='alpha.api.reuters.com')
#    collections = api.getCollections()
#    for collection in collections:
#        logging.info('Found collection:  %s', collection)
    
