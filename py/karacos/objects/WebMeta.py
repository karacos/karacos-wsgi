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

Created on 12 dec. 2009

@author: nico
'''
#from twisted.python.zippath import ZIP_PATH_SEP
#from pkg_resources import StringIO
__author__="Nicolas Karageuzian"
__contributors__ = ["Cyril Gratecos"]
import cherrypy, types
import karacos
import StringIO
import os, traceback, sys
from mako.lookup import TemplateLookup

class WebMeta(karacos.db['AuthMeta']):
    """
    Class type for web exposed objects
    """
    
    
    def __init__(self, name, parents, dict):
        """
        Appele lors de la construction d'un type
        """
        self.log = karacos.core.log.getLogger(self)
        self.log.info("WebMeta :  for %s  " % name)
        karacos.db['KcDocMeta'].__init__(self, name, parents, dict)
        karacos.webdb[name] = self
            
    def __call__(self, *args, **kw):
        
        """
        Method called at instance creation.
        
        """
        self.log.info("BEGIN WebMeta.__call__ ")
        assert 'data' in kw
        assert 'type' in kw['data']
        if kw['data']['type'] == 'WebNode':
            assert 'WebType' in kw['data']
        instance = karacos.db['AuthMeta'].__call__(self, *args, **kw)
        return instance
        
karacos.db['WebMeta'] = WebMeta