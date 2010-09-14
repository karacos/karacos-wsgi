'''
Created on 10 sept. 2010

@author: KaragNi
'''
import karacos
from karacos.http import *

import Cookie
from uuid import uuid4
import webob
import inspect
import sys

class Dispatcher(object):
    '''
    KaraCos Application Entry point
    '''
    
    def __init__(self):
        self.log = karacos.core.log.getLogger(self)
    
    def __call__(self, environ, start_response):
        # Gets KaraCos request/response objects.
        try:
            request = karacos.serving.get_request()
            request.__args__ = []
            request.__kwds__ = {}
            response = karacos.serving.get_response()
            response.__method__ = None
            response.__instance__ = None
            response.__result__ = None
            response.__action__ = None
            session = karacos.serving.get_session()
            domain = session.get_karacos_domain()
            resource = domain.lookup_resource(request.path) # Gives App the resource to process
            self.process_resource(resource)
            self.process_request(request,response)
            
            #request = webob.Request(environ)
            #request.path()
            self.log.debug(request.path)
            """ %s
            
            "Bienvenue %s" % karacos.serving.get_session().get_user_auth()['name']
            
            response.unicode_body = 
            <form method="POST" action=".">
            <input type="text" name="a"/>
            <input type="submit" name="ok" value="ok"/>
            </form>
            % response.unicode_body"""
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'warn')
            self.process_error(e)
        return response
    
    def process_error(self,e):
        """
        Process error
        """
    
    def process_request(self,request,response):
        """
        """
        self.log.debug("process_request %s" % dir(request.params))
        self.log.debug(request.headers['Content-Type'])
        if request.headers['Content-Type'].find("application/json")<0:
            #c pas du json
            if request.headers['Content-Type'].find("application/xml")<0:
                self.process_http_params(request,response)
            else:
                if response.__result__ != None or response.__action__ != None:
                    raise HTTPError(status=400, message="Bad request")
                else:
                    self.process_xml_params(request,response)
        else:
            if response.__result__ != None or response.__action__ != None:
                raise HTTPError(status=400, message="Bad request")
            else:
                self.process_json_params(request,response)
        self.process_action(request, response)
        if 'text/html' in request.accept or 'application/xhtml+xml' in request.accept:
            response.__render_method__ = self.render_html
        elif 'application/json' in request.accept:
            response.__render_method__ = self.render_json
        elif 'application/xml' in request.accept:
            response.__render_method__ = self.render_xml
    
    def process_http_params(self,request,response):
        """
        """
        for name, value in request.params.items():
            request.__kwds__[name] = value
        if 'method' in request.__kwds__:
            if response.__method__ != None:
                raise HTTPError(status=400, message="Bad request")
            else:
                method = "%s" % request.__kwds__['method']
                del request.__kwds__['method']
                self.process_method_params(response.__instance__.get_action(method))
                self.ckeck_method_params(method, request, response)
                response.__result__ = response.__instance__.get_action(method)(*request.__args__,**request.__kwds__)

    
    def process_json_params(self,request,response):
        """
        """
    def process_xml_params(self,request,response):
        """
        """
    def render_html(self, response):
        """
        """
    def render_json(self, response):
        """
        """
        
    def render_xml(self,response):
        """
        """
    def check_session(self):
       
        session = karacos.serving.get_session()
        self.log.debug("session fould, [%s] " % session)
    
    def process_action(self,request, response):
        """
        Process actionMethod for getting some result
        """
        if response.__method__ == None:
            response.__result__ = response.__instance__.get_user_actions_forms()
        else:
            if response.__args_spec__.args == ['self']:
                self.log.info("Method %s takes no arguments" % (response.__method__.func.__name))
                assert request.__kwds__ == [] and request.__args__ == [], "No argument accepted for %s" % response.__method__.func.__name
    
    def process_resource(self,resource):
        """
        Process resource
        """
        self.log.debug("process_resource_html START")
        response = karacos.serving.get_response()
        request = karacos.serving.get_request()
        response.__instance__ = resource['object']
        if 'args' in resource:
            request.__args__ = resource['args']    
        if 'method' not in resource.keys():
            self.log.debug("Resource is only instance")
        else:
            self.process_method_params(resource['method'])
            
    def process_method_params(self,method):
        response = karacos.serving.get_response()
        request = karacos.serving.get_request()
        request.__method__ = method
        request.__args_spec__ = inspect.getargspec(method.func)
        self.log.debug("Parameters for method '%s' are '%s'" % (method.func.func_name,request.__args_spec__))
    
    def ckeck_method_params(self,method,request):
        """
        """
        given = len(request.__args__) + len(request.__kwds__)
        assert given == len(request.__args_spec__), "Invalid number of parameter '%s', '%s' expected" % (given,len(request.__args_spec__))
        assert len(request.__kwds__) == len(request.__args_spec__.defaults), "Invalid number of named parameters"