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
    
    def get_karacos_domain(self):
        """
        Returns karacos domain for current session
        """
        if __domain__ not in dir(self):
            self.probe_domain()
            
    def probe_domain(self):
        """
        If no domain can be found, use sysdomain
        """
        if karacos.serving.get_request() == None:
            self.__domain__ = karacos.db['Domain'].get_by_name('sysdomain')
            