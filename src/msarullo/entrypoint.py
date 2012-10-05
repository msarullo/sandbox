'''
Created on Oct 2, 2012

@author: msarullo
'''
import logging
import sys
from msarullo.tornadoapp.webapp import TestWebApp
from msarullo.utils.contentgen import getContentGenerator
from tornado import ioloop, httpserver

logger = logging.getLogger(__name__)
port = 1313
contentGenerator = None

def main():
    print('Starting server, see test-server.log for further information.')

    # configure logging
    logging.basicConfig(
        filename='test-server.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)

    # also output log messages to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    logger.info('Started')

    startContentGenerator()
    startHttpServer()

    # keep the server alive until killed
    loop = ioloop.IOLoop.instance()

    logger.info('Server running on port %d, Hit <CTRL-C> to stop', port)

    # used for graceful exit
    try:
        loop.start()
    except KeyboardInterrupt:
        stopContentGenerator()
        logger.info('Finished')
        print 'Exiting server'
        sys.exit(0)


def startHttpServer():
    logger.info('Starting Tornado...')
    http_server = httpserver.HTTPServer(TestWebApp())
    http_server.listen(port)
    
    
def startContentGenerator():
    logger.info('Starting Content Generator...')
    getContentGenerator().start()


def stopContentGenerator():
    logger.info('Stopping Content Generator...')
    getContentGenerator().gracefulStop()


if __name__ == '__main__':
    main()

