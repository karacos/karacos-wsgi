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

Created on 2 dec. 2009

@author: nico
'''
import karacos
import hashlib
import sys

class User(karacos.db['Node']):
    """
    Un user.
    parametres : domaine, name, base=None
    """
    __metaclass__ = karacos.db['AuthMeta']

    @staticmethod
    def create(parent=None, base=None,data=None):
        result = karacos.db['Node'].create(parent=parent,base=base,data=data)
        return result
    
    @staticmethod
    def hash_pwd(password):
        """
        Tool func password hash
        """
        m = hashlib.sha224()
        m.update(password)
        return m.hexdigest()
    
    def __init__(self, *args, **kw):
        """
        """
        assert 'parent' in kw
        parent = kw['parent']
        karacos.db['Node'].__init__(self,*args, **kw)
    
    def _get_email(self):
        if 'email' in self:
            return self['email']
        else:
            if karacos.core.mail.valid_email(self['name']):
                self['email'] = self['name']
            else:
                self['email'] = None
            self.save()
            return self['email']
    
    def _set_email(self, email):
        assert karacos.core.mail.valid_email(email)
        self['email'] = email
        self.save()
        return {'success': True, 'message': "Email is now registered"}
    
    def get_auth_id(self):
        """
        """
        return "user.%s" % self['name']
    
    def set_password(self,password):
        """
        """
        self['password'] = "%s" % User.hash_pwd(password)
        try:
            self.db[self.id] = self
        except:
            self.log.log_exc(sys.exc_info(),'warn')
            
    def belongs_to(self,group):
        """
        check if user is member of group
        """
        return group.is_member(self)
    
    def pseudo(self):
        if 'pseudo' not in self:
            return self['name'].split('@')[0]
        return self['pseudo']
    
    def get_groups(self):
        """
        """
        return self['groups']