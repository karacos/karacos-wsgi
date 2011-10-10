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
import sys, traceback
from karacos.lib import static
from karacos.http.jsonrpc import *
import cStringIO
from io import StringIO
import exceptions

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
            response.__headers_type_set__ = False
            self.log.debug("Response object has body '%s'" % response.body)
            session = karacos.serving.get_session()
            domain = session.get_karacos_domain()
            resource = domain.lookup_resource(request.path) # Gives App the resource to process
            if 'staticfile' in resource:
                self.log.debug("serving static resource %s" % resource['staticfile'])
                static.serve_file(resource['staticfile'])
                return response
            self.process_resource(resource)
            self.process_request(request,response)
            self.render(request, response)
            self.log.debug(request.path)
        
        except BaseException, e:
            self.log.log_exc(sys.exc_info(),'warn')
            self.process_error(e,sys.exc_info())
        
        return response
    def render(self,request, response):
        session = karacos.serving.get_session()
        self.log.debug("RENDER : Response object has body '%s'" % response.body[:200])
        #if response.__action__ == None:
        self.log.info("Checking backlinks %s" % session['backlinks'])
        try:
            if len(session['backlinks']) > 0:
                blid = len(session['backlinks']) -1
                forward = session['backlinks'][blid][0]
                instid = session['backlinks'][blid][1]
                method = session['backlinks'][blid][2]
                self.log.debug("Backlink : %s" % session['backlinks'][blid])
                argslen = len(request.__args__) + len(request.__kwds__)
                if argslen > 0:
                    assert str(request.__method__.func.func_name) == str(method) and str(response.__instance__.id) == str(instid)
                    self.log.info("Processing backlink %s" % forward)
                    backlinks = session['backlinks']
                    del backlinks[blid]
                    session['backlinks'] = backlinks
                    raise Redirect(forward, 302, _("Action processing redirect backlink"))
        except exceptions.AssertionError:
            self.log.info("Exception while processing forward, continuing")
        if response.body == '':
            try:
                if (request.headers['Accept'].find('text/html') >= 0 or
                    request.headers['Accept'].find('application/xhtml+xml') >= 0):
                    self.render_html(response)
                elif request.headers['Accept'].find('application/json') >= 0 :
                    self.render_json(response)
                elif request.headers['Accept'].find('application/xml') >= 0:
                    self.render_xml(response)
                else:
                    self.render_html(response)
            except:
                self.render_html(response)

    def process_error(self,e,exc_info):
        """
        Process error
        """
        exceptionType, exceptionValue,exceptionTraceback = exc_info
        response = karacos.serving.get_response()
        request = karacos.serving.get_request()
        session = karacos.serving.get_session()
        domain = session.get_karacos_domain()
        template = domain.lookup.get_template('system') 
        if isinstance(e, HTTPError):
            response.status = e.status
            response.body = template.render(instance = domain,
                                            result = {'status': 'failure',
                                                      'message': e.get_message()})
            if isinstance(e, Redirect):
                response.headers['Location'] = '%s' % e.location
                for k in response.headers.keys():
                    response.headers[k] = '%s' % response.headers[k]
            if isinstance(e,DataRequired):
                response.body = template.render(instance = e.instance,
                                                result = None,
                                                action = e.method.get_action(e.instance))
                if e.backlink != None:
                    backlinks = session['backlinks']
                    backlink = (e.backlink,e.instance.id,e.method.func.func_name)
                    backlinks.append(backlink)
                    session['backlinks'] = backlinks
                    self.log.info("Setting backlinks : %s" % session['backlinks'] )
        else:
            if (request.headers['Accept'].find('text/html') >= 0 or
                request.headers['Accept'].find('application/xhtml+xml') >= 0):
                    response.body = template.render(instance = domain,
                                            result = {'status': 'failure',
                                                      'message': exceptionValue,
                                                      'data' : "%s,%s,%s" % (exceptionType, exceptionValue,traceback.format_tb(exceptionTraceback))})
            elif request.headers['Accept'].find('application/json') >= 0 :
                response.body = karacos.json.dumps({'status': 'failure',
                                                      'message': "%s" % exceptionValue,
                                                      'data' : "%s,%s,%s" % (exceptionType, exceptionValue,traceback.format_tb(exceptionTraceback))})
            elif request.headers['Accept'].find('application/xml') >= 0:
                ""#self.render_xml(response)
            else:
                response.body = template.render(instance = domain,
                                            result = {'status': 'failure',
                                                      'message': "%s" % exceptionValue,
                                                      'data' : "%s,%s,%s" % (exceptionType, exceptionValue,traceback.format_tb(exceptionTraceback))})
    
    def process_request(self,request,response):
        """
        """
        self.log.debug("process_request %s" % dir(request.params))
        #self.log.debug(request.headers['Content-Type'])
        if 'Accept' in request.headers:
            # If post with type != application/json, application/xml, ou multipart/form-data,
            # then it's a file upload.
            if (request.method == "POST" and            # 
                'X-File-Name' in request.headers ) :
                self.process_file_upload(request,response)
            elif (request.headers['Accept'].find('text/html') >= 0 or
                    request.headers['Accept'].find('application/xhtml+xml') >= 0):
                self.process_http_params(request,response)
            elif request.headers['Accept'].find('application/json') >= 0:
                self.process_json_params(request,response)
            elif request.headers['Accept'].find('application/xml') >= 0:
                self.process_xml_params(request,response)
            else:
                self.process_http_params(request,response)
            self.process_action(request, response)
        else:
            self.process_http_params(request,response)
            self.process_action(request, response)
        
    def process_file_upload(self,request,response):
        self.log.info("Processing direct file upload")
        assert request.__method__ == None
        assert response.__instance__ != None
        assert 'X-File-Name' in request.headers
        assert 'Content-Type' in request.headers
        if 'add_attachment' not in response.__instance__._get_actions():
            raise HTTPError(404, "Upload unavailable here")
        request.__method__ = response.__instance__.get_action('add_attachment')
        base64 = False
        if request.headers['Content-Type'].find('base64') >= 0:
            base64 = True
        content_type = request.headers['Content-Type']
        if request.headers['Content-Type'].find(';') >=0:
            content_type = request.headers['Content-Type'].split(';')[0]
        file_param = karacos.container()
        file_param.filename = request.headers['X-File-Name']
        if base64 and request.body.startswith('data'):
            file_param.file_body = request.body[len("data:%s;base64," % content_type): ]
        else:
            file_param.file_body = request.body
        #self.log.warn("%s" % file_param.file_body)
        request.__kwds__ = {'att_file':file_param,
                            'base64':base64,
                            'content_type': content_type
                            }
        self.process_method_params(request.__method__)
        self.ckeck_method_params('add_attachment', request)
        
        
    def process_http_params(self,request,response):
        """
        """
        self.log.debug("process_http_params START")
        method = ""
        for name, value in request.params.items():
            request.__kwds__[str(name)] = value
        if 'method' in request.__kwds__:
            if request.__method__ != None:
                raise HTTPError(status=400, message="Bad request, method found before !")
            else:
                method = "%s" % request.__kwds__['method']
                request.__method__ = response.__instance__.get_action(method)
                del request.__kwds__['method']
        if '_' in request.__kwds__:
            del request.__kwds__['_']
        else:
            if request.__method__ == None:
                if not (len(request.__kwds__) == 0 and len(request.__args__) == 0):
                    raise HTTPError(status=400, message="Bad request, args without method")
        if request.__method__ != None:
            self.process_method_params(request.__method__)
            self.ckeck_method_params(method, request)
        
    
    def process_json_params(self,request,response):
        """
        """
        data = None
        #body = ''
        #self.log.debug("request environ [%s]" % request.body_file)
        #if isinstance(request.body_file, socket._fileobject):
        #    self.log.debug("request body is cStringIO")
        body = request.body
        self.log.debug("process_json_params START with body [%s]" % body)
        try:
            if (body != None and
                '%s' % body != ''):
                self.log.debug("process_json_params decoding json with body [%s]" % body)
                data = karacos.json.loads(body)
            else:
                if request.method == 'GET':
                    return
                response.__result__ = dict(error = {
                    'origin': ErrorOrigin.Server, 
                    'code' : ErrorCode.ParameterMismatch,
                    'message': 'Error empty request body'
                })
                return
        except ValueError, e:
            response.__result__ = dict(error = {
                'origin': ErrorOrigin.Server, 
                'code' : ErrorCode.IllegalService,
                'message': 'Error decoding JSON request: %s' % e
            })
            return
        #return self.process_json(response.__instance__,d) 
        keys = data.keys()
            
        for required_key in ('id', 'method','params'):
            if not required_key in keys:
                response.__result__ = dict(error = {
                    'origin': ErrorOrigin.Server, 
                    'code' : ErrorCode.ParameterMismatch,
                    'message': 'Request does not contain %s!' % required_key
                })
                return # self._get_json_response(error = err, id=0)
        # TODO: RPC id request...
        # READ json-rpc carefully and correct implementation
        rpcid = data['id']
        self.log.info("Processing JSON for method %s" % data['method'])
        
        try:
            if isinstance(data['params'],dict):
                for k in data['params'].keys():
                    request.__kwds__[str(k)] =  data['params'][k] # set keys to str instead of unicode

            elif isinstance(data['params'],list):
                
                if len(data['params']) > 0 and isinstance(data['params'][-1],dict):
                    request.__kwds__ = data['params'][-1]
                    del data['params'][-1]
                request.__args__ = tuple(data['params'])
            rpcmethod = str(data['method']) #json returns unicode
            if rpcmethod in response.__instance__.get_user_actions(response.__instance__.__domain__.get_user_auth()):
                request.__method__ = response.__instance__.get_action(rpcmethod)
                self.process_method_params(request.__method__)
                self.ckeck_method_params(rpcmethod, request)
                return
            else:
                if rpcmethod in response.__instance__.get_actions():
                    response.__result__ = dict(error =  {
                        'origin': ErrorOrigin.Application, 
                        'code' : ErrorCode.PermissionDenied,
                        'message': 'Permisison denied, method |%s| is not allowed' % rpcmethod,
                        'trace': traceback.format_exc().splitlines()
                    })
                    return # self._get_json_response(error = err, id = rpcid)
                else:
                    response.__result__ = dict(error = {
                        'origin': ErrorOrigin.Server, 
                        'code' : ErrorCode.MethodNotFound,
                        'message': 'Method |%s| not found' % rpcmethod,
                        'trace': traceback.format_exc().splitlines()
                    })
                    return
        except Exception, e:
            #something else went wrong - application error
            response.__result__ = dict(error = {
                'origin': ErrorOrigin.Application, 
                'code' : ErrorCode.Unknown,
                'message': 'Error processing JSON request: %s' % e,
                'trace': traceback.format_exc().splitlines()
            })
            return #self._get_json_response(error = err, id = rpcid)
        
    def process_xml_params(self,request,response):
        """
        """
    def render_html(self, response):
        """
        """
        session = karacos.serving.get_session()
        domain = session.get_karacos_domain()
        template = domain.lookup.get_template('system')
        response.headers['Content-Type'] = 'text/html'
        response.body = template.render(instance = response.__instance__,
                                        result = response.__result__,
                                        action = response.__action__)
    
    
    def render_json(self, response):
        """
        """
        self.log.debug("render_json START")
        body = None
        if response.__result__ == None and response.__action__ != None :
            body = karacos.json.dumps(response.__action__)
        if response.__result__ != None and response.__action__ == None :
            try:
                body = karacos.json.dumps(response.__result__)
            except:
                body = karacos.json.dumps({'success': False, 'error': 'Error serializing json Response', 'errorData':traceback.format_exc().splitlines(), 'errorMessage': str(response.__result__)})
        if body == None:
            body = karacos.json.dumps({"status": "success",'success': True, "message":"Empty method result"})
        response.body = body
        if not response.__headers_type_set__:
            response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Length'] = "%s" % len(body)
        
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
        if response.__result__ != None:
            # Nothing to process, result already exist
            return
        if request.__method__ == None:
            response.__result__ = {"success": True, "data": {
                        "id": response.__instance__.id,
                        "base_id":response.__instance__['base_id']
                    }}
        else:
            given = len(request.__args__) + len(request.__kwds__)
            
            if (request.__args_spec__.args == ['self']
                and request.__args_spec__.varargs == None
                and request.__args_spec__.keywords == None):
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
        self.log.debug("process_resource START")
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
            if (request.__args_spec__.varargs != None
                 or request.__args_spec__.keywords != None):
                expected += 1
            assert given >= expected, "Invalid number of parameter '%s', '%s' expected" % (given,len(request.__args_spec__))
            if (request.__args_spec__.varargs == None
                 and request.__args_spec__.keywords == None):
                assert len(request.__kwds__) == defaults_expected, "Invalid number of named parameters"
            return True
        except AssertionError,e:
            self.log.log_exc(sys.exc_info(),'debug')
            return False