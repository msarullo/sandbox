'''
Created on Oct 9, 2012

@author: msarullo
'''

import logging
import os
from datetime import datetime
from tornado import web


class NextAPIHandler(web.RequestHandler):
    
    logger = logging.getLogger(__name__)
    htmlPath = os.path.abspath(os.path.dirname(__file__))
    mainPage = open(os.path.join(htmlPath, 'nextapi.html')).read()

    def get(self, *args):
        self.logger.debug("Serving up default page.")
        self.write(self.mainPage.format(dteNow=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
