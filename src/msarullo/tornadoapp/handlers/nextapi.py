'''
Created on Oct 9, 2012

@author: msarullo
'''

import logging
from msarullo.nextapi.nextapicaller import NextAPICaller
from tornado import web


class NextAPIQueryHandler(web.RequestHandler):

    logger = logging.getLogger(__name__)
    
    def onApiCallComplete(self, result):
        self.write(str(result))
        self.finish()


    @web.asynchronous
    def get(self, *args):
        self.logger.debug("Requested next api query with:  %s", self.request.query)

        apiCaller = NextAPICaller(host=self.get_argument("host"), port=self.get_argument("port"))
        apiCaller.get(self.get_argument("resource"), self.onApiCallComplete)
