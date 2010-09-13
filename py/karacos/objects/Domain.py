'''
    This file is part of KaraCos.
    
    KaraCos is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    KaraCos - web platform engine - http://karacos.org/
    Copyright (C) 2009-2010  Nicolas Karageuzian - Cyril Gratecos

Created on 28 nov. 2009

@author: nico
'''
from logging import getLogger
log = getLogger(__name__)
from mako.template import Template
from uuid import uuid4
import os, datetime, sys, traceback
import karacos

KcDocument = karacos.db['Document']
class Domain(karacos.db['Parent']):
    """
    Domain Descriptor - 
    attribute db holds reference to the physical object DB
    'data' contains :
     * name (String Mandatory) - name of db in system
     * title (String optional)
     * description (String optional)
    """
    default_data = { 'name': None,
                     'title': None,
                     'description':None,
                     'fqdn': None
                       }
    __metaclass__ = karacos.db['WebMeta']
    authdoc = None
    
    @staticmethod
    def get_by_id(id):
        """
        """
        raise self.Exception, "Not implemented yet"
    
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_domains_list(name):
        """
        function(doc) { // %s
         if (doc.type == "Domain" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc.name);
        }
        """
    
    @staticmethod
    def get_domains_list():
        return Domain._get_domains_list('alors')
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_by_name(name):
        """
        function(doc) {
         if (doc.type == "Domain" && doc.name == "%s" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc);
        }
        """
    
    @staticmethod
    def get_by_name(name=None):
        log.debug("BEGIN Domain.get_by_name : %s" % name)
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        try:
            domains = Domain._get_by_name(name)
            assert domains.__len__() <= 1, "Domain.get_by_name : More than one Domain with that name in system DB"
            if domains.__len__() == 1:
                for domain in domains:
                    log.debug("Domain.get_by_name : db.key = %s db.value = %s" % (domain.key,domain.value) )
                    result = karacos.db.sysdb[domain.key]
        except Exception, e:
            print sys.exc_info()
            log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_by_fqdn(name):
        '''
            function(doc) {
            if (doc.type == "Domain" && doc.fqdn == "%s" && !("_deleted" in doc && doc._deleted == True))
              emit(doc._id, doc.name);
        }
        '''
    
    @staticmethod
    def get_by_fqdn(fqdn=None):
        """
        """
        log.debug("BEGIN Domain.get_by_fqdn : %s" % fqdn)
        assert isinstance(fqdn,basestring), "Parameter name must be string"
        result = None
        try:
            domains = Domain._get_by_fqdn(fqdn)
            assert domains.__len__() <= 1, "Domain.get_by_fqdn : More than one Domain with that name in system DB"
            if domains.__len__() == 1:
                for domain in domains:
                    log.debug("Domain.get_by_fqdn : db.key = %s db.value = %s" % (domain.key,domain.value) )
                    result = karacos.db.sysdb[domain.key]
        except Exception, e:
            log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result
    
    @staticmethod
    def exist_with_name(name=None):
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        
        domains = Domain._get_by_name(name)
        try:
            assert domains.__len__() <= 1, "More than one db with that name in system DB"
            if domains.__len__() == 1:
                for domain in domains:
                    base = karacos.db['Base'].get_by_id(domain.value['base_id'])    
                    return True
            else:
                return False
        except Exception, e:
            log.log_exc(sys.exc_info(),'warn')
            raise karacos._db.Exception, e
        
    @staticmethod
    def exist_with_fqdn(name=None):
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        
        domains = Domain._get_by_fqdn(name)
        try:
            assert domains.__len__() <= 1, "More than one db with that name in system DB"
            if domains.__len__() == 1:
                for domain in domains:
                    base = karacos.db['Base'].get_by_id(domain.value['base_id'])
                    return True
            else:
                return False
        except Exception, e:
            log.log_exc(sys.exc_info(),'warn')
            raise karacos._db.Exception, e
        
    @staticmethod
    def create(data=None,base=None):
        log.info("BEGIN Domain create")
        assert isinstance(data,dict), "Parameter data must be dict"
        assert isinstance(base,karacos.db['Base']), "Icompatible type, domain is : %s, should be karacos.db['Base']" % type(base)
        assert 'name' in data
        assert 'fqdn' in data
        assert isinstance(data['name'],basestring), "name should be a string"
        assert isinstance(data['fqdn'],basestring), "fqdn should be a string"
        
        result = None
        assert not Domain.exist_with_name(data['name']), "Base already exist with the same name"
        assert not Domain.exist_with_fqdn(data['name']), "Base already exist with the same name"
        
        #karacos.Db.server.create(unicode(data['name']))
        doc_id = "%s" % uuid4().hex
        log.debug("BASE doc_id : %s" % doc_id)
        session = karacos.serving.get_session()
        username = session['username']
        if username == 'anonymous':
            raise karacos.core.Exception("Domain creation not allowed for anonymous")
        
        result = { 'name': data['name'],
                   'fqdn': data['fqdn'],
                   'type': 'Domain',
                   'base_id':base.id,
                   'parent_id':karacos.db.sysbase.id,
                   'parent_db':karacos.db.sysbase.id,
                   'creator_id': username, 
                   'owner_id': username,
                   'mail_register_from_addr': 'system@karacos.org',
                   'ACL': {'group.registered@%s' % data['name']:['logout','get_user_actions_forms','w_browse'],
                           'group.confirmed@%s' % data['name']:['logout','get_user_actions_forms','w_browse'],
                           'user.anonymous@%s'%data['name']: ['login','get_user_actions_forms','w_browse']
                           }
                 }
        
        for k,v in data.items():
            if k not in result:
                result[k] = v
        if 'WebType' not in result:
            result['WebType'] = 'Domain'
        karacos.db.sysdb[doc_id] = result
        self.log.debug("Retrieving BASE doc_id : %s" % doc_id)
        result = karacos.db.sysdb[doc_id]
        admin = result._create_user(username='admin@%s' % result['name'],password='demo')
        anonymous = result._create_user(username='anonymous@%s' % result['name'])
        result['ACL'][admin.get_auth_id()] = result._get_adm_actions()
        result['ACL'][anonymous.get_auth_id()] = ['get_user_actions','login']
        
        
        result.save()
        result.log.info("END Domain.create : result type : %s", type(result) )
        return result
    

      
    def __init__(self,*args, **kw):
        self.log.debug("BEGIN Domain __init__")# : %s" % data.items())
        assert 'data' in kw
        data = kw['data']
        assert isinstance(data,dict), "Incompatible data type : %s is not a KcDocument" % type(data)
        assert isinstance(data[u'name'],basestring), "Domain name should be String"
        base = karacos.db['Base'].get_by_id(data['base_id'])
        self.__domain__ = self
        karacos.db['Parent'].__init__(self,data=data,base=base)
        self['ACL']['user.admin@%s' % self['name']] = self._get_adm_actions()
        self.__parent__ = karacos.container()
        self.__parent__.base = karacos.db.sysbase
        self.__parent__.db = karacos.db.sysdb
        if 'childrens' not in self:
            self['childrens'] = {}
        self.log.debug("END : domain.__init__ : %s" % self)
        if karacos.config.get('system','mode') == 'dev':
            self._self = self
        self.save()
        self.log.debug("END Domain __init__")
        """ is a SOURCE of PROBLEMS at Domain's creation
        if '_attachments' not in self:
            self.log.info("%s , %s" % (self.id,self.rev))
            mfzip = file(os.path.join(KaraCos.__path__[0],'_Core','themes','multiflex37.zip'))
            self.parent.db.put_attachment(self, mfzip.read(), 'multiflex37.zip')#, 'image/png')
            self._update_item()
        if 'multiflex37.zip' not in self['_attachments']:
            mfzip = file(os.path.join(KaraCos.__path__[0],'_Core','themes','multiflex37.zip'))
            self.parent.db.put_attachment(self, mfzip.read(), 'multiflex37.zip')#, 'image/png')
            self._update_item()
        """
    
    def _get_users_node(self):
        self._update_item()
        if '__users_node__' not in dir(self):
            if 'KC_usersNode' not in self.__childrens__:
                if len(self._get_child_by_name('KC_usersNode')) == 0:
                    karacos.db['Node'].create(base=None, parent=self,data={'name':'KC_usersNode'})
                    self.save()
            self.__users_node__ = self.get_child_by_name('KC_usersNode')
        return self.__users_node__
    
    def _get_groups_node(self):
        self._update_item()
        if '__groups_node__' not in dir(self):
            if 'KC_groupsNode' not in self.__childrens__:
                karacos.db['Node'].create(base=None, parent=self,data={'name':'KC_groupsNode'})
                self.save()
            self.__groups_node__ = self.__childrens__['KC_groupsNode']
        return self.__groups_node__
    
    def _get_adm_actions(self):
        if '__adm_actions__' not in dir(self):
            self.__adm_actions__ = []
            for action in self.get_actions():
                if action not in ['login','register']:
                    self.__adm_actions__.append(action)
        return self.__adm_actions__
    
    def _get_confirmed_group(self):
        
        if '__confirmed_group__' not in dir(self):
            name = 'confirmed@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__confirmed_group__ = self._create_group(name, False)
            else:
                self.__confirmed_group__ = self._get_groups_node().__childrens__[name]
        return self.__confirmed_group__ 
     
    def _get_registered_group(self):
        
        if '__registered_group__' not in dir(self):
            name = 'registered@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__registered_group__ = self._create_group(name, False)
            else:
                self.__registered_group__ = self._get_groups_node().__childrens__[name]
        return self.__registered_group__
    
    def _get_everyone_group(self):
        
        if '__everyone_group__' not in dir(self):
            name = 'everyone@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__everyone_group__ = self._create_group(name, False)
            else:
                self.__everyone_group__ = self._get_groups_node().__childrens__[name]
        return self.__everyone_group__
    
    @karacos._db.isaction
    def set_name(self,name):
        self['name'] = name

    @karacos._db.isaction
    def set_fqdn(self,fqdn):
        self['fqdn'] = fqdn
    set_fqdn.label = _("Changer le nom de domaine")
    
    def validate(self):
        """
        Validate object Data
        """
        KaraCos.Db.KcDocument.basic_validations(self)
        self.base.validate()
        
        #if not self['data'].__contains__('name'):
        #    raise self.Exception, "valueError: 'data.name' : dict entry not found"
        assert 'name' in self, "valueError: 'data.name' : name is null"
      
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def _get_user_by_name(self,username):
        """ // %s
        function(doc) {
         if (doc.type == "User" && doc.name == "%s")
          emit(doc._id, doc);
        }
        """
    
    def user_exist(self,username):
        """
        """
        assert isinstance(username,basestring), "Parameter name must be string"
        if username in self._get_users_node().__childrens__:
            return True
        else:
            return False
    
    def get_user_by_name(self,username):
        """
        """
        self.log.debug("BEGIN Domain.get_user_by_name : %s" % username)
        assert isinstance(username,basestring), "Parameter name must be string"
        result = None
        try:
            users = self._get_user_by_name(username)
            assert users.__len__() <= 1, "Domain.get_user_by_name : More than one User with that name in system DB"
            if users.__len__() == 1:
                for user in users:
                    self.log.debug("Domain.get_user_by_name : user.name = %s" % user.value['name'])
                    #base = KaraCos.Db.BaseObject.get_by_id(domain.value['base_id'])
                    result = self.db[user.key]
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result
            
    def _create_user(self,username=None,password=None,hasbase=False):
        """
        """
        self.log.info("BEGIN %s.create_user" % self['name'])
        #if self.authdoc == None:
        #    self.authdoc = KaraCos.Db.DomainAuthDoc(domain=self)
        assert len(self._get_user_by_name(username)) == 0
         #assert username not in self._get_users_node().__childrens__, "User exist with that name"
        assert username != None
        pwdValue = None
        if password != None:
            pwdValue = "%s" % karacos.db['User'].hash_pwd(password)
        #assert username not in self.users, "User already eist in that domain"
        base = None
        if hasbase:
            base = karacos.db['Base'].create('%s_user_%s' % (self['name'],username))
        user = {'name':username,
                'password': pwdValue,
                'type': 'User',
                'groups': [],
                }
        result = karacos.db['Node'].create(parent=self._get_users_node(),base=base,data=user)
        return result
    
    def get_sessuserid(self):
        return '%s.user' % self['name']
    
    def get_user_auth(self):
        user_name = None
        self.log.info("START %s.get_user_auth" % self['name'])
        
        if 'session' in dir(cherrypy):
        
            sessuserid = self.get_sessuserid()
            self.log.info("%s.get_user_auth: cherrypy session found" % self['name'])
            if sessuserid not in cherrypy.session:
                cherrypy.session[sessuserid] = ""
                cherrypy.session[sessuserid] = self._get_anonymous_user()['name']
            else:
                if cherrypy.session[sessuserid] == "" or cherrypy.session[sessuserid] == 'system':
                    cherrypy.session[sessuserid] = self._get_anonymous_user()['name']
            user_name = cherrypy.session.get(sessuserid)
        else:
            user_name='system'
        if str(user_name) != 'system' and user_name != "":
            self.log.info("%s.get_user_auth user name is %s" % (self['name'],user_name))
            
            self.log.debug("%s.get_user_auth returning user %s" % (self['name'],self.get_user_by_name(user_name)))
            
            return self.get_user_by_name(user_name)
        else:
            return self._get_anonymous_user()
        
    
    def is_user_authenticated(self):
        """
        """
        if self.get_user_auth() == self._get_anonymous_user():
            return False
        else:
            return True
    
    @karacos._db.isaction
    def reset_admin_ACL(self):
        self._update_item()
        admin = self.get_user_by_name(username='admin@%s' % self['name'])
        self['ACL'][admin.get_auth_id()] = self._get_adm_actions()
        self.save()
        return {'status':'success', 'message':_("adm actions reset"),'data':''}
    
    @karacos._db.isaction
    def logout(self):
        """
        """
        sessuserid = self.get_sessuserid()
        cherrypy.session[sessuserid] = self._get_anonymous_user()['name']
        user_name = cherrypy.session.get(sessuserid)
        return {'status':'success', 'message':_("D&eacute;connexion r&eacute;ussie"),'data':user_name}
    logout.label = _('Se d&eacute;connecter')
    
    def _get_user_base_settings_form(self):
        user = self.__domain__.get_user_auth()
        if 'CUSTOM_SITE_BASE' not in user:
            user['CUSTOM_SITE_BASE'] = self.get_site_theme_base()
        if 'CUSTOM_SITE_SKIN' not in user:
            user['CUSTOM_SITE_SKIN'] = self.get_site_template_uri()
        user.save()
        user = self.__domain__.get_user_auth()
        
        form = {'title':'Parametres utilisateur',
                'submit':'modifier',
                'fields':[
                    {'name':'CUSTOM_SITE_SKIN', 'title':_('Skin de site'), 'dataType': 'TEXT', 'value': user['CUSTOM_SITE_SKIN']},
                    {'name':'CUSTOM_SITE_BASE', 'title':_('Skin de site'), 'dataType': 'TEXT', 'value': user['CUSTOM_SITE_BASE']}
                        ]
                }
        return form
        
    
    @karacos._db.isaction
    def user_base_settings(self,*args,**kw):    
        assert 'CUSTOM_SITE_SKIN' in kw
        assert 'CUSTOM_SITE_BASE' in kw
        
        user = self.__domain__.get_user_auth()
        user['CUSTOM_SITE_SKIN'] = kw['CUSTOM_SITE_SKIN']
        user['CUSTOM_SITE_BASE'] = kw['CUSTOM_SITE_BASE']
        user.save()
    user_base_settings.get_form = _get_user_base_settings_form
    
    def _get_edit_content_form(self):
        self._update_item()
        if 'content' not in self:
            self['content'] = ''
        if 'title' not in self:
            self['title'] = ''
        self.save()
        form = {'title':'Modifier le contenu de la page',
                'submit':'Modifier',
                'fields':[
                    {'name':'title', 'title':_('Titre'), 'dataType': 'TEXT', 'value': self['title']},
                    {'name':'content', 'title':_('Contenu'), 'dataType': 'TEXT', 'formType': 'WYSIWYG', 'value': self['content']}
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,title=None,content=None):
        """
        Basic content modification for domain
        """
        self._update_item()
        self.log.info("EDIT CONTENT %s" % {title:content})
        self['content'] = content
        self['title'] = title
        self.save()
        return {'status':'success', 'message':_("Contenu modifi&eacute;"),'data':{}}
    edit_content.get_form = _get_edit_content_form
    edit_content.label = _('Modifier la page')
    
    
    def authenticate(self,username,password):
        """
        """
        self.log.debug("BEGIN Domain.authenticate_user : %s" % username)
        assert isinstance(username,basestring), "Parameter name must be string"
        assert isinstance(password,basestring), "Parameter name must be string"
        result = None
        try:
            passwordhash = "%s" % KaraCos.Db.User.hash_pwd(password)
            user = self.get_user_by_name(username)
            if user['password'] == passwordhash:
                sessuserid = self.get_sessuserid()
                cherrypy.session[sessuserid] = user['name']
                return user
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        raise KaraCos.Exception("Authentication error")
    
    
    def __batch_set_user_password__(self,username,password):
        user = self.get_user_by_name(username)
        user['password'] = "%s" % KaraCos.Db.User.hash_pwd(password)
        user.save()
    
    @karacos._db.isaction
    def change_password(self,old_password=None,password=None,confirm=None):
        """
        """
        assert password == confirm, _("Confirmation du mot de passe echouee")
        assert isinstance(old_password,basestring), "Parameter name must be string"
        assert isinstance(password,basestring), "Parameter name must be string"
        assert isinstance(confirm,basestring), "Parameter name must be string"
        result = None
        try:
            old_passwordhash = "%s" % KaraCos.Db.User.hash_pwd(old_password)
            passwordhash = "%s" % KaraCos.Db.User.hash_pwd(password)
            user = self.get_user_auth()
            if user['password'] == old_passwordhash:
                user['password'] = passwordhash
                user.save()
                result = {'status':'success', 'message':_("Mot de passe modifi&eacute;"),'data':{}}
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
            result = {'status':'failure', 'message':_("Echec"),'error':{}}
        return result
    
    
    change_password.form = {'title': _("Changer son mot de passe"),
         'submit': _('Changer'),
         'fields': [{'name':'old_password', 'title':_('Ancien mot de passe'),'dataType': 'PASSWORD'},
                    {'name':'password', 'title':_('Nouveau mot de passe'),'dataType': 'PASSWORD'},
                    {'name':'confirm', 'title':_('Confirmation'),'dataType': 'PASSWORD'},
                 ] }
    
    @karacos._db.isaction
    def create_child_node(self,name=None,type=None,base=False):
        """
        Creates a child Node.
        As an web exposed Method, this will only allow to create WebNode derived objects
        """
        try:
            assert name != None
            assert type != None
            assert issubclass(KaraCos.Db.__dict__[type],KaraCos.Db.WebNode),_("Type incorrect")
            data = {'name':name}
            node = self._create_child_node(data=data, type=type, base=base)
            return {'status':'success', 'message': _("Node cree avec succes"), 'data':node}
        except Exception, e:
            return {'status':'failure', 'message' : '%s' % e,
                        'trace': traceback.format_exc().splitlines() }
    create_child_node.label = _("Creer un noeud")
        
    """
    @karacos._db.isaction
    def login_or_register(self):
        pass
    login_or_register.form = {'title': _("Connexion au domaine"),
         'submit': _('S\'authentifier'),
                              }
    login_or_register.label = _("Entrez dans le domaine")
    """
    
    @karacos._db.isaction
    def login(self,email=None,password=None):
        """
        """
        user = None
        if True: # KaraCos._Core.mail.valid_email(email):
            try:
                user = self.authenticate(email,password)
            except karacos._db.Exception, e:
                
                return {'status':'failure', 'message' : '%s' % e.parameter,
                        'errors': None }
        else:
            return {'status':'failure', 'message':_('Adresse email invalide'),
                    'errors':{'email':_('This is not a valid mail address')}}
            
        return {'status':'success', 'message':_("Authentification r&eacute;ussie"),'data':user}
    login.label = _('S\'authentifier')

        
        
        
    def _get_anonymous_user(self):
        """
        Returns this domain anonymous user
        """
        self._update_item()
        #if self
        self.log.info("START %s._get_anonymous_user" % self['name'])
        result = ""
        if 'session' not in dir(cherrypy):
                
            result = KaraCos._Auth.objects.DummyUser('system')
        else:
            if self.get_sessuserid() in cherrypy.session:
                if '__anonymous__' not in dir(self):
                    user = None
                    group = None
                    name = 'anonymous@%s' % self['name']
                    if len(self._get_user_by_name(name)) == 0:
                        user = self._create_user(username=name)
                        user['pseudo'] = _('anonyme')
                        user.save()
                        if not self.group_exist(name):
                            group = self._create_group(name)
                        group.add_user(user)
                        self._get_everyone_group().add_user(user)
                    self.__anonymous__ = self.get_user_by_name(name)
                    #self.__anonymous__ = user
                result = self.__anonymous__
            else:
                result = KaraCos._Auth.objects.DummyUser('system')
        return result
        

    @karacos._db.ViewsProcessor.isview('self','javascript')
    def _get_group_by_name(self,parent,groupname):
        """ // %s
        function(doc) {
         if (doc.type == "Group" && doc.name == "%s")
          emit(doc._id, doc);
        }
        """
    
    def group_exist(self,groupname):
        """
        """
        assert isinstance(groupname,basestring), "Parameter name must be string"
        
        groups = self._get_group_by_name(groupname)
        try:
            assert groups.__len__() <= 1, "More than one group with that name in Domain"
            if groups.__len__() == 1:
                return True
            else:
                return False
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
    
    def get_group_by_name(self,groupname):
        """
        """
        self.log.debug("BEGIN get_group_by_name : %s" % groupname)
        assert isinstance(groupname,basestring), "Parameter name must be string"
        result = None
        try:
            groups = self._get_group_by_name(groupname)
            assert groups.__len__() <= 1, "Domain.get_by_fqdn : More than one Domain with that name in system DB"
            if groups.__len__() == 1:
                for group in groups:
                    self.log.debug("Domain.get_group_by_name : group.key = %s group.value = %s" % (group.key,group.value) )
                    #base = KaraCos.Db.BaseObject.get_by_id(domain.value['base_id'])
                    result = self.db[group.key]
            else:
                raise "Not found"
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result

    @karacos._db.isaction
    def set_ACL(self, ACL=None):
        self['ACL'] = json.loads(ACL)
        self.save()
    def _set_ACL_form(self):
        return {'title': _("Modifier l'ACL"),
         'submit': _('Modifier'),
         'fields': [{'name':'ACL', 'title':'ACL','dataType': 'TEXT','formType': 'TEXTAREA', 'value': json.dumps(self['ACL'])}]}
    set_ACL.label = "Edit ACL"
    set_ACL.get_form = _set_ACL_form
    
    def _get_ACL_default_update(self):
        if 'ACL_default_update' not in self:
            self['ACL_default_update'] = {}
            self.save()
        return self['ACL_default_update']
    
    @karacos._db.isaction
    def set_ACL_default_update(self, ACL=None):
        self['ACL_default_update'] = json.loads(ACL)
        self.save()
        
    def _set_ACL_default_update_form(self):
        if 'ACL_default_update' not in self:
            self['ACL_default_update'] = {}
            self.save()
        return {'title': _("Modifier l'ACL par defaut pour les objets du domaine"),
         'submit': _('Modifier'),
         'fields': [{'name':'ACL', 'title':'ACL','dataType': 'TEXT','formType': 'TEXTAREA', 'value': json.dumps(self['ACL_default_update'])}]}
    set_ACL_default_update.get_form = _set_ACL_default_update_form

    @karacos._db.isaction
    def set_web_domain_type(self, webtype=None):
        self['WebType'] = webtype
        self.save()
    set_web_domain_type.form = {'title': _("Changer le theme"),
         'submit': _('Changer'),
         'fields': [{'name':'webtype', 'title':'theme','dataType': 'TEXT'}]}
    set_web_domain_type.label = "Change web_domain type"

    @karacos._db.isaction
    def set_site_theme_base(self, site_theme_base=None):
        self['site_theme_base'] = site_theme_base
        self.save()
    set_site_theme_base.form = {'title': _("Changer le theme"),
         'submit': _('Changer'),
         'fields': [{'name':'site_theme_base', 'title':'theme base','dataType': 'TEXT'}]}
    set_site_theme_base.label = "Set site template"
    
    def get_site_theme_base(self):
        result = "/default"
        if 'site_theme_base' in self:
            result = self['site_theme_base']
        if len(self._get_user_by_name("anonymous@%s" % self['name'])) == 1:
            user = self.get_user_auth()
            if 'CUSTOM_SITE_BASE' in user:
                result = user['CUSTOM_SITE_BASE']
        return result
    
    def _get_trac_node(self):
        if '__trac__' not in self.__dict__:
            if "_tracking" not in self.__childrens__:
                self._create_child_node(data={'name':'_tracking'}, type='Node')
            self.__trac__ = self.__childrens__["_tracking"]
        return self.__trac__
    
    def get_manager_node(self):
        if 'manager' not in self.__childrens__:
            self._create_child_node(data={'name':'manager'}, type='Manager')
        return self.__childrens__['manager']
    
    def _trac(self,id=None):
        assert isinstance(id,basestring)
        trac_node = self._get_trac_node()
        forward = '/'
        if 'items' not in trac_node:
            trac_node['items'] = {}
            trac_node.save()
        if id in trac_node['items']:
            forward = trac_node['items'][id]['forward']
            trac_node['items'][id]['count'] = trac_node['items'][id]['count'] + 1
            trac_node.save()
        raise cherrypy.HTTPRedirect(forward,301)
    
    @karacos._db.isaction
    def _t(self,id):
        self.log.info("_t: id = %s" % id)
        self._trac(str(id))

    @karacos._db.isaction
    def trac(self,id=None):
        self._trac(str(id))
    
    @karacos._db.isaction
    def create_tracking_item(self,id=None,forward=None,description=None):
        trac_node = self._get_trac_node()
        if 'items' not in trac_node:
            trac_node['items'] = {}
        if id not in trac_node['items']:
            trac_node['items'][id] = {'forward':forward,'count':0,'description':description}
        else:
            assert False, "id Already exist"
        trac_node.save()
        
    create_tracking_item.form = {'title': _("Creer Tracking ref"),
         'submit': _('Changer'),
         'fields': [{'name':'id', 'title':'Tracking reference id','dataType': 'TEXT'},
                    {'name':'forward', 'title':'Forward URL','dataType': 'TEXT'},
                    {'name':'description', 'title':'Description','dataType': 'TEXT'}]}
    create_tracking_item.label = "Creer Tracking ref"
    
    @karacos._db.isaction
    def view_tracking(self):
        return {'status':'succes','data' : json.dumps(self._get_trac_node()['items'])}
    
    @karacos._db.isaction
    def set_site_template_uri(self, site_template_uri=None):
        self['site_template_uri'] = site_template_uri
        self.save()
    set_site_template_uri.form = {'title': _("Changer le template site"),
         'submit': _('Changer'),
         'fields': [{'name':'site_template_uri', 'title':'template_uri','dataType': 'TEXT'}]}
    set_site_template_uri.label = "Set site template"
    
    def get_instance_template_uri(self):
        uri = ""
        try:
            uri = "%s/%s" % (self.get_site_theme_base(),self['WebType'])
            template = self.lookup.get_template(uri)
        except:
            try:
                self.log.log_exc(sys.exc_info(),'info')
                uri = "%s/Domain" % self.get_site_theme_base()
                template = self.lookup.get_template(uri)
            except:
                try:
                    self.log.log_exc(sys.exc_info(),'info')
                    uri = "/default/%s" % self['WebType']
                    template = self.lookup.get_template(uri)
                except:
                    uri = "/default/Domain"
        self.log.info("Using template %s" % uri)
        return uri
        
    
    def get_site_template_uri(self):
        if 'site_template_uri' not in self.__dict__:
            if 'site_template_uri' not in self:
                try:
                    self.site_template_uri = '%s/site' % self.get_site_theme_base()
                    template = self.lookup.get_template(self.site_template_uri)
                except:
                    self.site_template_uri = '/default/site'
            else:
                self.site_template_uri = self['site_template_uri']
        user = self.get_user_auth()
        if 'CUSTOM_SITE_SKIN' in user:
            return user['CUSTOM_SITE_SKIN']
        else:
            return self.site_template_uri
         
    def _create_group(self,groupname,hasbase=False):
        """
        """
        assert groupname != None
        #assert username not in self.users, "User already eist in that domain"
        base = None
        if hasbase:
            base = KaraCos.Db.BaseObject.create('%s_group_%s' % (self['name'],groupname))
        group = {'name':groupname,
                'type': 'Group',
                'users': {},
                }
        owner = KaraCos._Auth.objects.DummyUser('system')
        return KaraCos.Db.Node.create(parent=self._get_groups_node(),base=base,data=group,owner=owner)
        #self.authdoc['groups'][group['name']] = group.id

    
    @karacos._db.isaction
    def delete(self):
        """
        """
        #self.base = KaraCos.Db.sysdb[self['_id']]
        #KaraCos.Db.sysdb.delete(self.base)
        #self = self.parent.db[self['_id']]
        self.log.debug(" Base delete : %s" % self)
        
        for child in self.__childrens__:
            self.get_child_by_name(child).delete()
        if self['base_id'] != self['parent_db']:
            self.base.delete()
        
        del KaraCos.Db.sysdb[self['_id']]
        del self
    
    #@cherrypy.expose()
    def default(self,*args,**kw):
        """
        """
        if cherrypy.request.headers['Host'] != self.__domain__['fqdn']:
            if self.__domain__['name'] != 'sysdomain':
                raise cherrypy.HTTPRedirect('http://%s'%self.__domain__['fqdn'],301)
        currentparent = self
        countargs = 0
        forward = ''
        if 'forward' in cherrypy.session:
            forward = cherrypy.session['forward']
        for arg in args:
            if unicode(arg) in currentparent.get_web_childrens().values():
                currentparent = currentparent.__childrens__[arg]
                countargs=countargs+1
            else:
                if arg in dir(currentparent):
                    argObject = eval("currentparent.%s" % arg)
                    self.log.info("Domain dispatcher : arg in dir : %s" % dir(argObject))
                    if isinstance(argObject,type(currentparent.get_web_childrens)):
                        if 'isaction' in dir(argObject):
                            if argObject.isaction:
                                if 'request' in dir(cherrypy):
                                    if cherrypy.request.method == 'GET':
                                        if forward != '': #"" Un GET est un forward
                                            del cherrypy.session['forward']
                                        if len(kw.keys()) < 1:
                                            if cherrypy.request.headers['Accept'].find("html")>=0:
                                                template = currentparent.__domain__.lookup.get_template('/system')                                                   
                                                return template.render(instance=currentparent, action=argObject.get_action(currentparent))
                                            if cherrypy.request.headers['Accept'].find("application/json")>=0:
                                                return json.dumps(argObject.get_action(currentparent))
                                            if cherrypy.request.headers['Accept'].find("application/xml")>=0:
                                                ""  # Gestion XML
                                            template = currentparent.__domain__.lookup.get_template('/system')
                                            return template.render(instance=currentparent, action=argObject.get_action(currentparent))
                                    else:
                                        result = argObject(args[countargs:],kw)
                                        if forward != '':
                                            del cherrypy.session['forward']
                                            raise cherrypy.HTTPRedirect(forward,301)
                                        else:
                                            return result
                                            
                        elif 'exposed' in dir(argObject):
                            if argObject.exposed:
                                countargs=countargs+1
                                result = argObject(*args[countargs:],**kw)
                                return result
                        else:
                            raise KaraCos.HTTPError(status=404,message=_("Ressource incorrecte"),domain=self)
                    else:
                        countargs=countargs+1
                        self.log.info("len(args) =%s, countargs = %s" %(len(args), countargs))
                        
                    #    if u'index' in currentparent.get_user_actions(self.get_user_auth()):
                    #        return currentparent.index(*args[countargs:],**kw)
                    #    else:
                    #        raise cherrypy.HTTPError(status=403,message=_("Ressource non autorisee"))
                else:
                    raise KaraCos.HTTPError(status=404,message=_("Ressource introuvable"),domain=self)
        ####
            self.log.info("currentparent : %s" % currentparent)#.get_user_actions(self.get_user_auth()))    
            if u'index' in unicode(currentparent.get_user_actions(self.get_user_auth())):
                #countargs=countargs+1
                if countargs == len(args):
                    return currentparent.index(*args[countargs:],**kw)
            else:
                raise KaraCos.HTTPError(status=403,message=_("Ressource non autorisee"),domain=self)
        ## for ## 