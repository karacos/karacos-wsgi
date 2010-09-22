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
from karacos.http import HTTPError
import inspect
import urllib2
log = getLogger(__name__)
from mako.template import Template
from mako.lookup import TemplateLookup
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
              emit(doc._id, doc);
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
        assert not Domain.exist_with_fqdn(data['fqdn']), "Base already exist with the same name"
        
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
        log.debug("Retrieving BASE doc_id : %s" % doc_id)
        result = karacos.db.sysdb[doc_id]
        result._update_item()
        admin = result._create_user(username='admin@%s' % result['name'],password='demo')
        anonymous = result._create_user(username='anonymous@%s' % result['name'])
        result._update_item()
        result['ACL'][admin.get_auth_id()] = result._get_adm_actions()
        result['ACL'][anonymous.get_auth_id()] = ['get_user_actions','login']
        result.save()
        result.log.info("END Domain.create : result type : %s", type(result) )
        return result
    

      
    def __init__(self,*args, **kw):
        self.log = karacos.core.log.getLogger(self)
        self.log.debug("BEGIN Domain __init__")# : %s" % data.items())
        assert 'data' in kw
        data = kw['data']
        assert isinstance(data,dict), "Incompatible data type : %s is not a KcDocument" % type(data)
        assert isinstance(data[u'name'],basestring), "Domain name should be String"
        base = karacos.db['Base'].get_by_id(data['base_id'])
        self.__domain__ = self
        karacos.db['Parent'].__init__(self,data=data,base=base)
        self.__parent__ = karacos.container()
        self.__parent__.base = karacos.db.sysbase
        self.__parent__.db = karacos.db.sysdb
        self['ACL']['user.admin@%s' % self['name']] = self._get_adm_actions()
        if 'childrens' not in self:
            self['childrens'] = {}
            self.save()
        self.log.debug("END : domain.__init__ : %s" % self)
        if karacos.config.has_section('system'):
            if karacos.config.has_option('system', 'mode'):
                if karacos.config.get('system','mode') == 'dev':
                    self._self = self
        if 'lookup' not in self.__dict__:
            self.log.info("Creating template lookup for %s" % self['name'])
            default_template_dir = os.path.join(karacos.homedir,'resources','templates')
            module_dir = os.path.join(karacos._srvdir,'temp','pytemplates')
            if not os.path.exists(module_dir):
                os.makedirs(module_dir)
            templatesdirs = [default_template_dir]
            if 'templatesdirs' in self:
                for templatedir in self['templatesdirs']:
                    templatesdirs.append(templatedir)
            self.lookup =  TemplateLookup(directories=templatesdirs,
                #default_filters=['decode.utf8'], 
                module_directory=module_dir,filesystem_checks=False,
                input_encoding='utf-8',output_encoding='utf-8')
        if 'staticdirs' not in self.__dict__:
            default_static_dir = os.path.join(karacos.homedir,'resources','static')
            if 'staticdirs' not in self:
                self['staticdirs'] = {'_browser':default_static_dir}
                self.save()
            if self['staticdirs']['_browser'] != default_static_dir:
                self['staticdirs']['_browser'] = default_static_dir
                self.save()
            self.staticdirs = self['staticdirs'] 
        self.log.debug("END Domain __init__")
    
    @karacos._db.isaction
    def get_user_actions_forms(self):
        return self._get_user_actions_forms()
    
    def _get_users_node(self):
        self._update_item()
        self.log.debug("_get_users_node : creating user_node")
        if '__users_node__' not in dir(self):
            self.log.debug("__users_node__ not found")
            if 'KC_usersNode' not in self.__childrens__:
                self.log.debug("KC_usersNode not found")
                if len(self._get_child_by_name('KC_usersNode')) == 0:
                    self.log.debug("creating user_node")
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
        self._update_item()
        if '__adm_actions__' not in dir(self):
            self.__adm_actions__ = []
            for action in self.get_actions():
                if action not in ['login','register']:
                    self.__adm_actions__.append(action)
        return self.__adm_actions__
    
    def _get_confirmed_group(self):
        self._update_item()
        if '__confirmed_group__' not in dir(self):
            name = 'confirmed@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__confirmed_group__ = self._create_group(name, False)
            else:
                self.__confirmed_group__ = self._get_groups_node().__childrens__[name]
        return self.__confirmed_group__ 
     
    def _get_registered_group(self):
        self._update_item()
        if '__registered_group__' not in dir(self):
            name = 'registered@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__registered_group__ = self._create_group(name, False)
            else:
                self.__registered_group__ = self._get_groups_node().__childrens__[name]
        return self.__registered_group__
    
    def _get_everyone_group(self):
        self._update_item()
        if '__everyone_group__' not in dir(self):
            name = 'everyone@%s' % self['name']
            if name not in self._get_groups_node().__childrens__:
                self.__everyone_group__ = self._create_group(name, False)
            else:
                self.__everyone_group__ = self._get_groups_node().__childrens__[name]
        return self.__everyone_group__
    
    @karacos._db.isaction
    def set_name(self,name):
        self._update_item()
        self['name'] = name
        self.save()
    @karacos._db.isaction
    def set_fqdn(self,fqdn):
        self._update_item()
        self['fqdn'] = fqdn
        self.save()
    set_fqdn.label = _("Changer le nom de domaine")
    
    def validate(self):
        """
        Validate object Data
        """
        self._update_item()
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
        self._update_item()
        assert isinstance(username,basestring), "Parameter name must be string"
        if username in self._get_users_node().__childrens__:
            return True
        else:
            return False
    
    def get_user_by_name(self,username):
        """
        """
        self._update_item()
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
        self._update_item()
        self.log.info("BEGIN %s.create_user" % self['name'])
        assert len(self._get_user_by_name(username)) == 0, "User exist with that name"
        assert username != None
        pwdValue = None
        if password != None:
            pwdValue = "%s" % karacos.db['User'].hash_pwd(password)
        base = None
        if hasbase:
            base = karacos.db['Base'].create('%s_user_%s' % (self['name'],username))
        user = {'name':username,
                'password': pwdValue,
                'type': 'User',
                'groups': [],
                }
        users_node = self._get_users_node()
        assert users_node != None 
        result = karacos.db['User'].create(parent=users_node,base=base,data=user)
        return result
    
    def get_sessuserid(self):
        self._update_item()
        return '%s.user' % self['name']
    
    def get_user_auth(self):
        self._update_item()
        self.log.info("START %s.get_user_auth" % self['name'])
        return karacos.serving.get_session().get_user_auth()
        
    
    def is_user_authenticated(self):
        """
        """
        self._update_item()
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
        karacos.serving.get_session().invalidate()
        return {'status':'success', 'message':_("D&eacute;connexion r&eacute;ussie")}
    logout.label = _('Se d&eacute;connecter')
    
    def _get_user_base_settings_form(self):
        user = self.get_user_auth()
        if 'CUSTOM_SITE_BASE' not in user:
            user['CUSTOM_SITE_BASE'] = self.get_site_theme_base()
        if 'CUSTOM_SITE_SKIN' not in user:
            user['CUSTOM_SITE_SKIN'] = self.get_site_template_uri()
        user.save()
        user = self.get_user_auth()
        
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
        
        user = self.get_user_auth()
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
        if 'head_bloc' not in self:
            self['head_bloc'] = ''
        
        self.save()
        form = {'title':'Modifier le contenu de la page',
                'submit':'Modifier',
                'fields':[
                    {'name':'title', 'title':_('Titre'), 'dataType': 'TEXT', 'value': self['title']},
                    {'name':'head_bloc', 'title':_('Head bloc'), 'dataType': 'TEXT', 'value': self['head_bloc'], 'formType': 'TEXTAREA'},
                    {'name':'content', 'title':_('Contenu'), 'dataType': 'TEXT', 'formType': 'WYSIWYG', 'value': self['content']}
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,title=None,content=None,head_bloc=None):
        """
        Basic content modification for domain
        """
        self._update_item()
        self.log.debug("EDIT CONTENT %s" % {title:content})
        self['content'] = content
        self['title'] = title
        self['head_bloc'] = head_bloc
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
        return karacos.serving.get_session().authenticate(username,password)
    
    
    def __batch_set_user_password__(self,username,password):
        user = self.get_user_by_name(username)
        user['password'] = "%s" % karacos.db['User'].hash_pwd(password)
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
            old_passwordhash = "%s" % karacos.db['User'].hash_pwd(old_password)
            passwordhash = "%s" % karacos.db['User'].hash_pwd(password)
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
        self._update_item()
        try:
            assert name != None
            assert type != None
            assert issubclass(karacos.db[type],karacos.db['WebNode']),_("Type incorrect")
            data = {'name':name}
            node = self._create_child_node(data=data, type=type, base=base)
            return {'status':'success', 'message': _("Node cree avec succes"), 'data':node}
        except Exception, e:
            return {'status':'failure', 'message' : '%s' % e,
                        'trace': traceback.format_exc().splitlines() }
    create_child_node.label = _("Creer un noeud")
    create_child_node.form = {'title': _("Creer un element"),
         'submit': _('Creer'),
         'fields': [{'name':'name', 'title':_('Nom de la resource'),'dataType': 'TEXT'},
                    {'name':'type', 'title':_("Type d'objet"),'dataType': 'TEXT'},
                    {'name':'base', 'title':_('Base'),'dataType': 'TEXT'},
                 ] }
    
    @karacos._db.isaction
    def login(self,email=None,password=None):
        """
        """
        self._update_item()
        user = None
        if karacos.core.mail.valid_email(email):
            try:
                user = self.authenticate(email,password)
            except karacos._db.Exception, e:
                
                return {'status':'failure', 'message' : '%s' % e.parameter,
                        'errors': None }
        else:
            return {'status':'failure', 'message':_('Adresse email invalide'),
                    'errors':{'email':_('This is not a valid mail address')}}
            
        return {'status':'success', 'message':_("Authentification r&eacute;ussie"),'data':user}
    login.label = _("S'authentifier")
    login.form = {'title': _("Connexion au site"),
         'submit': _('Se connecter'),
         'fields': [{'name':'email', 'title':_('Adresse email'),'dataType': 'TEXT'},
                    {'name':'password', 'title':_('Mod de passe'),'dataType': 'PASSWORD'}]}



    def _get_anonymous_user(self):
        """
        Returns this domain anonymous user
        """
        self._update_item()
        #self._update_item()
        self.log.info("START %s._get_anonymous_user" % self['name'])
        result = ""

        if '__anonymous__' not in dir(self):
            user = None
            group = None
            name = 'anonymous@%s' % self['name']
            if len(self._get_user_by_name(name)) == 0:
                user = self._create_user(username=name)
                user['pseudo'] = _('anonymous')
                user.save()
                if not self.group_exist(name):
                    group = self._create_group(name)
                group.add_user(user)
                self._get_everyone_group().add_user(user)
            self.__anonymous__ = self.get_user_by_name(name)
            #self.__anonymous__ = user
        result = self.__anonymous__
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
        self._update_item()
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
        self._update_item()
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
        self._update_item()
        self['ACL'] = karacos.json.loads(ACL)
        self.save()
    def _set_ACL_form(self):
        return {'title': _("Modifier l'ACL"),
         'submit': _('Modifier'),
         'fields': [{'name':'ACL', 'title':'ACL','dataType': 'TEXT','formType': 'TEXTAREA', 'value': karacos.json.dumps(self['ACL'])}]}
    set_ACL.label = "Edit ACL"
    set_ACL.get_form = _set_ACL_form
    
    def _get_ACL_default_update(self):
        self._update_item()
        if 'ACL_default_update' not in self:
            self['ACL_default_update'] = {}
            self.save()
        return self['ACL_default_update']
    
    @karacos._db.isaction
    def set_ACL_default_update(self, ACL=None):
        self._update_item()
        self['ACL_default_update'] = karacos.json.loads(ACL)
        self.save()
        
    def _set_ACL_default_update_form(self):
        self._update_item()
        if 'ACL_default_update' not in self:
            self['ACL_default_update'] = {}
            self.save()
        return {'title': _("Modifier l'ACL par defaut pour les objets du domaine"),
         'submit': _('Modifier'),
         'fields': [{'name':'ACL', 'title':'ACL','dataType': 'TEXT','formType': 'TEXTAREA', 'value': json.dumps(self['ACL_default_update'])}]}
    set_ACL_default_update.get_form = _set_ACL_default_update_form

    @karacos._db.isaction
    def set_web_domain_type(self, webtype=None):
        self._update_item()
        self['WebType'] = webtype
        self.save()
    set_web_domain_type.form = {'title': _("Changer le theme"),
         'submit': _('Changer'),
         'fields': [{'name':'webtype', 'title':'theme','dataType': 'TEXT'}]}
    set_web_domain_type.label = "Change web_domain type"

    @karacos._db.isaction
    def set_site_theme_base(self, site_theme_base=None):
        self._update_item()
        self['site_theme_base'] = site_theme_base
        self.save()
    set_site_theme_base.form = {'title': _("Changer le theme"),
         'submit': _('Changer'),
         'fields': [{'name':'site_theme_base', 'title':'theme base','dataType': 'TEXT'}]}
    set_site_theme_base.label = "Set site template"
    
    def get_site_theme_base(self):
        self._update_item()
        result = "/default"
        if 'site_theme_base' in self:
            result = self['site_theme_base']
        if len(self._get_user_by_name("anonymous@%s" % self['name'])) == 1:
            user = self.get_user_auth()
            if 'CUSTOM_SITE_BASE' in user:
                result = user['CUSTOM_SITE_BASE']
        return result
    
    def _get_trac_node(self):
        self._update_item()
        if '__trac__' not in self.__dict__:
            if "_tracking" not in self.__childrens__:
                self._create_child_node(data={'name':'_tracking'}, type='Node')
            self.__trac__ = self.__childrens__["_tracking"]
        return self.__trac__
    
    def get_manager_node(self):
        self._update_item()
        if 'manager' not in self.__childrens__:
            self._create_child_node(data={'name':'manager'}, type='Manager')
        return self.__childrens__['manager']
    
    def _trac(self,id=None):
        self._update_item()
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
        raise karacos.http.Redirect(forward,301)
    
    @karacos._db.isaction
    def _t(self,id):
        self.log.info("_t: id = %s" % id)
        self._trac(str(id))

    @karacos._db.isaction
    def trac(self,id=None):
        self._trac(str(id))
    
    @karacos._db.isaction
    def create_tracking_item(self,id=None,forward=None,description=None):
        self._update_item()
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
        self._update_item()
        return {'status':'succes','data' : json.dumps(self._get_trac_node()['items'])}
    
    @karacos._db.isaction
    def set_site_template_uri(self, site_template_uri=None):
        self._update_item()
        self['site_template_uri'] = site_template_uri
        self.save()
    set_site_template_uri.form = {'title': _("Changer le template site"),
         'submit': _('Changer'),
         'fields': [{'name':'site_template_uri', 'title':'template_uri','dataType': 'TEXT'}]}
    set_site_template_uri.label = "Set site template"
    
    def get_instance_template_uri(self):
        self._update_item()
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
        self._update_item()
        if 'site_template_uri' not in self:
            try:
                self['site_template_uri'] = '%s/site' % self.get_site_theme_base()
                template = self.lookup.get_template(self.site_template_uri)
            except:
                self['site_template_uri'] = '/default/site'
            self.save()
        user = self.get_user_auth()
        if 'CUSTOM_SITE_SKIN' in user:
            return user['CUSTOM_SITE_SKIN']
        else:
            return self['site_template_uri']
         
    def _create_group(self,groupname,hasbase=False):
        """
        """
        self._update_item()
        assert groupname != None
        #assert username not in self.users, "User already eist in that domain"
        base = None
        if hasbase:
            base = karacos.db['Base'].create('%s_group_%s' % (self['name'],groupname))
        group = {'name':groupname,
                'type': 'Group',
                'users': {},
                }
        return karacos.db['Group'].create(parent=self._get_groups_node(),base=base,data=group)
        #self.authdoc['groups'][group['name']] = group.id

    
    @karacos._db.isaction
    def delete(self):
        """
        """
        self._update_item()
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
    
    def lookup_resource(self,urlpath):
        """
        returns a record with object and args
        """
        self._update_item()
        countargs = 0
        result = {'object': self }
        #cirrentobj = self
        self.log.debug("lookup_object for path : %s" % urlpath)
        args = urlpath.split("/")
        self.log.debug("lookup_object argssplit '%s'" % args)
        for arg_quote in args :
            arg = urllib2.unquote(arg_quote)
            countargs=countargs+1
            self.log.debug("lookup_object (for) arg '%s'" % arg)
            if arg != '' and arg != '_self':
                if isinstance(result['object'],karacos.db['Document']):
                    if arg in result['object'].get_web_childrens_for_id().keys():
                        self.log.debug("lookup '%s' in web childrens is [%s]" % (arg,result['object'].__childrens__[arg]))
                        result['object'] = result['object'].db[result['object']['childrens'][arg]]
                    else:
                        self.log.debug("testing for '%s' in %s" % (arg,dir(result['object'])))
                        if arg not in dir(result['object']):
                            if isinstance(result['object'], karacos.db['Parent']):
                                if arg not in self['staticdirs'].keys():
                                    raise karacos.http.NotFound()
                                
                                self.log.debug("serving static resource for url '%s'" % urlpath)
                                resourcename = urlpath[urlpath.index(arg)+len(arg)+1:]
                                self.log.debug("Resource name is : '%s' and served from dir '%s'" % (resourcename,self['staticdirs'][arg]) )
                                return {'object': self,  'staticfile': os.path.join(self['staticdirs'][arg] , resourcename) }
                        else:
                            if arg not in result['object'].get_user_actions(self.get_user_auth()) :
                                raise HTTPError(403, "Unauthorized resource")
                            evalstr = str("result['object'].%s" % arg)
                            self.log.debug('Evaluating "%s" in [%s]' % (evalstr,result['object']))
                            obj = eval(evalstr)
                            self.log.debug("Evaluated '%s' in 'dir(%s)' : '%s'" % (arg,result['object']['name'],obj))
                            if inspect.ismethod(obj):
                                if 'isaction' in dir(obj):
                                    if obj.isaction:
                                        result['method'] = obj
                                        result['args'] = args[countargs:]
                                        break
                            raise HTTPError(404, "Resource unavailable")
        self.log.debug("lookup_object result is [%s]" % result)
        return result