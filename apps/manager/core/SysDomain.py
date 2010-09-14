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

Created on 22 jun. 2010

@author: nico
'''
import karacos

class SysDomain(karacos.db['Domain']):
    
    def __init__(self,*args, **kw):
        karacos.db['Domain'].__init__(self,*args, **kw)
    
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'SysDomain'
        result = karacos.db['Domain'].create(base=base,data=data)
        result.log.info("create domain : %s" % result)
        return result
    
    @karacos._db.isaction
    def create_domain(self,domain_name=None,fqdn=None, type=None): 
        """
        """
        if domain_name in self.__dict__:
            raise cherrypy.HTTPRedirect("/",301)
        domain = karacos.db['Domain'].get_by_name(domain_name)
        if domain != None:
            self.__dict__[domain['name']] = domain
            raise karacos.http.HTTPRedirect("/",301)
        
        base_name = "%s_db" % domain_name
        base = karacos.db['Base'].get_by_name(base_name)
        if base != None:
            raise karacos.http.HTTPRedirect("/",301)
        
        base = karacos.db['Base'].create(base_name)
        
        domainvalue  = {}# KaraCos.Db.KaraCosObject.get_default_value()
        domainvalue['name'] = domain_name
        domainvalue['fqdn'] = fqdn #cherrypy.request.headers['Host']
        domain  = karacos.db['Domain'].create(base=base,data=domainvalue)
        self.__dict__[domain['name']] = domain
        
    create_domain.form = {'title': _("Ajouter un domaine"),
         'submit': _('Ajouter'),
         'fields': [{'name':'domain_name', 'title':_('Nom du domaine'),'dataType': 'TEXT'},
                    {'name':'fqdn', 'title':_('FQDN'),'dataType': 'TEXT'},
                 ] }