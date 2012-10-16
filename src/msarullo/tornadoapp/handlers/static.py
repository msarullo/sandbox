'''
Created on Oct 11, 2012

@author: msarullo
'''

import logging
import os
from tornado import web


class StaticHandler(web.RequestHandler):
    
    logger = logging.getLogger(__name__)

    def initialize(self, **kwargs):
        self.htmlPath = os.path.abspath(os.path.dirname(__file__))
        self.pageName = kwargs['page']
        self.alwaysReload = kwargs['alwaysReload'] if 'alwaysReload' in kwargs else True
        self.mimeType = kwargs['mimeType'] if 'mimeType' in kwargs else 'text/html'
        if self.alwaysReload:
            self.page = open(os.path.join(self.htmlPath, self.pageName)).read()

    def get(self, *args):
        self.logger.debug("Serving up static page:  %s", self.pageName)
        self.set_header('Content-Type', self.mimeType)
        if self.alwaysReload:
            self.write(self.page)
        else:
            self.write(open(os.path.join(self.htmlPath, self.pageName)).read())
