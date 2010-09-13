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
            response = karacos.serving.get_response()
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
        request.__kwds__ = {}
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
        if 'text/html' in request.accept or 'application/xhtml+xml' in request.accept:
            request.__render_method__ = self.render_html
        elif 'application/json' in request.accept:
            request.__render_method__ = self.render_json
        elif 'application/xml' in request.accept:
            request.__render_method__ = self.render_xml
    
    def process_http_params(self,request,response):
        """
        """
        for name, value in request.params.items():
            request.__kwds__[name] = value
        if 'method' in request.__kwds__:
            if response.__result__ != None or response.__action__ != None:
                raise HTTPError(status=400, message="Bad request")
            else:
                method = "%s" % request.__kwds__['method']
                del request.__kwds__['method']
                response.__result__ = response.__instance__.get_action(method)(*(),**request.__kwds__)
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
        
    def process_resource(self,resource):
        """
        Process resource
        """
        self.log.debug("process_resource_html START")
        response = karacos.serving.get_response()
        request = karacos.serving.get_request()
        request.args = None
        response.__instance__ = resource['object']
        if 'args' in resource:
            request.__args__ = resource['args']    
        if 'method' not in resource.keys():
            self.log.debug("Resource is only instance")
        else:
            self.log.debug("Lookup returned instance '%s' and method '%s'" % (resource['object']['name'],resource['method'].func.func_name))
            self.process_resource_method(resource)
            #response.body = template.render(instance=resource['object'])
    
    def process_resource_method(self,resource):
        response = karacos.serving.get_response()
        assert 'method' in resource.keys(), _("Can't process resource_method with no method")
        args_spec = inspect.getargspec(resource['method'].func)
        self.log.debug("Parameters for method '%s' are '%s'" % (resource['method'].func.func_name,args_spec))
        if args_spec.args == ['self']:
            self.log.debug("Instance method with no parameters, running method and returning result")
            response.__result__ = resource['method'](resource['object'])
        else:
            self.log.debug("Found more than 'self' parameter in method")            