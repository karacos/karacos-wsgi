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
    
    def __call__(self, environ, start_response):
        # Gets KaraCos request/response objects.
        
        
        response = Response()
        response.body = "Mon appli"
        
        response.body = """ %s
        <form method="POST" action=".">
        <input type="text" name="a"/>
        <input type="submit" name="ok" value="ok"/>
        </form>
        """ % response.body
        return response
