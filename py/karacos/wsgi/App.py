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
            response = karacos.serving.get_response()
            session = karacos.serving.get_session()
            domain = session.get_karacos_domain()
            template = domain.lookup.get_template("system")
            request = karacos.serving.get_request()
            resource = domain.lookup_resource(request.path) # Gives App the resource to process
            self.process_resource_html(resource)
            
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
        
    
    def check_session(self):
       
        session = karacos.serving.get_session()
        self.log.debug("session fould, [%s] " % session)
        
    def process_resource_html(self,resource):
        """
        Process resource
        """
        self.log.debug("process_resource_html START")
        response = karacos.serving.get_response()
        session = karacos.serving.get_session()
        domain = session.get_karacos_domain()
        template = domain.lookup.get_template("system")
        if 'method' not in resource.keys():
            self.log.debug("Resource is only instance, generating template output")
            #response.body = template.render(instance=resource['object'])
        else:
            self.log.debug("Lookup returned instance '%s' and method '%s'" % (resource['object']['name'],resource['method'].func.func_name))
            result = self.process_resource_method(resource)
            
            #response.body = template.render(instance=resource['object'])
    
    def process_resource_method(self,resource):
        result = {}
        assert 'method' in resource.keys(), _("Can't process resource_method with no method")
        args_spec = inspect.getargspec(resource['method'].func)
        self.log.debug("Parameters for method '%s' are '%s'" % (resource['method'].func.func_name,args_spec))
        self.log.debug("%s"%dir(args_spec))
        if args_spec.args == ['self']:
            self.log.debug("Instance method with no parameters, running method and returning result")
            resource['method'](resource['object'])
        else:
            self.log.debug("Found more than 'self' parameter in method")
            