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

Created on 3 dec. 2009

@author: nico
'''
from logging import getLogger
log = getLogger(__name__)
import karacos

#KaraCosObject = KaraCos.Db.KaraCosObject
from uuid import uuid4
import sys


class Node(karacos.db['Child']):
    """
    Single node
    """
    
    @staticmethod
    def create(parent=None, base=None,data=None):
        """
        """
        assert parent != None, "parent should be specified"
        assert isinstance(parent,karacos.db['Parent'])
        assert data != None
        assert isinstance(data,dict)
        assert isinstance(data['name'],basestring)
        assert data['name'] != ""
        assert not parent.child_exist(data['name'])
        #assert parent != None, "at least one of parent or base parameter must be specified"
        log.info("Node.create for %s" % data['name'])
        doc_id = "%s" % uuid4().hex
        if base == None or base == False:
            base = parent.base
        username = karacos.serving.get_session()['username']
        result = { 'parent_id': parent['_id'],
                   'parent_db': parent.__parent__.base.id,
                   'base_id': base.id,
                   'creator_id': username, 
                   'owner_id': username
                 }
                    
        for k,v in data.items():
            result[k] = v
        if 'type' not in result:
            result['type'] = 'Node'
        parent.base.db[doc_id] = result
        result = parent.base.db[doc_id]
        parent.add_child(result)
        return result
    
    
    def __init__(self, *args, **kw):
        """
        """
        self.log.debug("Node.__init__ ")
        data = None
        if 'data' in kw:
            data = kw['data']
        assert isinstance(data,dict), "Incompatible data type : %s is not a KcDocument" % type(data)
        assert isinstance(data['name'],basestring)
        
        assert isinstance(data['parent_id'],basestring)
        assert isinstance(data['base_id'],basestring)
        
        karacos.db['Child'].__init__(self,*args, **kw)
        self.__domain__ = self.__parent__.__domain__
    
    def _add_attachment(self, att_file=None):
        self._update_item()
        self.__parent__.db.put_attachment(self, att_file.file.read(), unicode(att_file.filename))
        self._update_item()
        return {"status":"success", "message": "%s"}
    
    @karacos._db.isaction
    def add_attachment(self, att_file=None):
        #size = 0
        #while True:
        #    data = att_file.file.read(8192)
        #    if not data:
        #        break
        #    size += len(data)
        return self._add_attachment(att_file)
        
    add_attachment.form = {'title': _("upload file"),
         'submit': _('Upload'),
         'fields': [{'name':'att_file', 'title':'Fichier','dataType': 'FILE'}]}

    
    @karacos._db.isaction
    def reset_admin_ACL(self):
        self._update_item()
        admin = self.__domain__.get_user_by_name(username='admin@%s' % self.__domain__['name'])
        self['ACL'][admin.get_auth_id()] = self.get_actions()
        self.save()
        return {'status':'success', 'message':_("adm actions reset"),'data':''}
    
    def _delete(self):
        """
        """
        #self.base = KaraCos.Db.sysdb[self['_id']]
        #KaraCos.Db.sysdb.delete(self.base)
        #self = self.__parent__.db[self['_id']]
        self.log.debug(" Object delete : %s" % self)
        
        for child in self.__childrens__:
            try:
                self.get_child_by_name(child).delete()
            except Exception, e:
                self.log.log_exc(sys.exc_info(),'error')
        if self['base_id'] != self.__parent__['base_id']:
            self.base.delete()
        
        del self.__parent__.base.db[self['_id']]
        del self.__parent__['childrens'][self['name']]
        self.__parent__.save()
        del self
    @karacos._db.isaction
    def delete(self):
        self._delete()