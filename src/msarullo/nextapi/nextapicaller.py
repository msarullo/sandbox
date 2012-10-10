'''
Created on Oct 9, 2012

@author: msarullo
'''

import httplib
from json import JSONDecoder
import logging
from nextapimodel import NextAPICollection

class NextAPICaller(object):

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.apiHost = kwargs["apiHost"]

    def getCollections(self):
        conn = httplib.HTTPConnection(self.apiHost)
        conn.request("GET", "/collections")

        resp = conn.getresponse()
        logging.debug("Request for collections returned response %d - %s\n", resp.status, resp.reason)

        decoder = JSONDecoder()
        body = decoder.decode(resp.read())
        conn.close()
        
        collections = []
        for collection in body['collections']:
            logging.debug('found collection:  %s', collection['id'])
            collections.append(NextAPICollection(collection))

        return collections


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)

    api = NextAPICaller(apiHost='alpha.api.reuters.com')
    collections = api.getCollections()
    for collection in collections:
        logging.info('Found collection:  %s', collection)
    
