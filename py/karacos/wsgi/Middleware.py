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
        """
        Initialize application
        """
        self.application = application
        self.log = karacos.core.log.getLogger(self)
        if not karacos.db['Domain'].exist_with_name('sysdomain'):
            db_name = "kc2_sysdomain_%s" % uuid4().hex
            base = karacos.db['Base'].create(db_name)
            karacos.db['Domain'].create(data={'name':'sysdomain', 'fqdn': 'localhost:61080'}, base=base)
    
    def __call__(self, environ, start_response):
        """
        """
#        karacos.serving = karacos.http._Serving()
        karacos.serving.set_request(Request(environ))
        karacos.serving.set_response(Response())
        self.check_session(environ)
        
        self.application(environ, start_response)
        
        return karacos.serving.response(environ, start_response)

    def check_session(self,environ):
        """
        """
        session_id = ""
        try:
            cookie = Cookie.SimpleCookie(karacos.serving.request.headers['cookie'])
            self.log.debug("COOKIE FOUND : [%s]" % cookie )
            assert 'karacos.session' in cookie  
            session_id = cookie['karacos.session'].value
            self.log.info("Found 'karacos.session' in cookie : %s" % session_id)
        except:
            session_id = "%s" % uuid4().hex
            self.log.info("Created 'karacos.session' in cookie : %s" % session_id)
        Session(id=session_id) # instanciate session, sets session in karacos.serving
        karacos.serving.response.set_cookie('karacos.session',karacos.serving.session.id)