'''
Created on 10 sept. 2010

@author: KaragNi
'''

from wsgiref.simple_server import make_server
from threading import Thread
import time, os

if __name__ == '__main__':
    class wsgiregserver(Thread):
        def __init__(self,server,port):
            os.environ['KC_SERVER_NAME'] = server
            from karacos.wsgi import App, Middleware
            Thread.__init__(self)
            app = App.Dispatcher()
            wrapped_app = Middleware.Middleware(app)
            self.server = make_server('0.0.0.0', port, wrapped_app)
        def run(self):
            self.server.serve_forever()
    
    wsgirefsrv = wsgiregserver('dev',61080)
    wsgirefsrv.start()