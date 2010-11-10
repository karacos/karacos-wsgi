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
         if (doc.type == "Base" && doc._id == "%s")
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
        log.debug("BEGIN Base.get_by_name : %s" % name)
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
        self.log = karacos.core.log.getLogger(self)
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
        
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def __search_name__(self,name):
        """ // %s first param, unused
        function(doc) {
            var tokens;
            if (doc.name) {
                re = new RegExp("%s");
                if (doc.name.match(re)) {
                    emit(doc._id, doc);
                }
            }
        }
        """
    
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def __search_file__(self,name):
        """// %s first param, unused
        function(doc) {
            re = new RegExp("%s");
            if (doc.name) {
                
                if (doc.name.match(re)) {
                    emit(doc._id, doc);
                    if (doc.k_atts) {
                        for (name in doc.k_atts) {
                            emit(doc._id,{'file_name':name, 'stats':doc.k_atts[name]});
                        }
                    }
                }
            }
            if (doc.k_atts) {
            for (name in doc.k_atts) {
                if (name.match(re)) {
                    emit(doc._id,{'file_name':name, 'stats':doc.k_atts[name]});
                }
            }
            }
        }
        """
    @karacos._db.ViewsProcessor.isview('self', 'javascript')
    def __get_sub_dbs__(self):
        """
        function(doc) {
            if (doc.base_id) {
                if ( doc.base_id != '%s') {
                    emit(doc.base_id, doc.base_id);
                }
            }
        }
        """
    
    def _search_name(self,name=None):
        found = self.__search_name__(name)
        result = {}
        for item in found:
            item_obj = self.db[item.key]
            if 'type' in item.value:
                result[item_obj._get_action_url()] = { "url": "http://%s%s" % (item_obj.__domain__['fqdn'],item_obj._get_action_url()),
                                                  'type':'folder',
                                                  'objectType':'folder',
                                                  'name': item_obj['name']}
                result.update(item_obj._search_get_childs())
            else:
                obj_id = "%s/%s" % (item_obj._get_action_url(),item.value['file_name'])
                result[obj_id]= { "url": "http://%s%s" % (item_obj.__domain__['fqdn'],obj_id),
                                                  'type':'file',
                                                  'objectType':'file',
                                                  'fileType':item.value['stats']['type'],
                                                  'fileSize':item.value['stats']['size'],
                                                  'name': item_obj['name']}
        sub_dbs = self.__get_sub_dbs__()
        for db in sub_dbs :
            db_obj = karacos.db.sysdb[db.key]
            result.update(db_obj._search_name(name))
        return result #json.dumps(result)
    
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