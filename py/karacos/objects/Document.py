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

Created on 24 nov. 2009

@author: nico
'''
import karacos
import datetime
import sys
import couchdb.client

import logging
import urlparse
log = logging.getLogger("%s.KcDocMeta" % __name__)
class KcDocMeta(type):
    """
    Metaclasse pour Document KaraCos
    """
    def __init__(self, name, parents, dict):
        """
        Appele lors de la construction d'un type
        """
        
        log.info("__init__ for '%s'" % (name))
        log.debug("parents of class '%s' [%s] [%s]" % (name,parents,dir(parents)))
        if self not in karacos.webdb.actions.keys():
            karacos.webdb.actions[self] = []
        if couchdb.client.Document not in parents:
            karacos.webdb.actions[self].extend(karacos.webdb.actions[parents[0]])
        karacos.db[name] = self
        
        for attrname in dir(self) :
            attr = eval("self.%s" % attrname)
            self.processactions(attr,attrname)
        self.__name__ = name
        
    
    def __call__(self,*args, **kw):
        """
        """
        log.debug("__call__  begin")
        instance = type.__call__(self, *args, **kw)
        
        return instance
    
    def processactions(self,attr,attrname):
        """
        """
        #self.log.info("KcDoMeta : Processing action %s" % (attr))
        try:
            if 'isaction' in dir(attr):
                if attrname not in karacos.webdb.actions[self]:
                    karacos.webdb.actions[self].append(attrname)
        except:
            log.log_exc(sys.exc_info(),'error')
        
        
karacos.db['KcDocMeta'] = KcDocMeta

class Document(couchdb.client.Document):
    """
    Main container for all objects in karacos
    Abstract type, subclass it and override methods : get_by_name, get_by_id, get_all
    it expose following attributes :
     * id [facultatif]
     * name [required]
     * data [required]
     * creation_date [required] String DATE au format ISO %Y-%m-%dT%H:%M:%S.%f
     * last_modification_date [required] String DATE au format ISO %Y-%m-%dT%H:%M:%S.%f
     * creator_id [required]
     * owner_id [required]
     * group_id [required]
     * ACL (reste a specifier)
    and these methods :
     * basic_validations
    """
    
    __metaclass__ = KcDocMeta
    
    @staticmethod
    def get_by_name(name):
        """
        Get object by name
        No DB at this level, this method has to be implemented by subtypes
        """
        raise karacos._db.Exception, "Incorrect type : get_by_name has to be overrided by subclass"   
        
    def __init__(self,data=None):
        """
        Constructeur..
        Ici seront affectees les valeurs de createur id, groupid ownerId et les permissions par defaut
        """
        assert isinstance(data,dict), "Value must be a dict"
        couchdb.client.Document.__init__(self,data.items())
        self.log = karacos.core.log.getLogger(self)
        if 'creator_id' not in self:
            self['creator_id'] = 'system'
        if 'owner_id' not in self:
            self['owner_id'] = 'system'
        if 'group_id' not in self:
            self['group_id'] = {}
        if 'ACL' not in self:
            self['ACL'] = {}
        if 'creation_date' not in self:
            self['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        if 'last_modification_date' not in self:
            self['last_modification_date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.basic_validations()
        if karacos.config.has_section('system'):
            if karacos.config.has_option('system', 'mode'):
                if karacos.config.get('system','mode') == 'dev':
                    self._self = self
        #if '_id' not in self:
        _user_actions = []
    
    def __getstate__(self):
        """
        Required to have nice access to __dict__ attribute of instance
        """
        return 
    
    def get_aloha_template_uri(self):
        uri = ""
        try:
            uri = "/includes/alohaconf/%s.js" % self['WebType']
            template = self.__domain__.lookup.get_template(uri)
        except:
            self.log.log_exc(sys.exc_info(),'info')
            uri = "/includes/alohaconf/%s.js" % self['type']
            template = self.__domain__.lookup.get_template(uri)
        return uri
    
    def _get_action_url(self):
        acturl = ""
        assert isinstance(self.__class__,karacos.db['WebMeta'])
        if isinstance(self, karacos.db['Domain']):
            acturl = "/"
        elif isinstance(self, karacos.db['WebNode']):
            acturl = '/%s' % self.get_relative_uri()
        if karacos.config.get('system','mode') == 'dev':
            acturl = '/_self%s' % acturl
        requested_host = karacos.serving.get_request().headers['Host']
        if 'fqdn_aliases' not in self.__domain__:
            self.__domain__['fqdn_aliases'] = []
            self.__domain__.save()
        if  requested_host != self.__domain__['fqdn'] and requested_host not in self.__domain__['fqdn_aliases']:
            if not self.__domain__['name'] == 'sysdomain':
                raise karacos.http.Redirect('http://%s%s'%(self.__domain__['fqdn'],acturl),301)
        return acturl
    
    def get_actions(self):
        """
        Returns array of all available actions for this class
        """
        return karacos.webdb.actions[type(self)]
    
    
    def _get_user_actions_forms(self):
        """
        Returns user authorized actions for this object (Core component of KcAuth)
        """
        user=None
        assert issubclass(self.__metaclass__,karacos.db['WebMeta']), "Only WebTypes can handle method with 1 arg"
        if karacos.serving.get_session() != None:
            user = self.__domain__.get_user_auth()
        actions = self.get_user_actions(user)
        result = {'actions':[],
                  'user':user['name']
                  }
        if 'pseudo' in user:
            result['pseudo'] = user['pseudo']
        for action in actions:
            actresult = {'action' : action,
                         'acturl': self._get_action_url()}
            if 'form' in dir(self.get_action(action)):
                actresult['form'] = self.get_action(action).form
            elif 'get_form' in dir(self.get_action(action)):
                actresult['form'] = self.get_action(action).get_form(self)
            if 'label' in dir(self.get_action(action)):
                actresult['label'] = self.get_action(action).label
            result['actions'].append(actresult)
        return {'status':'success', 'message':_("get_user_actions_forms succeeded"),'data':result}
        
    def _get_actions(self):
        if karacos.serving.get_session() != None:
            user = self.__domain__.get_user_auth()
        return self.get_user_actions(user)
    
    def get_user_actions(self, user):
        """
        Returns user authorised actions for this object (Core component of KcAuth)
        """
        assert isinstance(user,karacos.db['User']), "actions can only be retrieved for a user"
        result = []
        if user.get_auth_id() in self['ACL']:
            for action in self['ACL'][user.get_auth_id()]:
                if action == 'all':
                        return self.get_actions()
                else:
                    if action not in result:
                        result.append(action)
        for group in user.get_groups():
            if group in self['ACL']:
                for action in self['ACL'][group]:
                    if action == 'all':
                        return self.get_actions()
                    else:
                        if action not in result:
                            result.append(action)
        return result
        
    def get_action(self,action):
        return eval("self.%s" % action)
    
    
    def save(self):
        #self = self.__parent__.db[self.id]
        db = self.__parent__.db
        id = self.id
        self['last_modification_date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        db[id] = self
#        self = db[id]

    def _update_item(self):
        db = self.__parent__.db
        db.refresh_item(self)
    
    def basic_validations(self):
        """
        validate Core Data
        """
        assert 'creation_date' in self, "valueError: 'creation_date' : dict entry not found"
        try:
            self.log.warn(self['creation_date'])
            datetime.datetime.strptime(self['creation_date'],'%Y-%m-%dT%H:%M:%S')
        except:
            self.log.log_exc(sys.exc_info(),'debug')
            raise karacos.core.Exception, "valueError: 'creation_date' : date format not recognised"
        assert 'last_modification_date' in self, "valueError: 'last_modification_date' : dict entry not found"
        try:
            datetime.datetime.strptime(self['last_modification_date'],'%Y-%m-%dT%H:%M:%S')
        except:
            self.log.log_exc(sys.exc_info(),'debug')
            raise self.Exception, "valueError: 'last_modification_date' : date format not recognised"
        
        assert 'creator_id' in self, "valueError: 'creator_id' : dict entry not found"
        assert 'owner_id' in self, "valueError: 'owner_id' : dict entry not found"
        assert 'group_id' in self, "valueError: 'group_id' : dict entry not found"
        assert 'ACL' in self, "valueError: 'permissions' : dict entry not found"

    def __get_title__(self):
        session = karacos.serving.get_session()
        codlang = session.get_session_lang()
        if 'title' not in self:
            return 'No title.'
        if codlang == 'default':
            return self['title']
        else:
            if 'title_%s' % codlang in self:
                return self['title_%s' % codlang]
            else:
                return self['title']
    
    def __get_content__(self):
        session = karacos.serving.get_session()
        codlang = session.get_session_lang()
        if 'content' not in self:
            return '<p>No content found.</p>'
        if codlang == 'default':
            return self['content']
        else:
            if 'content_%s' % codlang in self:
                return self['content_%s' % codlang]
            else:
                return self['content']
    
    @karacos._db.isaction
    def _sync(self, data=None, override=False):
        """
        Entry-point for remote synchronisation
        @param data: synchronisation data
        @param override: True if given data should override existing, bypassing content verification 
        """
        result = {}
        assert 'name' in data, _("Object name must be specified")
        assert 'type' in data, _("Object type must be specified")
        assert data['type'] == self['type'], _("Object type don't match")
        if 'WebType' in data:
            assert 'WebType' in self, _("Object type don't match")
            assert self['WebType'] == data['WebType'], _("Object type don't match")
            del data['WebType']
        assert unicode(data['name']) == unicode(self['name']), _("Object name don't match")
        if 'sync' not in self:
            self['sync'] = {}
        assert '_id' in data
        remote_id = data['_id']
        
        if remote_id not in self['sync']:
            # use the remote id as a key for sync trace
            self['sync'][remote_id] = []
        self_last_modif = datetime.datetime.strptime(self['last_modification_date'],'%Y-%m-%dT%H:%M:%S')
        remote_last_modif = datetime.datetime.strptime(data['last_modification_date'],'%Y-%m-%dT%H:%M:%S')
        sync_data = {'remote': {'ip': karacos.serving.get_request().remote_addr,
                                '_rev':data['_rev'],
                                'parent_id': data['parent_id'],
                                'base_id': data['base_id'],
                                'last_modification_date': data['last_modification_date']},
                    'local': {'_rev_before': self['_rev']}}
        # Drop system properties
        del data['_id']
        del data['_rev']
        del data['type']
        del data['ACL']
        del data['creator_id']
        del data['group_id']
        del data['base_id']
        del data['parent_db']
        del data['parent_id']
        del data['childrens']
        del data['creation_date']
        del data['last_modification_date']
        
        if 'sync' in data:
            del data['sync']
        
        if override or self_last_modif < remote_last_modif:
            self.update(data)
            self.save()
            result['status'] = 'success'
            result['message'] = _("Newer remote content, local content updated with new values")
        else:
            self.update(data,**self)
            self.save()
            result['status'] = 'success'
            result['message'] = _("Newer local content, local content updated with missing values")
        sync_data['local']['_rev_after'] = self['_rev']
        self['sync'][remote_id].append(sync_data)
        self.save()
        result['data'] = self
        return result
    
    def do_remote_authentication(self,remote_server,remote_user_id,remote_password):
        data = {'method':"login","id": 1, "params": {"email": remote_user_id,
                                                     "password": remote_password}}
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        handler = karacos.core.net.http.UrlHandler(http_timeout=3000)
        response = handler.processRequest(method="POST",url=remote_server,
                                          data=karacos.json.dumps(data),
                                          headers=headers)
        assert response.status == 200
        return response.getheader('set-cookie')
        
    @karacos._db.isaction
    def _synchronize_remote(self, remote_url=None, remote_user_id=None, remote_password=None): #, recursive=False, override=False):
        """
        Synchronizes the current node data with remote url
        """
        scheme, netloc, path, query, fragment = urlparse.urlsplit(remote_url)
        cookie = self.do_remote_authentication("%s://%s/"%(scheme,netloc),remote_user_id,remote_password)
        override=False
        data = {"method":"_sync", "id":1, "params": {"data":self, "override":override}}
        headers = {'Accept':'application/json', 'Content-Type':'application/json',
                   'Cookie': cookie}
        handler = karacos.core.net.http.UrlHandler(http_timeout=3000)
        response = handler.processRequest(method="POST",url=remote_url,
                                           data=karacos.json.dumps(data),headers=headers)
        if response.status == 200:
            return karacos.json.loads(response.read())
    _synchronize_remote.form = {'title': _("Synchronize with remote object"),
                                'submit': _('Synchronize'),
                                'fields': [{'name':'remote_url', 'title':_('Remote url'), 'dataType': 'TEXT'},
                                           {'name':'remote_user_id', 'title':_('Remote user Id'), 'dataType': 'TEXT'},
                                           {'name':'remote_password', 'title':_('Remote password'), 'dataType': 'TEXT'}] }
    _synchronize_remote.label = _("Synchronize with remote system")