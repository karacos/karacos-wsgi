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

Created on 24 jun. 2010

@author: nico
'''
import karacos

class AuthManager(karacos.db['WebNode']):
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['WebNode'].__init__(self,parent=parent,base=base,data=data)
    
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        #assert isinstance(parent.__domain__,KaraCos.Db.SysDomain)
        if 'WebType' not in data:
            data['WebType'] = 'AuthManager'
        return karacos.db['WebNode'].create(parent=parent,base=base,data=data)
    
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __list_users__(self):
        """
        // %s
        function(doc) {
         if (doc.type == "User")
          emit(doc._id, doc);
        }
        """
    
    def _list_users(self):
        """
        """
        result = []
        users = self.__list_users__()
        for user in users:
            result.append(user.value)
        return result
        
    @karacos._db.isaction
    def list_users(self):
        """
        """
        result = {'status':'success', 'message':_("User list OK"),'data':self._list_users(),'datatype':'UsersList', 'success':True}
        return result
    
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __list_groups__(self):
        """
        // %s
        function(doc) {
         if (doc.type == "Group")
          emit(doc._id, doc);
        }
        """
    
    def _list_groups(self):
        """
        """
        result = []
        groups = self.__list_groups__()
        for group in groups:
            result.append(group.value)
        return result
        
    @karacos._db.isaction
    def list_groups(self):
        """
        """
        result = {'status':'success', 'message':_("Group list OK"),'data':self._list_groups(),'datatype':'GroupsList', 'success':True}
        return result
        
    @karacos._db.isaction
    def modify_user(self,*args,**kw):
        """
        fast hack, should be securised
        """
        assert 'name' in kw
        user = self.__domain__.get_user_by_name(kw['name'])
        del kw['name']
        if 'password' in kw:
            if kw['password'] != "":
                if 'password_confirm' in kw:
                    if kw['password'] == kw['password_confirm']:
                        user['password'] =  "%s" % karacos.db['User'].hash_pwd(kw['password'])
            del kw['password']
        if 'password_confirm' in kw:
            del kw['password_confirm']
        for key in kw.keys():
            user[key] = kw[key]
        
        user.save()
        
    @karacos._db.isaction
    def add_user_to_group(self,username=None,groupname=None):
        group = self.__domain__.get_group_by_name(groupname)
        user = self.__domain__.get_user_by_name(username)
        group.add_user(user)
    add_user_to_group.form = {'title': _("Ajouter utilisateur a un groupe"),
         'submit': _('Ajouter'),
         'fields': [{'name':'username', 'title':"Nom de l'utilisateur",'dataType': 'TEXT'},
                    {'name':'groupname', 'title':'Nom du groupe','dataType': 'TEXT'},]}
    
    @karacos._db.isaction
    def create_user(self,username=None,password=None):
        """
        Create user in containing domain
        """
        assert isinstance(username,basestring)
        assert isinstance(password,basestring)
        self.__domain__._create_user(username=username,password=password)
    create_user.form = {'title': _("Creer un groupe"),
         'submit': _('Creer'),
         'fields': [{'name':'username', 'title':'Nom du user','dataType': 'TEXT'},
                    {'name':'password', 'title':'Mot de passe','dataType': 'PASSWORD'}]}
    @karacos._db.isaction
    def create_group(self,groupname=None):
        """
        Create group in containing domain
        """
        assert isinstance(groupname,basestring)
        self.__domain__._create_group(groupname, False)
    create_group.form = {'title': _("Creer un groupe"),
         'submit': _('Creer'),
         'fields': [{'name':'groupname', 'title':'Nom du groupe','dataType': 'TEXT'},]}