'''
Created on 10 sept. 2010

@author: nico
'''
import karacos

class SessionMeta(type):
    
    
    def __init__(self,*args, **kw):
        """
        """
        self.sessions = dict()
        self.log = karacos.core.log.getLogger(self)
        self.log.info("Created type '%s.%s' and sessions container" % (self.__module__,self.__name__))
        
    def __call__(self,*args, **kw):
        #instance = type.__call__(self,*args, **kw)
        """
        """
        assert 'id' in kw
        instance = None
        session_id = "%s" % kw['id']
        self.log.debug("sessions in type '%s.%s' : [%s] " % (self.__module__,self.__name__,self.sessions) )
        if kw['id'] in self.sessions.keys():
            self.log.debug("Session FOUND '%s'" % session_id )
            instance = self.sessions[session_id]
        else:
            self.log.debug("Session NOT FOUND '%s'" % session_id)
            instance = type.__call__(self,*args, **kw)
            self.sessions[session_id] = instance
        if 'serving' in dir(karacos):
            self.log.debug("karacos.serving object found")
            karacos.serving.set_session(instance)
        return instance        


class Session(dict):
    '''
    Session object
    '''
    
    __metaclass__ = SessionMeta

    def __init__(self, id=None):
        '''
        Constructor
        '''
        assert id != None
        dict.__init__(self)
        self['username'] = 'anonymous'
        self.id = id
        self.log = karacos.core.log.getLogger(self)
        self.log.debug("NEW SESSION CREATED '%s'" % self.id)
    
    def get_user_auth(self):
        """
        Returns user auth for current session
        """
        domain = self.get_karacos_domain()
        result = None
        if self['username'] == 'anonymous':
            result = domain._get_anonymous_user()
        else:
            result = domain.get_user_by_name(self['username'])
        self.log.debug("result type '%s', data [%s]" % (result.__class__.__name__, result))
        return result
        
    
    def get_karacos_domain(self):
        """
        Returns karacos domain for current session
        """
        if '__domain__' not in dir(self):
            self.probe_domain()
        return self.__domain__
            
    def probe_domain(self):
        """
        If no domain can be found, use sysdomain
        """
        if karacos.serving.get_request() == None:
            assert self.id == 'system_thread', _("Not in HTTP, session should be 'system_thread'")
            self.__domain__ = karacos.db['Domain'].get_by_name('sysdomain')
        else:
            request = karacos.serving.get_request()
            self.log.debug("Probing domain from request [%s]" % request)
            requested_fqdn = request.headers['Host']
            self.log.debug("Requesting domain '%s' in sysdb" % requested_fqdn)
            if karacos.db['Domain'].exist_with_fqdn(requested_fqdn):
                self.__domain__ = karacos.db['Domain'].get_by_fqdn(requested_fqdn)
            else:
                self.log.debug("Domain with fqdn '%s' not found in sysdb, using sysdomain" % requested_fqdn)
                self.__domain__ = karacos.db['Domain'].get_by_name('sysdomain')