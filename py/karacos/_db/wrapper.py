'''
    KaraCos - web platform engine - http://karacos.org/
    Copyright (C) 2009-2010  Nicolas Karageuzian - Cyril Gratecis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on 8 dec. 2009

@author: nico
'''
import exceptions
import httplib2
import mimetypes
from urllib import quote, urlencode
from types import FunctionType
from inspect import getsource
from textwrap import dedent
import re
import socket
import couchdb.client
import karacos




class Server(couchdb.client.Server):
    """
    Our couchDB server
    """
    cache = {}
    def __getitem__(self, name):
        """Return a `Database` object representing the database with the
        specified name.

        :param name: the name of the database
        :return: a `Database` object representing the database
        :rtype: `Database`
        :raise ResourceNotFound: if no database with that name exists
        """
        db = None
        if name in self.cache:
            db = self.cache[name]
        else:
            db = DataBase("%s/%s"%(self.resource.url, name), couchdb.client.validate_dbname(name),
                          session=self.resource.session)
            db.resource.head() # actually make a request to the database
            self.cache[name] = db
        return db
    

class DataBase(couchdb.client.Database):
    """
    """
    cache = {}
    def __init__(self, url, name=None, session=None):
        """
        """
        couchdb.client.Database.__init__(self, url, name=None, session=None)
        self.log = karacos.core.log.getLogger(self)
    
    def __delitem__(self, id):
        """Remove the document with the specified ID from the database.

        :param id: the document ID
        """
        aaa,resp, data = self.resource.head(id)
        self.log.info("COUCHDB COMMAND 'DELETE' [%s]" % id)
        self.resource.delete(id, rev=resp['etag'].strip('"'))
        del self.cache[id]
    
    def reset_cache(self,id):
        if id in self.cache:
            del self.cache[id] 
    
    def refresh_item(self,item):
        self.log.info("COUCHDB COMMAND 'GET' [%s]" % item.id)
        aaa, resp, data = self.resource.get_json(item.id)
        item.update(data)
    
    def __getitem__(self, id):
        """Return the document with the specified ID.

        :param id: the document ID
        :return: a `Row` object representing the requested document
        :rtype: `Document`
        """
        if id in self.cache.keys():
            self.log.debug("'%s' found in cache, serving memory object" % id)
            return self.cache[id]
        else:
            self.log.info("COUCHDB COMMAND 'GET' [%s]" % id)
            aaa,resp, data = self.resource.get_json(id)
            self.cache[id] = data
            #KaraCos._Db.log.debug("BASE GET ITEM DATA : %s" %data)
            document = None
            hasDocument = type = WebType = False
            assert isinstance(data,dict)
            if 'type' in data:
                assert isinstance(data['type'],basestring), "type must be a String"
                if data['type'] in karacos.db.keys():
                    type = True
            if 'WebType' in data:
                assert isinstance(data['WebType'],basestring), "WebType must be a String"  
                if data['WebType'] in karacos.webdb.keys():
                    WebType = True
                

            if type and not WebType:
                self.log.debug("type and not webtype, instanciating in '%s'" % data['type'])
                #KaraCos._Db.log.info("BASE GET ITEM type : %s BEGIN" % data)
                document = karacos.db[data['type']](data=data,base=self)
                hasDocument = True
            if type and WebType:
                self.log.debug("type and WebType, instanciating in '%s'" % data['WebType'])
                document = karacos.webdb[data['WebType']](data=data,base=self)
                hasDocument = True
            if not hasDocument:
                self.log.debug("Type not found or no type found, instanciating Document with data '%s'" % data)
                document = couchdb.client.Document(data)
            #KaraCos._Db.log.debug("BASE GET ITEM RESULT : %s" %document)
            self.cache[id] = document
            return document
    
    def __setitem__(self, id, content):
        """Create or update a document with the specified ID.

        :param id: the document ID
        :param content: the document content; either a plain dictionary for
                        new documents, or a `Row` object for existing
                        documents
        """
        self.log.debug("start __setitem__ '%s'[%s]" % (id,content))
        try: 
            self.log.info("COUCHDB COMMAND 'GET' [%s]" % id)
            aaa,resp, data = self.resource.get_json(id)
            document = couchdb.client.Document(data)
            if self.cache[id].rev != document.rev:
                raise karacos._db.Exception("document update conflict")
            self.log.debug("Resource exists, processing update in couchdb")
        except:
            self.log.debug("Resource doesn't exists, processing creation in couchdb")
#        content = unicode(karacos.json.dumps(content))
        self.log.info("COUCHDB COMMAND 'PUT' [%s]" % id)
        aaa,resp,data = self.resource.put_json(id, body=content)
        content.update({'_id': data['id'], '_rev': data['rev']})
        if id in self.cache:
            del self.cache[id]
            
    def view(self, name, wrapper=None, **options):
        """
        Cop/coll for view method.
        do i have to create views cache ?
        """
        self.log.debug('Processing View [%s]' % name)
        if not name.startswith('_'):
            design, name = name.split('/', 1)
            name = '/'.join(['_design', design, '_view', name])
        return couchdb.client.PermanentView(self.resource(*name.split('/')), name,
                             wrapper=wrapper)(**options)
        
    