'''
Created on 10 sept. 2010

@author: KaragNi
'''
import karacos
import threading
from karacos.http import *

import Cookie
from uuid import uuid4

class Middleware(object):
    '''
    KaraCos Middleware
    provides KaraCos sessions
    '''
    def __init__(self, application):
        self.application = application
        self.log = karacos.core.log.getLogger(self)
    
    def __call__(self, environ, start_response):
        """
        """
        request = Request(environ)
        self.check_session(environ,request)
        
        response = self.application(environ, start_response)
        
        self.set_session(environ, response)
        
        return response(environ, start_response)
    
    def set_session(self,environ, response):    
        session_id = environ['karacos.session'].id
        response.set_cookie('karacos.session',session_id)

    def check_session(self,environ,request):
        """
        """
        session_id = ""
        try:
            cookie = Cookie.SimpleCookie(request.headers['cookie'])
            self.log.debug("COOKIE FOUND : [%s]" % cookie )
            assert 'karacos.session' in cookie  
            session_id = cookie['karacos.session'].value
            self.log.info("Found 'karacos.session' in cookie : %s" % session_id)
        except:
            session_id = "%s" % uuid4().hex
            self.log.info("Created 'karacos.session' in cookie : %s" % session_id)
        environ['karacos.session'] = Session(id=session_id)
    
    def authorized(self, header):
        if not header:
            return False
        auth_type, encoded = header.split(None, 1)
        print '%s' %  encoded.decode('base64')
        if not auth_type.lower() == 'basic':
            return False
        username, password = encoded.decode('base64').split(':', 1)
        return self.check_password(username, password)
    
    def check_password(self, username, password):
        print "checking password '%s' '%s'" % (username,password)
        result = username == password
        print result
        return result
    
    def auth_required(self, req):
        return Response(status=401, headers={'WWW-Authenticate': 'Basic realm="talm"'},
                         body="""\
         <html>
          <head><title>Authentication Required</title></head>
          <body>
           <h1>Authentication Required</h1>
           If you can't get in, then stay out.
          </body>
         </html>""")