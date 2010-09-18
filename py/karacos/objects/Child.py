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

import couchdb
import karacos

KcDocument = karacos.db['Document']
import logging
log = logging.getLogger("%s.ChildMeta" % __name__)

class ChildMeta(karacos.db['ParentMeta']):
    """
    metaclass for ChildObject
    """
    
    def __call__(self, *args, **kw):
        """
        A l'appel du constructeur
        """
        log.debug("BEGIN ChildMeta.__call__ ")
        assert 'data' in kw
        assert 'parent_id' in kw['data']
        assert 'parent_db' in kw['data']
        if 'parent' not in kw:
            parentbase = karacos.db.sysdb[kw['data']['parent_db']]
            log.debug("ChildMeta.__call__ parentbase = %s",parentbase)
            parent = parentbase.db[kw['data']['parent_id']]
            kw['parent'] = parent
        instance = karacos.db['ParentMeta'].__call__(self, *args, **kw)
        assert isinstance(instance.base,karacos.db['Base']), "'instance.base' attribute is not BaseObject"
        assert '__parent__' in dir(instance), "'parent' attribute not found"
        assert 'db' in dir(instance.__parent__), " parent's 'db' attribute not found"
        assert isinstance(instance.__parent__.db,couchdb.Database), "parent.db is not a couchdb Database object"
        log.debug("END ChildMeta.__call__ ")
        return instance

karacos.db['ChildMeta'] = ChildMeta

class Child(karacos.db['Parent']): 
    
    __metaclass__ = ChildMeta
       
    def __init__(self,*args, **kw):
        """
        """
        assert isinstance(self,karacos.db['Child']), "Icompatible type, instance is : %s, should be karacos.db['Child']" % type(self)
        assert type(self) != Child, "This type cannot be instanciated directly"
        self.__parent__ = None
        assert 'parent' in kw
        self.__parent__ = kw['parent']
        assert isinstance(self.__parent__,karacos.db['Parent']), "Child MUST have a parent"
        if 'base' not in self.__dict__ or self.base == None:
            self.base = self.__parent__.base
        self.db = self.base.db
        kw['base'] = self.base
        karacos.db['Parent'].__init__(self,*args, **kw)
        self.log.info("BEGIN Child.__init__ ")
        """
        if parent != None:
            assert isinstance(parent,KaraCos.Db.__parent__Object), "Incompatible value type : %s is not a KaraCos.Db.__parent__Object" % type(parent)
            self.__parent__ = parent
            self['parent_id'] = parent['_id']
            if self.base == None:
                self.db = parent.db
                self.base = parent.base
                self['base_id'] = parent['base_id']
        """
    def _rename(self,name):
        self._update_item()
        assert isinstance(name,basestring), "error, incorrect name"
        assert name != "", "name must be a string"
        assert name not in self.__parent__.__dict__, "error, reserved name" # TODO: test exposed and action methods, this is assertion for web view, not for pyapi
        assert name not in self.__parent__.__childrens__, "error, Node with that name exist"
        del self.__parent__.__childrens__[self['name']]
        self['name'] = name
        self.__parent__.__childrens__[self['name']] = self['id']
        self.save()
        self.__parent__.save()
    
        
        
    @karacos._db.isaction
    def rename(self,name=None):
        """
        """
        try:
            self._rename(name)
            return {'status':'success',
                            'message' : _("Element renomme avec succes"),
                         'data': {} }
        except Exception, e:
            return {'status':'failure', 'message' : '%s' % e.parameter,
                        'errors': None }
    
    #rename.form = forms._forms['rename']
    rename.label = _("Renommer")
           
    @karacos._db.isaction
    def get_parent(self):
        """
        parent is unique reference
        """
        return self.__parent__