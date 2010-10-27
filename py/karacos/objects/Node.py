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
import os
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
        data = None
        if 'data' in kw:
            data = kw['data']
        assert isinstance(data,dict), "Incompatible data type : %s is not a KcDocument" % type(data)
        assert isinstance(data['name'],basestring)
        
        assert isinstance(data['parent_id'],basestring)
        assert isinstance(data['base_id'],basestring)
        
        karacos.db['Child'].__init__(self,*args, **kw)
        self.log.debug("Node.__init__ ")
        self.__domain__ = self.__parent__.__domain__
    
    def _add_attachment(self, att_file=None,base64=False):
        request = karacos.serving.get_request()
        new_file_name = os.path.join(self.get_att_dir(),att_file.filename)
        new_file = open(new_file_name,'wb')
        self.log.info(request.headers)
        if base64:
            import base64
            if 'file' in dir(att_file):
                new_file.write(base64.b64decode(att_file.file.read()))
            elif 'file_body'in dir(att_file):
                new_file.write(base64.b64decode(att_file.file_body))
        else:
            if 'file' in dir(att_file):
                new_file.write(att_file.file.read())
            elif 'file_body'in dir(att_file):
                new_file.write(att_file.file_body)
        new_file.flush()
        new_file.close()
        return {"success":True,"status":"success", "data": "%s/_att/%s" % (self._get_action_url(),att_file.filename),#"/_atts/%s/%s"%(self.id,att_file.filename),
                "message": "%s has been successfully writen" % att_file.filename }
    def get_att_dir(self):
        att_dirname = os.path.join(karacos._srvdir,'_atts',self.id)
        if not os.path.exists(att_dirname):
            os.makedirs(att_dirname)
        return att_dirname
    
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