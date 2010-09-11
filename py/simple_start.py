'''
Created on 10 sept. 2010

@author: KaragNi
'''

from wsgiref.simple_server import make_server
from karacos.wsgi import App, Middleware

if __name__ == '__main__':
    app = App.Dispatcher()
    wrapped_app = Middleware.Middleware(app)
    server = make_server('localhost', 61080, wrapped_app)
    server.serve_forever()