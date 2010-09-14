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
from karacos.lib import static

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
            request.__method__ = None
            request.__args_spec__ = None
            response = karacos.serving.get_response()
            response.__instance__ = None
            response.__result__ = None
            response.__action__ = None
            session = karacos.serving.get_session()
            domain = session.get_karacos_domain()
            resource = domain.lookup_resource(request.path) # Gives App the resource to process
            if 'staticfile' in resource:
                self.log.debug("serving static resource %s" % resource['staticfile'])
                static.serve_file(resource['staticfile'])
                return response
            self.process_resource(resource)
            self.process_request(request,response)
            if 'text/html' in request.accept or 'application/xhtml+xml' in request.accept:
                self.render_html(response)
            elif 'application/json' in request.accept:
                self.render_json(response)
            elif 'application/xml' in request.accept:
                self.render_xml(response)
            self.log.debug(request.path)
        
        except BaseException, e:
            self.log.log_exc(sys.exc_info(),'warn')
            self.process_error(e)
        
        return response
    
    def process_error(self,e):
        """
        Process error
        """
        response = karacos.serving.get_response()
        session = karacos.serving.get_session()
        domain = session.get_karacos_domain()
        template = domain.lookup.get_template('system') 
        if isinstance(e, HTTPError):
            response.body = template.render(instance = domain,
                                            result = {'status': 'failure',
                                                      'message': e.get_message()})
        else:
            response.body = template.render(instance = domain,
                                            result = {'status': 'failure',
                                                      'message': "%s,%s" % (e.args,sys.exc_info())})
    
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
        
    
    def process_http_params(self,request,response):
        """
        """
        method = ""
        for name, value in request.params.items():
            request.__kwds__[name] = value
        if 'method' in request.__kwds__:
            if request.__method__ != None:
                raise HTTPError(status=400, message="Bad request")
            else:
                method = "%s" % request.__kwds__['method']
                request.__method__ = response.__instance__.get_action(method)
                del request.__kwds__['method']
        else:
            if request.__method__ == None:
                if not (len(request.__kwds__) == 0 and len(request.__args__) == 0):
                    raise HTTPError(status=400, message="Bad request")
        if request.__method__ != None:
            self.process_method_params(request.__method__)
            self.ckeck_method_params(method, request)
        
    
    def process_json_params(self,request,response):
        """
        """
    def process_xml_params(self,request,response):
        """
        """
    def render_html(self, response):
        """
        """
        session = karacos.serving.get_session()
        domain = session.get_karacos_domain()
        template = domain.lookup.get_template('system') 
        
        response.body = template.render(instance = response.__instance__,
                                        result = response.__result__,
                                        action = response.__action__) 
        """<pre>
        response.__instance__ : %s 
        response.__action__   :%s
        response.__result__   : %s </pre>""" % (
                karacos.json.dumps(response.__instance__),
                karacos.json.dumps(response.__action__),
                karacos.json.dumps(response.__result__),
        )
        
        
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
        if request.__method__ == None:
            response.__result__ = response.__instance__.get_user_actions_forms()
        else:
            given = len(request.__args__) + len(request.__kwds__)
            
            if request.__args_spec__.args == ['self']:
                self.log.info("Method %s takes no arguments" % (request.__method__.func.__name__))
                if given != 0:
                    raise HTTPError(status=400, message="Bad request, no argument accepted for %s" % request.__method__.func.__name)
            if self.ckeck_method_params(request.__method__, request):
                response.__result__ = request.__method__(*request.__args__,**request.__kwds__)
            else:
                if given == 0:
                    response.__action__ = request.__method__.get_action(response.__instance__)
                else:
                    raise HTTPError(status=400, message="Bad request, invalid parameter number")
    
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
        self.log.debug("process_method_params BEGIN")
        request = karacos.serving.get_request()
        request.__method__ = method
        request.__args_spec__ = inspect.getargspec(method.func)
        self.log.debug("Parameters for method '%s' are '%s'" % (method.func.func_name,request.__args_spec__))
    
    def ckeck_method_params(self,method,request):
        """
        Check if correct parameters are passed to method
        """
        self.log.debug("check_method_params BEGIN")
        try:
            given = len(request.__args__) + len(request.__kwds__) + 1 # +1 stands for ungiven 'self' param
            expected = 0
            try:
                expected = len(request.__args_spec__.args)
            except:
                expected = 0
            defaults_expected = 0
            try:
                defaults_expected = len(request.__args_spec__.defaults)
            except:
                defaults_expected = 0
            assert given == expected, "Invalid number of parameter '%s', '%s' expected" % (given,len(request.__args_spec__))
            assert len(request.__kwds__) == defaults_expected, "Invalid number of named parameters"
            return True
        except AssertionError,e:
            self.log.log_exc(sys.exc_info(),'info')
            return False