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
__author__ = "Nicolas Karageuzian"
import couchdb
import karacos
import sys, datetime
KcDocument = karacos.db['Document']
import simplejson as json

class ParentMeta(karacos.db['KcDocMeta']):
    """
    metaclass of a parentObject
    """
    
    def __call__(self, *args, **kw):
        """
        A l'appel du constructeur
        le type doit avoir une base (KcDocument) et un objet db (objet couchdb)
        """
        self.log.debug("begin __call__")
        instance = karacos.db['KcDocMeta'].__call__(self, *args, **kw)
        instance.log.debug("__call__ dir(instance):'%s'" % dir(instance))
        assert "db" in dir(instance), "'db' attribute not found"
        assert isinstance(instance.db, couchdb.Database), "db is not a couchdb Database object"
        assert 'base' in dir(instance), "'base' attribute not found"
        assert isinstance(instance.base, karacos.db['Base']), "'db' attribute is not Base"
        assert 'base_id' in instance
        if 'childrens' not in instance:
            instance['childrens'] = dict()
            try:
                #Sauvegarde objet modifie
                instance.__parent__.db[instance['_id']] = instance
            except:
                self.log.log_exc(sys.exc_info(), 'warn')
        self.log.debug("end __call__")
        return instance
            
karacos.db['ParentMeta'] = ParentMeta

class Childrens(dict):
    parent = None
    def __init__(self, parent):
        """
        """
        self.__parent__ = parent
    
    def __delitem__(self, name):
        assert isinstance(name, basestring)
        assert name in self.__parent__['childrens'], "%s" % name
        del self.__parent__['childrens']['name']
        self.__parent__.save()
    
    def __setitem__(self, name, value):
        assert isinstance(value, basestring)
        assert isinstance(name, basestring)
        assert value in self.__parent__.db
        self.__parent__['childrens'] = value
        self.__parent__.save()
    
    def __getitem__(self, name):
        assert self.__parent__.child_exist(name), "KeyError, does't exist"
        result = self.__parent__.get_child_by_name(name)
        return result
    
    def __contains__(self, name):
        if name in self.__parent__['childrens']:
            return True
        else:
            return False
    def __iter__(self):
        """
        """
        return self.__parent__['childrens'].__iter__()
    def keys(self):
        return self.__parent__['childrens'].keys()
    def values(self):
        return self.__parent__['childrens'].values()
    def items(self):
        return self.__parent__['childrens'].items()

class Parent(KcDocument):
    """
    Un type pour un objet contenant d'autres objets
    Doit avoir au moins parent ou une base, peut avoir les 2
    """
    __metaclass__ = karacos.db['ParentMeta']

    __childrens__ = None

    def __init__(self, *args, **kw):
        self.log.debug("Parent.__init__ START")
        assert isinstance(self, karacos.db['Parent']), "Icompatible type, instance is : %s, should be karacos.db['Parent']" % type(self)
        assert type(self) != Parent, "This type cannot be instanciated directly"
        assert 'data' in kw
        data = kw['data']
        #localvars = locals()
        base = None
        """
        if 'parent_id' in data:
            #parent = 
            parent = kw['parent']
        """
        if kw.__contains__('base'):
            base = kw['base']
        
        if 'base_id' in data:
            ""
            base = karacos.db.sysdb[data['base_id']]
            #self.base = base
        
              
        #assert base != None or parent != None, "at least one of parent or base parameter must be specified"
        
        
        if base != None:
            assert isinstance(base, karacos.db['Base']), "Incompatible value type : %s is not a karacos.db['BaseObject']" % type(base)
            self.base = base
            self.db = base.db
            self['base_id'] = base['_id']
        

        
        karacos.db['Document'].__init__(self, data=data)
        self.__childrens__ = Childrens(self)
        self.log.debug("Parent.__init__ END: %s" % self.__dict__)
        
    def add_child(self, child):
        """
        Parents may have childs from multiple locations
        """
        assert isinstance(child, karacos.db['Child']), "child is %s, should be %s" % (type(child), karacos.db['Child'])
        #assert self['base_id'] == child['base_id'], "child is not in parent's base, Feature not implemented yet"
        #self.childrens.append(child)
        #self = self.__parent__.db[self.id]
        self._update_item()
        if 'childrens' not in self:
            self['childrens'] = {}
        self['childrens'][child['name']] = child['_id']
        self.save()
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_web_childrens(self):
        """
        function(doc) {
         if (doc.parent_id == "%s" && doc.WebType && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc.name);
        }
        """
    
    def get_web_childrens(self):
        """
        """
        results = self._get_web_childrens()
        result = {}
        for item in results:
            result[item.key] = item.value
        return result

    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_childs_list(self):
        """
        function(doc) {
         if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc.name);
        }
        """
    
    @karacos._db.isaction
    def get_childs_list(self):
        childs = self._get_childs_list()
        result = {}
        for child in childs:
            result[child.key] = child.value
        return json.dumps(result)
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_childrens_of_type(self, type):
        """
        function(doc) {
         if (doc.parent_id == "%s" && doc.type == "%s" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc.name);
        }
        """
    def get_childrens_of_type(self, type):
        return self._get_childrens_of_type(type)
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_child_by_name(self, name):
        """
        function(doc) {
         if (doc.parent_id == "%s" && doc.name == "%s" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc);
        }
        """
    def get_child_by_name(self, name):
        ""
        self.log.info("BEGIN get_child_by_name : %s" % name)
        assert isinstance(name, basestring), "Parameter name must be string"
        result = None
        try:
            childs = self._get_child_by_name(name)
            assert childs.__len__() <= 1, "get_child_by_name : More than one child with that name in DB"
            if childs.__len__() == 1:
                for child in childs:
                    self.log.info("get_child_by_name : db : %s db.key = %s" % (self.db, child.key))
                    result = self.db[child.key]
        except Exception, e:
            self.log.log_exc(sys.exc_info(), 'warn')
            #raise karacos._db.DbException, e
        return result
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_child_by_id(self, id):
        """
        function(doc) {
         if (doc.parent_id == "%s" && doc._id == "%s" && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc);
        }
        """
    def get_child_by_id(self, id):
        ""
        self.log.info("BEGIN get_child_by_id : %s" % id)
        assert isinstance(id, basestring), "Parameter id must be string"
        result = None
        try:
            childs = self._get_child_by_id(id)
            assert childs.__len__() <= 1, "get_child_by_name : More than one child with that name in DB"
            if childs.__len__() == 1:
                for child in childs:
#                    karacos._db.log.debug("get_child_by_name : db.key = %s db.value = %s" % (child.key,domain.value) )
                    result = self.db[child.key]
        except Exception, e:
            self.log.log_exc(sys.exc_info(), 'warn')
            #raise karacos._db.DbException, e
        return result
    
    def child_exist(self, name):
        assert isinstance(name, basestring), "Parameter name must be string"
        if name in self.__childrens__:
            return True
        else:
            return False

    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_web_childrens_id_for_id(self, userid, groups):
        """
        function(doc) {
         parent = "%s";
         userid = "%s";
         groups = %s;
         
         if (doc.parent_id == parent && doc.WebType && !("_deleted" in doc && doc._deleted == true)) {
            emitdoc = false ;
            for(var i = 0; i <= groups.length; i++)
                if (doc.ACL[groups[i]])
                    if (doc.ACL[groups[i]].join().search(/w_browse/) != -1)
                        emitdoc = true;
            if (doc.ACL[userid])
                if (doc.ACL[userid].join().search(/w_browse/) != -1)
                    emitdoc = true;
            if (emitdoc) {
                emit(doc.name,doc._id);
                }
            }
        }
        """

    def get_web_childrens_objects_for_id(self):
        """
        """
        userid = self.__domain__.get_user_auth()
        results = self._get_web_childrens_id_for_id(userid.get_auth_id(), json.dumps(userid.get_groups()))
        result = {}
        for item in results:
            result[item.key] = self.db[item.value]
        return result

    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def _get_web_childrens_for_id(self, userid, groups):
        """
        function(doc) {
         parent = "%s";
         userid = "%s";
         groups = %s;
         if (doc.parent_id == parent && doc.WebType && !("_deleted" in doc && doc._deleted == true)) {
            emitdoc = false ;
            for(var i = 0; i <= groups.length; i++)
                if (doc.ACL[groups[i]])
                    if (doc.ACL[groups[i]].join().search(/w_browse/) != -1)
                        emitdoc = true;
            if (doc.ACL[userid])
                if (doc.ACL[userid].join().search(/w_browse/) != -1)
                    emitdoc = true;
            if (emitdoc) {
                var doclabel = ""
                if (doc.label)
                    doclabel = doc.label
                else
                    doclabel = doc.name
                emit(doc.name,doclabel);
                }
            }
        }
        """
    
    
    def get_web_childrens_for_id(self):
        """
        """
        userid = self.__domain__.get_user_auth()
        results = self._get_web_childrens_for_id(userid.get_auth_id(), json.dumps(userid.get_groups()))
        result = {}
        for item in results:
            result[item.key] = item.value
        return result

    @karacos._db.isaction
    def w_browse(self):
        return self.get_web_childrens_for_id()
        

    def _create_child_node(self, *args, **kw): #data=None,type=None,base=False):
        assert 'data' in kw
        data = kw['data']
        assert isinstance(data, dict)
        assert 'name' in data
        assert 'type' in kw
        type = kw['type']
        del kw['type']
        assert isinstance(type, basestring)
        assert type in karacos.db.keys(), _("Type n'existe pas")
        assert issubclass(karacos.db[type], karacos.db['Child']), _("Type incorrect")
        assert data['name'] not in self.__childrens__, _("Node existe avec ce nom")
        base = self.base
        if 'base' in kw:
            if base == "true":
                base_name = "base_%s" % uuid4().hex
                base = karacos.db['Base'].create(base_name.lower())
        kw['base'] = base
        kw['owner'] = self.__domain__.get_user_auth()
        kw['parent'] = self
        self._update_item()
        node = karacos.db[type].create(*args, **kw)
        #node['ACL'] = {"user.admin@%s" % self.__domain__['name']: node.get_actions(),
        #               self.__domain__.get_user_auth().get_auth_id(): node.get_actions() }
        node.save()
        return node

        
