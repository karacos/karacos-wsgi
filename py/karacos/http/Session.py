'''
Created on 10 sept. 2010

@author: nico
'''
import karacos
import sys
import os

class SessionMeta(type):
    
    
    def __init__(self,*args, **kw):
        """
        """
        self.sessions = dict()
        self.log = karacos.core.log.getLogger(self)
        self.filedir = os.path.join(karacos._srvdir,'temp',self.__name__)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
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
        if os.path.exists(instance.filename):
            file = open(instance.filename,"r")
            data = karacos.json.loads(file.read())
            file.close()
            instance.update(data)
        else:
            file = open(instance.filename,"w")
            file.write(karacos.json.dumps(instance,skipkeys=True))
            file.flush()
            file.close()
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
        self.id = id
        self.log = karacos.core.log.getLogger(self)
        self.filename = os.path.join(self.filedir,"%s" % id)
        self['username'] = 'anonymous'
        self['backlinks'] = []
        self.log.debug("NEW SESSION CREATED '%s'" % self.id)
    
    def __getitem__(self, key):
        file = open(self.filename,"r")
        data = karacos.json.loads(file.read())
        file.close()
        self.update(data)
        return dict.__getitem__(self,key)
    
    def __setitem__(self, key, item):
        ""
        dict.__setitem__(self,key,item)
        file = open(self.filename,"w")
        file.write(karacos.json.dumps(self,skipkeys=True))
        file.flush()
        file.close()
    
    def __delitem__(self, key):
        ""
        dict.__delitem__(self, key)
        file = open(self.filename,"w")
        file.write(karacos.json.dumps(self,skipkeys=True))
        file.flush()
        file.close()
    
    def set_user(self,user):
        self.log.debug("set_user %s" % user)
        assert isinstance(user, karacos.db['User'])
        self.user = user
        self['username'] = self.user['name']
        if 'codlang' in self.user:
            self['codlang'] = self.user['codlang']
    
    
    def get_session_lang(self):
        try:
            if 'codlang' not in self:
                domain = self.get_karacos_domain()
                request = karacos.serving.get_request()
                langs = request.accept_language.best_matches(domain.get_default_site_language())
                for lang in langs:
                    lang = "%s%s" % (lang[0:2].lower(), lang[2:len(lang)+1].upper())
                    if lang in domain.get_supported_site_languages():
                        self['codlang'] = lang
                        break
        except:
            self.log.log_exc(sys.exc_info(),'error')
        if 'codlang' not in self:
            self['codlang'] = domain.get_default_site_language()
        return self['codlang']
    
    def set_session_lang(self, lang):
        domain = self.get_karacos_domain()
        assert lang in domain.get_supported_site_languages(), "This language is not supported"
        self['codlang'] = lang
    
    def get_user_auth(self):
        """
        Returns user auth for current session
        """
        domain = self.get_karacos_domain()
        result = None
        if 'user' in dir(self):
            if self.user != None:
                return self.user
        if self['username'] == 'anonymous':
            result = domain._get_anonymous_user()
        else:
            result = domain.get_user_by_name(self['username'])
            self.user = result
        self.log.debug("result type '%s', data [%s]" % (result.__class__.__name__, result))
        return result
    
    def invalidate(self):
        """
        Invalidate session
        """
        self.user = None
        for k in self.keys():
            del self[k]
        self['username'] = 'anonymous'
        self['backlinks'] = []
    
    def authenticate(self,username,password):
        assert self['username'] == 'anonymous'
        try:
            passwordhash = "%s" % karacos.db['User'].hash_pwd(password)
            user = self.get_karacos_domain().get_user_by_name(username)
            assert user != None, _("User not found in domain")
            if user['password'] == passwordhash:
                self.set_user(user)
                return user
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        raise karacos.core.Exception("Authentication error")
        
    
    def is_authenticated(self):
        if self['username'] == 'anonymous':
            return False
        return True
    
    def get_karacos_domain(self):
        """
        Returns karacos domain for current session
        """
        if '__domain__' not in dir(self):
            self.probe_domain()
        request = karacos.serving.get_request()
        if request.headers['Host'] != self.__domain__['fqdn']:
            if 'fqdn_aliases' in self.__domain__:
                if request.headers['Host'] in self.__domain__['fqdn_aliases']:
                    return self.__domain__    
            self.probe_domain()
            if request.headers['Host'] == self.__domain__['fqdn']:
                self.log.info("probe domain changed current kc domain, resetting auth")
                self.user = None
                self['username'] = 'anonymous'
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