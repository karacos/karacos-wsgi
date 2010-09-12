'''
Created on 10 sept. 2010

@author: KaragNi
'''
import karacos
from karacos.http import *

import Cookie
from uuid import uuid4

class Dispatcher(object):
    '''
    KaraCos Application Entry point
    '''
    
    def __init__(self):
        self.log = karacos.core.log.getLogger(self)
    
    def __call__(self, environ, start_response):
        # Gets KaraCos request/response objects.
        
        self.check_session()
        response = karacos.serving.response
        response.body = "Mon appli"
        
        response.body = """ %s
        <form method="POST" action=".">
        <input type="text" name="a"/>
        <input type="submit" name="ok" value="ok"/>
        </form>
        """ % response.body
        return response

    def check_session(self):
       
        session = karacos.serving.get_session()
        if session != None:
            self.log.debug("session fould, HTTP detected...")
            
        else:
            self.log.debug("session NOT fould")