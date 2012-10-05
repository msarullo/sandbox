'''
Created on Oct 2, 2012

@author: msarullo
'''

import logging
from msarullo.utils.contentgen import getContentGenerator, ContentGenerationListener
from tornado import web, websocket
from datetime import datetime

mainPage = """
<html>
  <head>
    <title>TestWebApp</title>
    <script type="text/javascript">
    <!--
      var myWebSocketURL = 'ws://localhost:1313/websocket';
      var myWebSocket;
      
      function handleWebSocketMessage(msg) {{
        $(myWebSocketTime).html(msg);
      }}
      
      function initializeWebSocket() {{
        myWebSocket = new WebSocket(myWebSocketURL);
        myWebSocket.onmessage = handleWebSocketMessage;
      }}
    // -->
    </script>
  </head>
  <body onload="initializeWebSocket()">
    Hello from the TestWebApp!
    <br/><br/>
    Time page was rendered:  {dteNow}
    <br/><br/>
    Time from web socket:  <span id="myWebSocketTime" />
  </body>
</html>
"""

class WebSocketHandler(websocket.WebSocketHandler, ContentGenerationListener):
    
    logger = logging.getLogger(__name__)

    def open(self):
        getContentGenerator().addListener(self)

    def onGeneration(self, msg):
        self.logger.info('Received message:  %s', msg)
        self.write_message(msg)

    def close(self):
        getContentGenerator().dropListener(self)
        super(WebSocketHandler, self).close()


class DefaultHandler(web.RequestHandler):
    
    logger = logging.getLogger(__name__)

    def get(self, *args):
        self.logger.debug("Serving up default page.")
        self.write(mainPage.format(dteNow=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
