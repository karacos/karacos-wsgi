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
    
    
Created on 12 dec. 2009
@author: nico
'''
import os
from karacos.lib import static

__author__="Nicolas Karageuzian"
__contributors__ = []

import sys
import karacos
import traceback



class WebNode(karacos.db['Node']):
    
    __metaclass__ = karacos.db['WebMeta']
    
    @karacos._db.isaction
    def reset_admin_ACL(self):
        self._update_item()
        admin = self.__domain__.get_user_by_name(username='admin@%s' % self.__domain__['name'])
        self['ACL'][admin.get_auth_id()] = self.get_actions()
        self.save()
        return {'status':'success', 'message':_("adm actions reset"),'data':''}
    
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'WebNode'
        if 'type' not in data:
            data['type'] = 'WebNode'
        assert 'name' in data
        result = karacos.db['Node'].create(parent=parent,base=base,data=data)
        # parent.get_child_by_name(data['name'])
        fullaccess = []
        result.log.info("Actions for %s : %s" % (result['name'],result.get_actions()))
        for action in result.get_actions():
            if action not in ['login','register']:
                fullaccess.append(action)
        if not result.__domain__.get_user_auth().get_auth_id().startswith("user.anonymous"):
            result['ACL'][result.__domain__.get_user_auth().get_auth_id()] = fullaccess
        result['ACL']["user.admin@%s" % result.__domain__['name']] = fullaccess
        try:
            acl_update = result.__domain__._get_ACL_default_update()
            result.log.info("Updating ACL with %s " % acl_update)
            for a_cl in acl_update.keys():
                if a_cl not in result['ACL']:
                    result['ACL'][a_cl] = []
                for a_auth_action in acl_update[a_cl]:
                    result['ACL'][a_cl].append(a_auth_action)
        except:
            result.log.info("problem while setting ACL")
        result.save()
        return result
    
    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent.__domain__,karacos.db['Domain']), "domain is %s, should be Domain" % parent.__domain__.__class__
        self.__domain__ = parent.__domain__
        karacos.db['Node'].__init__(self,parent=parent,base=base,data=data)
    
    @karacos._db.isaction
    def get_user_actions_forms(self):
        return self._get_user_actions_forms()

    @karacos._db.isaction
    def index(self):
        """
        Default index for app
        """
        return False
    def get_instance_template_uri(self):
        uri = ""
        try:
            uri = "%s/%s" % (self.__domain__.get_site_theme_base(),self['WebType'])
            template = self.__domain__.lookup.get_template(uri)
        except:
            try:
                self.log.log_exc(sys.exc_info(),'info')
                uri = "/default/%s" % self['WebType']
                template = self.__domain__.lookup.get_template(uri)
            except:
                try:
                    self.log.log_exc(sys.exc_info(),'info')
                    uri = "%s/WebNode" % self.__domain__.get_site_theme_base()
                    template = self.__domain__.lookup.get_template(uri)
                except:
                    uri = "/default/WebNode"
        self.log.info("Using template %s" % uri)
        return uri
    
    def get_relative_uri(self):
        instance = self
        result = ''
        while not isinstance(instance,karacos.db['Domain']):
            result = '%s/%s' % (instance['name'],result)
            instance = instance.__parent__
        return result[:-1] # strop off trailing / added
    
    def get_site_template_uri(self):
        instance = self
        result = ''
        while 'site_template_uri' not in instance.__dict__ and not isinstance(instance,karacos.db['Domain']):
            instance = instance.__parent__
        if isinstance(instance,karacos.db['Domain']):
            return self.__domain__.get_site_template_uri()
        return instance.site_template_uri
    

        
    @karacos._db.isaction
    def create_child_node(self,name=None,type=None,base=False):
        """
        Creates a child Node.
        As an web exposed Method, this will only allow to create WebNode derived objects
        """
        try:
            assert name != None
            assert type != None
            data = {'name':name}
            node = self._create_child_node(data=data, type=type, base=base)
            return {'status':'success', 'message': _("Node cree avec succes"), 'data':node}
        except Exception, e:
            return {'status':'failure', 'message' : '%s' % e,
                        'trace': traceback.format_exc().splitlines() }
    create_child_node.form = {'title': _("Creer un element"),
         'submit': _('Creer'),
         'fields': [{'name':'name', 'title':_('Nom de la resource'),'dataType': 'TEXT'},
                    {'name':'type', 'title':_("Type d'objet"),'dataType': 'TEXT'},
                    {'name':'base', 'title':_('Base'),'dataType': 'TEXT'},
                 ] }
    #create_child_node.label = _("Creer un noeud")
    
    def _serve_att(self,name):
        att_filename = os.path.join(self.get_att_dir(),name)
        if os.path.exists(att_filename):
            att_url = '/_atts/%s/%s' % (self.id, name)
            raise karacos.http.Redirect(url=att_url, code=301)
        raise karacos.http.NotFound(message=_("Ressource introuvable '%s'") % name)
    @karacos._db.isaction
    def _att(self,*args,**kw):
        response = karacos.serving.get_response()
        if len(args) == 0:
            # TODO templating
            res = '<ul>'
            for file in os.listdir(self.get_att_dir()):
                res = '%s<li><a href="%s/_att/%s">%s</a></li>' % (res,self._get_action_url(),file,file)
            res = '%s</ul>' % res
            response.body = '%s' % res
            return
        else:
            name=args[0]
            self._serve_att(name)
    
    @karacos._db.isaction
    def set_ACL(self, ACL=None):
        self['ACL'] = karacos.json.loads(ACL)
        self.save()
    
    def _set_ACL_form(self):
        return {'title': _("Modifier l'ACL"),
         'submit': _('Modifier'),
         'fields': [{'name':'ACL', 'title':'ACL','dataType': 'TEXT','formType': 'TEXTAREA', 'value': karacos.json.dumps(self['ACL'])}]}
    #set_ACL.label = "Edit ACL"
    set_ACL.get_form = _set_ACL_form
    def _publish_node(self):
        self['ACL']['group.everyone@%s' % self.__domain__['name']] = ["get_user_actions_forms","w_browse","index"]
        self['is_node_published'] = True
        self.save()
    @karacos._db.isaction
    def publish_node(self):
        """
        Make this node public for everyone
        """
        self._publish_node()
        return {'status': 'success', 'message': _('WebNode is public now')}
    
    @karacos._db.isaction
    def add_attachment(self, *args, **kwds):
        assert 'att_file' in kwds
        request = karacos.serving.get_request()
        
        result = self._add_attachment(request.POST.get('att_file'))
        if 'return_json' in kwds:
            request.headers['Accept'] = 'application/json'
            response = karacos.serving.get_response()
            response.headers['Content-Type'] = 'text/html'
            response.__headers_type_set__ = True
        #size = 0
        #while True:
        #    data = att_file.file.read(8192)
        #    if not data:
        #        break
        #    size += len(data)
        return result
        
    add_attachment.form = {'title': _("upload file"),
         'submit': _('Upload'),
         'fields': [{'name':'att_file', 'title':'Fichier','dataType': 'FILE'}]}
    add_attachment.label = _("Attacher un fichier")
    
    @karacos._db.isaction
    def delete_child(self,childname=None):
        assert childname != None
        child = self.get_child_by_name(childname)
        child.delete()