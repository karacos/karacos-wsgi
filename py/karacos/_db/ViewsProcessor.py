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


Created on 4 dec. 2009

@author: nico
'''
from logging import getLogger
log = getLogger(__name__)
import sys
import karacos

class ViewsProcessorMeta(type):
    """
    """
    _processors = dict()
    
    def __init__(self, name, parents, dict):
        type.__init__(self, name, parents, dict)
        self.log = karacos.core.log.getLogger(self)
    
    def __call__(self, base_name):
        """
        A l'appel du constructeur
        """
        assert base_name in karacos.db.server, "View for inexistant DB"
        if base_name not in ViewsProcessorMeta._processors:
            self.log.debug("create ViewProcessor : %s" % base_name)
            ViewsProcessorMeta._processors[base_name] = type.__call__(self, karacos.db.server[base_name])
        else:
            self.log.debug("returning existing ViewProcessor : %s" % base_name)
        return ViewsProcessorMeta._processors[base_name]


class ViewsProcessor(object):
    """
    Handles permanent views for a database
    """
    _views = dict()
    __metaclass__ = ViewsProcessorMeta
    db = None
    def __init__(self,db):
        """
        Constructor
        """
        self.db = db
        self.log = karacos.core.log.getLogger(self)
    
    def process_view(self,index, viewname,language,value, **kw):
        """
        """
        id = "_design/%s" % index
        self.log.debug("BEGIN process_view : %s" % id)
        self.create_view(id, viewname,language,value)
        view_index = '%s/_view/%s'%(id,viewname)
        self.log.debug("process_view : %s" % view_index)
        return self.db.view(view_index, **kw)
        
        
    
    def create_view(self,id, viewname,language,value):
        """
        """
        self.log.debug("create_view : %s - %s" % (id,viewname))
        id = str(id)
        if id not in self.db:
            self.log.debug("create_view : Creating %s viewset with single view %s with language=%s and value=%s" % (id,viewname,language,value))
            viewset = { 'language': str(language),
                        'views': { str(viewname) : { "map" : str(value) }}
                           }
            self.db[id] = viewset
        
        self.db.reset_cache(id)
            
        self._views[id] = self.db[id]
        
        if viewname not in self._views[id]['views']:
            self._views[id]['views'][viewname] = { "map" : value }
            self.db[id] = self._views[id]
                
                 
def isview(base_def,language):
    """
    Decorator pour les methodes qui renvoient des vues
    gere les vues permanentes
    """
    assert isinstance(base_def, basestring) , "Base Id shoud be string"
    assert base_def == 'self' or base_def == 'parent', ""
    def decor(func):
        log.debug("@isview : func = %s , doc = %s" % (func,dir(func)))
        
        def wrapper(*args,**kw):
            log.debug("BEGIN @isview.wrapper for func : %s with args %s" % (func,kw) )
            
            if len(args) > 1:
                ""
            self = args[0]
            base_name = None
            if base_def == 'self':
                base_name = self.base['name']
            if base_def == 'parent':
                base_name = self.parent.base['name']
            processor = ViewsProcessor(base_name)
            index = "%s.%s.%s" % (self.__module__
                            ,self.__class__.__name__,func.func_name) 
            viewname = self['_id']
            arglist = list()
            arglist.append(self['_id'])
            for arg in args[1:]:
                log.debug("@isview.wrapperfunc arg : %s" % arg)
                viewname = "%s.%s" % (viewname,arg)
                arglist.append(arg)
            argtuple = tuple(arglist)
    #        KaraCos._Db.views[func.viewindex]['views']
            #a = func(*args,**kw)
            log.debug("@isview.wrapperfunc args : %s" % repr(argtuple))
            value = func.__doc__ % argtuple
            result = processor.process_view(index, viewname,language,value,**kw)
            log.debug("END @isview.wrapper [RESULT]%s[/RESULT]" % result)
            return result
            
            #return func(*args,**kw)
        wrapper.isview = True
        return wrapper
    return decor

sysdb_processor = ViewsProcessor(karacos.db.sysdb_name)
def is_static_view(language):
    """
    decorator for a 'staticmethod style' view
    static view is *always* running on sysdb
    """
    def decor(func):
        log.debug("@is_static_view : func = %s , doc = %s" % (func,dir(func)))
        index = "%s.%s.%s" % (func.__module__
                        ,func.__class__.__name__,func.func_name)
        def wrapper(*args,**kw):
            log.debug("BEGIN @is_static_view for func : %s with args %s" % (func,args) )
            arglist =   argtuple = list()
            viewname = ""
            if len(args)>0:
                if isinstance(args[0],basestring):
                    viewname = args[0]
                    arglist.append(args[0])
            if len(arglist) > 1:
                for arg in args[1:]:
                    assert isinstance(arg,basestring),"views only accepts string args"
                    viewname = "%s.%s" % (viewname,arg)
                    arglist.append(arg)
            
                argtuple = tuple(arglist)
            else:
                if len(args)>0:
                    argtuple = args[0]
            value = func.__doc__
            if len(argtuple) > 0:
                value = func.__doc__ % argtuple
            result = sysdb_processor.process_view(index, viewname,language,value)
            #
            return result
            #KaraCos._Db.log.debug("END @isstaticview.wrapper [RESULT]%s[/RESULT]" % result)
            #return result
        return wrapper
    return decor
