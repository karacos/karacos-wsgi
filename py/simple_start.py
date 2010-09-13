'''
Created on 10 sept. 2010

@author: KaragNi
'''

from wsgiref.simple_server import make_server
from karacos.wsgi import App, Middleware
from threading import Thread
import time

if __name__ == '__main__':
    class wsgiregserver(Thread):
        def __init__(self):
            Thread.__init__(self)
            app = App.Dispatcher()
            wrapped_app = Middleware.Middleware(app)
            self.server = make_server('localhost', 61080, wrapped_app)
        def run(self):
            self.server.serve_forever()
    
    wsgirefsrv = wsgiregserver()
    wsgirefsrv.start()
    app = App.Dispatcher()
    while 1:
        #app.check_session()
        time.sleep(5)