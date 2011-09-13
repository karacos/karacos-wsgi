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
from uuid import uuid4
import karacos
import sys

class DomainsManager(karacos.db['WebNode']):
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['WebNode'].__init__(self,parent=parent,base=base,data=data)
        
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        #assert isinstance(parent.__domain__,KaraCos.Db.SysDomain)
        if 'WebType' not in data:
            data['WebType'] = 'DomainsManager'
        return karacos.db['WebNode'].create(parent=parent,base=base,data=data)
    
    @staticmethod
    @karacos._db.ViewsProcessor.is_static_view('javascript')
    def _get_domains(string=""):
        ''' //%s
            function(doc) {
            if (doc.type == "Domain" && !("_deleted" in doc && doc._deleted == True))
              emit(doc._id, doc);
        }
        '''
    
    def _edit_domain(self,*args,**kw):
        assert 'name' in kw, "Mandatory parameter name is required"
        domain = karacos.db['Domain'].get_by_name(name)
        domain._update_item()
        if 'fqdn' in kw:
            domain['fqdn'] = kw['fqdn']
        if 'site_theme_base' in kw:
            domain['site_theme_base'] = kw['site_theme_base']
        if 'site_template_uri' in kw:
            domain['site_template_uri'] = kw['site_template_uri']
        if 'WebType' in kw:
            domain['WebType'] = kw['WebType']
        domain.save()
        return {'success': True, 'message': "Domain data updated"}
        
        
    @karacos._db.isaction
    def edit_domain(self,*args,**kw):
        return self._edit_domain(*args,**kw)

    def _create_domain(self,name=None, fqdn=None,type='Domain'):
        """
        """
        assert type in karacos.db
        assert issubclass(karacos.db[type],karacos.db['Domain'])
        if karacos.db['Domain'].exist_with_fqdn(fqdn) or karacos.db['Domain'].exist_with_name(name):
            self.log.info("Domain exist with given fqdn or name, creation aborted")
            return
        _db_name = 'kc2_%s_%s' % (name, uuid4().hex)
        base = karacos.db['Base'].create(_db_name)
        domainvalue  = {}
        domainvalue['name'] = name
        domainvalue['fqdn'] = fqdn
        domainvalue['site_theme_base'] = '/default'
        domainvalue['stylesheets'] = ["domain"]
        self.log.info("MANAGER starting domain creation")
        try:
            domain = karacos.db[type].create(base=base,data=domainvalue)
            self.log.info("MANAGER domain creation OK")
            return {'success': True}
        except:
            self.log.log_exc(sys.exc_info())
            self.log.error("MANAGER domain creation exception")
    
    @karacos._db.isaction
    def create_domain(self,name=None, fqdn=None,type=None):
        """
        """

        return self._create_domain(name, fqdn,type)
        
    create_domain.form = {'title': _("Creer un domaine"),
         'submit': _('Creer'),
         'fields': [{'name':'name', 'title':_('Nom du domaine'),'dataType': 'TEXT'},
                    {'name':'fqdn', 'title':_('FQDN'),'dataType': 'TEXT'},
                    {'name':'type', 'title':_('Type'),'dataType': 'TEXT', 'value': 'Domain'}]}
    create_domain.label = _("Creer un domaine")
    def _domain_list(self):
        """
        """
        list = DomainsManager._get_domains("_domain_list")
        result = {}
        for domain in list:
            result[domain.value['name']] = karacos.db.sysdb[domain.key]
        return result
    
    @karacos._db.isaction
    def domain_list(self):
        """
        Returns a list of domains on current system
        """
        return {'status': 'success',
                'data': self._domain_list(),
                'datatype': 'DomainsList'}