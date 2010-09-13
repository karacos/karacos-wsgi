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
    def __init__(self,*args,**kw):
        threading.local.__init__(self,*args,**kw)
        self.log = karacos.core.log.getLogger(self)
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
            if 'session' not in dir(karacos.serving):
                self.log.debug("session not found, getting session for 'system_thread'")
                # AT this point, if middleware didn't add session,
                # it's not a request, it-s a system thhread.
                session_id = 'system_thread'
                karacos.serving.session = Session(id=session_id)
                karacos.serving.session['username'] = "system"
            return karacos.serving.session