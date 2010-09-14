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
#import hashlib
import sys

class Group(karacos.db['Node']):
    """
    Un groupe.
    parametres : domaine, name, base=None
    """
    
    
    
    __metaclass__ = karacos.db['AuthMeta']
    
    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        result = karacos.db['Node'].create(parent=parent,base=base,data=data,owner=owner)
        return result
    
    def __init__(self,parent=None,data=None,base=None):
        """
        
        """
        #assert isinstance(parent,KaraCos.Db.Domain), "Icompatible type, parent has to be KaraCos.Db.Domain"
        
        KaraCos.Db.Node.__init__(self,parent=parent,base=base,data=data)
        
    def get_auth_id(self):
        """
        """
        return "group.%s" % self['name']
    
    def add_user(self,user):
        """
        """
        assert isinstance(user,karacos.db['User'])
        if user['name'] not in self['users']:
            self['users'][user.get_auth_id()] = user.id
            user['groups'].append(self.get_auth_id())
            user.save()
            self.save()

    def is_member(self,user):
        """
        """
        if user.get_auth_id() in self['users']:
            return True
        
        return False

    def remove_user(self,user):
        """
        """
        assert isinstance(user,karacos.db['User'])
        if user.get_auth_id() in self['users']:
            del self['users'][user.get_auth_id()]
            user['groups'].remove(self.get_auth_id())
        
        self.save()