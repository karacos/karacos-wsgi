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


Created on 27 nov. 2009

@author: nico
'''
from logging import getLogger
log = getLogger(__name__)
import datetime
import karacos
import sys
from uuid import uuid4
KcDocument = karacos.db['Document']

class Base(KcDocument):
    """
    DB Descriptor - intented to store metadb info in menestrel
    Does not represents DB itself
    attribute db holds reference to the physical object DB
    'data' contains :
     * dbName (String Mandatory) - name of db in system
     * title (String optional)
     * description (String optional)
    may not contains childrens
    """
    db = karacos.db.sysdb
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_by_id(base_id):
        """
        function(doc) {
         if (doc.type == "BaseObject" && doc._id == "%s")
          emit(doc._id, doc);
        }
        """
         
    @staticmethod
    def get_by_id(base_id=None):
        log.debug("BEGIN BaseObject.get_by_name : %s" % base_id)
        assert isinstance(base_id,basestring), "Parameter name must be string"
        result = None
        try:
            dbs = Base._get_by_id(base_id)
            assert dbs.__len__() <= 1, "BaseObject.get_by_name : More than one db with that name in system DB"
            if dbs.__len__() == 1:
                for db in dbs:
                    log.debug("BaseObject.get_by_name : db.key = %s db.value = %s" % (db.key,db.value) )
                    result = karacos.db.sysdb[db.key]
        except Exception, e:
            log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_by_name(name):
        """
        function(doc) {
         if (doc.type == "Base" && doc.name == "%s")
          emit(doc._id, doc);
        }
        """ 
    
    @staticmethod
    def get_by_name(name=None):
        log.debug("BEGIN BaseObject.get_by_name : %s" % name)
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        try:
            dbs = Base._get_by_name(name)
            assert dbs.__len__() <= 1, "BaseObject.get_by_name : More than one db with that name in system DB"
            if dbs.__len__() == 1:
                for db in dbs:
                    #KaraCos._Db.log.debug("BaseObject.get_by_name : db.key = %s db.value = %s" % (db.key,db.value) )
                    result = karacos.db.sysdb[db.key]
        except Exception, e:
            log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e
        return result

    
    @staticmethod
    def exist(name=None):
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        
        dbs = Base._get_by_name(name)
        try:
            assert dbs.__len__() <= 1, "More than one db with that name in system DB"
            if dbs.__len__() == 1:
                if unicode(name) in karacos.db.server:
                    return True
                else:
                    raise karacos._db.Exception,"ALERT BOG BOG BOG ALERT"
            else:
                return False
        except Exception, e:
            log.log_exc(sys.exc_info(),'error')
            raise karacos._db.Exception, e


    @staticmethod
    def create(name):
        assert isinstance(name,basestring), "Parameter name must be string"
        result = None
        if name != karacos.db.sysdb_name:
            #assert name not in KaraCos.Db.server
            assert not Base.exist(name), "Base already exist with the same name"
            karacos.db.server.create(unicode(name))
        doc_id = "%s" % uuid4().hex
        log.debug("BASE doc_id : %s" % doc_id)
        result = { 'name': unicode(name),
                 'type': 'Base'
                }
        karacos.db.sysdb[doc_id] = result
        log.debug("Retrieving BASE doc_id : %s" % doc_id)
        result = karacos.db.sysdb[doc_id]
        result.log.debug("create : result type : %s", type(result) )
        return result
    
    
    def __init__(self,*args, **kw):
        data = None
        if 'data' in kw:
            data = kw['data']
        assert isinstance(data,dict), "Incompatible data type : %s is not a KcDocument" % type(data)
        assert isinstance(data[u'name'],basestring), "dbName should be String"
        self.log.debug("BEGIN Base __init__")# : %s" % data.items())
        karacos.db['Document'].__init__(self,data=data)
        self.log.debug("Base __init__ : %s" % self)
        self.db = karacos.db.server[self['name']]
        self.base = self
        self.log.debug("END Base __init__ : %s" % self)
        

    def set_title(self,title):
        """
        Set DB title
        """
        self['data']['title'] = title
    
    def set_description(self,description):
        """
        Set DB description
        """
        self['data']['description'] = description
    
    def validate(self):
        """
        Validate object Data
        """
        if self.__contains__('childrens'):
            raise self.Exception, "valueError: 'childrens' : May not contains childs"
        
        KcDocument.basic_validations(self)
        #if not self.__contains__('data'):
        #    raise self.Exception, "valueError: 'data' : type is not a dict"
        if not self.__contains__('name'):
            raise self.Exception, "valueError: 'name' : dict entry not found"
        if self['name'] == None:
            raise self.Exception, "valueError: 'name' : dbName is null"
        self['name'] = unicode(self['name'])
        assert isinstance(self['name'],basestring), "valueError: 'data.dbName' : type is not String"
        #if self['data'].__contains__('title'):
        #    if isinstance(self['data']['title'],basestring):
        #        raise self.Exception, "valueError: 'data.title' : type is not String"
        #if self['data'].__contains__('title'):
        #    if isinstance(self['data']['description'],basestring):
        #        raise self.Exception, "valueError: 'data.title' : type is not String"
    
    
    def delete(self):
        """
        """
        #self.base = KaraCos.Db.sysdb[self['_id']]
        #KaraCos.Db.sysdb.delete(self.base)
        self._update_item()
        self.log.debug(" Base delete : %s" % self)
        del karacos.db.sysdb[self['_id']]
        del karacos.db.server[str(self[u'name'])]
        del self
        
#KaraCos.Db.BaseObject = BaseObject  