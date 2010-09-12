from Request import Request
from Response import Response
from Session import Session
import threading

import karacos

class Redirect(karacos.core.Exception):
    """
    HTTP redirect Exception
    """
    def __init__(self,url,code=302):
        """
        """

class HTTPError(karacos.core.Exception):
    """
    """
    def __init__(self,status=500,message=""):
        """
        """
    
def isaction(func):
    """
    Decorator for object exposed actions
    """
      
class _Serving(threading.local):
    """
    Class for served objects
    """
    
    def set_request(self,request):
        if 'serving' in dir(karacos):
            karacos.serving.request = request
    
    def get_request(self):
        if 'serving' in dir(karacos):
            if 'request' in dir(karacos.serving):
                return karacos.serving.request

    def set_response(self,response):
        if 'serving' in dir(karacos):
            karacos.serving.response = response

    def get_response(self):
        if 'serving' in dir(karacos):
            if 'response' in dir(karacos.serving):
                return karacos.serving.response

    def set_session(self,session):
        if 'serving' in dir(karacos):
            karacos.serving.session = session
            
    
    def get_session(self):
        """
        """
        if 'serving' in dir(karacos):
            if 'session' in dir(karacos.serving):
                return karacos.serving.session