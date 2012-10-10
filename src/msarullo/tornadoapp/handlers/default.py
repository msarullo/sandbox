'''
Created on Oct 2, 2012

@author: msarullo
'''

import logging
from tornado import web
from datetime import datetime

mainPage = """
<html>
  <head>
    <title>TestWebApp</title>
  </head>
  <body>
    <h1>Python Test Web Application</h1>
    <ul>
      <li><a href="/websockettest">Web Sockets Test</a></li>
      <li><a href="/nextapi">Next API</a></li>
    </ul>
    Time page was rendered:  {dteNow}
  </body>
</html>
"""

class DefaultHandler(web.RequestHandler):
    
    logger = logging.getLogger(__name__)

    def get(self, *args):
        self.logger.debug("Serving up default page.")
        self.write(mainPage.format(dteNow=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
