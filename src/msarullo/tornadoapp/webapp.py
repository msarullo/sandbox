'''
Created on Oct 2, 2012

@author: msarullo
'''

import logging
from tornado import web
from msarullo.tornadoapp import webpaths

class TestWebApp(web.Application):

    def __init__(self):
        super(TestWebApp, self).__init__(webpaths.handlers)
        self.logger = logging.getLogger(__name__)

    def log_request(self, handler):
        """
        Logs HTTP request

        """
        self.logger.info(
                'HTTP Status: %d - Duration: %d  - URL: %s', 
                handler.get_status(),
                handler.request.request_time(),
                handler.request.full_url()
            )

