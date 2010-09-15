'''
Created on 22 aout 2010
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
@author: nico
'''

import karacos

class WorkFlowItem(karacos.db['Node']):
    """
    Workflow item refs an item in domain, and carry for it a validation method, an authref for valider,
    and a basic state active/inactive.
    This is 
    """
    def __init__(self,parent=None,base=None,data=None):
        assert self.__class__.__name__ != 'WorkFlowItem', "Type WorkFlowItem is abstract, it must be subclassed"
        karacos.db['Node'].__init__(self,parent=parent,base=base,data=data)
    
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert 'type' in data, "Abstract WokrFlowItem must be implemented in subclass" 
        assert isinstance(data,dict)
        assert isinstance(parent,karacos.db['Manager'])
        assert 'ref_db' in data, "Workflow Item must ref item related container db"
        assert 'ref_id' in data, "Workflow Item must ref item related id"
        assert not parent.workflow_exist_for_node(data['ref_db'],data['ref_id']), "Workflow item for node already exist"
        assert 'ref_auth' in data, "Workflow next step validator has to be given"
        if 'active' not in data:
            data['active'] = True
        data['iswkf'] = True
        return karacos.db['Node'].create(parent=parent,base=base,data=data)
    
    def _is_valid_for_user(self):
        authref = self._get_validation_authref()
        user = self.__domain__.get_user_auth()
        isvalidator = False
        if 'user.%s' % user['name'] in authref:
            isvalidator = True
        for group in user.get_groups():
            if group in authref:
                isvalidator = True
        return isvalidator
    
    def _is_active(self):
        """
        Returns true if item has to be validated
        """
        return self['active']
        
    def _get_validation_authref(self):
        """
        Returns auth id for validating item
        """
        return self['ref_auth']
    
    def _get_validation_method(self):
        """
        Returns validation method (python) to perform
        """
        assert False, "Method _get_validation_method must be overided in subclass"
        
    def _get_validation_action(self):
        """
        Returns validation action Form definition (json)
        """
        assert False, "Method _get_validation_action must be overided in subclass"

    def _get_title(self):
        """
        Returns a title for item
        """
        assert False, "Method _get_title must be overided in subclass"

    def _get_description(self):
        """
        Returns a description for item
        """
        assert False, "Method _get_description must be overided in subclass"