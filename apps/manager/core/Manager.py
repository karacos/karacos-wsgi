'''
Created on 20 aout 2010

@author: nico
'''
from uuid import uuid4

import karacos

class Manager(karacos.db['Node']):
    """
    Class for managing Domains
    is a placeholder for workflow data and managment nodes
    """
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['Node'].__init__(self,parent=parent,base=base,data=data)
    
    @staticmethod
    def _get_manager():
        """
        Gets Domain unique manager
        """
    
    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        assert isinstance(data,dict)
        assert isinstance(parent, KaraCos.Db.Domain)
        data['name'] = "manager"
        if 'WebType' not in data:
            data['WebType'] = 'Manager'
        return karacos.db['Node'].create(parent=parent,base=base,data=data,owner=owner)
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_workflow_item_for_node__(self,ref_db,ref_id):
        """ // %s
        function(doc) {
         if (doc.iswkf == true && doc.ref_db == "%s" && doc.ref_id == "%s")
          emit(doc._id, doc.name);
        }
        """
        
    def get_workflow_item_for_node(self,ref_db,ref_id):
        """
        Returns existing workflow item for node
        """
        result = False
        wfnoditems = self.__get_workflow_item_for_node__(ref_db,ref_id)
        if len(wfnoditems) == 1:
            for item in wfnoditems:
                result = self.db[item.key]
        return result
                                                        
    def workflow_exist_for_node(self,ref_db,ref_id):
        """
        Returns True if a workflow item exist for ref node
        """
        result = False
        if len(self.__get_workflow_item_for_node__(ref_db,ref_id)) == 1 :
            result = True
        return result
    
    def _create_workflow_item(self, data):
        assert 'type' in data
        assert data['type'] != 'WorkFlowItem'
        assert data['type'] in KaraCos.Db.__dict__
        assert issubclass(karacos.db[data['type']],karacos.db['WorkFlowItem'])
        if 'ref_auth' not in data:
            data['ref_auth'] = ['group.staff@%s' % self.__domain__['name']]
        data['name'] = "%s" % uuid4().hex
        result = self._create_child_node(data=data, type=data['type'], base=False)
        return result
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_active_workflow_items_list__(self):
        """ // %s
        function(doc) {
         if (doc.iswkf == true && doc.active == true && !("_deleted" in doc && doc._deleted == true))
          emit(doc._id, doc.name);
        }
        
        """
    
    @karacos._db.isaction
    def get_owner_workflow_items_list(self):
        """
        """
        items = self.__get_active_workflow_items_list__()
        result = []
        for item in items:
            itemobject = self.db[item.key]
            if itemobject._is_valid_for_user():
                result.append(itemobject)
        return {'status': 'success','message':'%s items to validate' % len(result), 'datatype':'workflowitems','data': result}
    
    def _get_action_for_item(self,item):
        """
        Returns actionform for validation of given item
        """
        result = {'acturl':self._get_action_url(),
                  'form':item._get_validation_action(),
                  'action':'process_workflow_item_validation'}
        result['form']['fields'].append({'name': 'item_id', 'dataType':'hidden', 'value':item.id})
        result['label'] = result['form']['title']
        return result
    
    @karacos._db.isaction
    def process_workflow_item_validation(self,*args,**kw):
        assert 'item_id' in kw
        item = self.db[kw['item_id']]
        assert item._is_active(), "Item is not active, no validation needed"
        
        assert item._is_valid_for_user(), "You can't process item validation"
        result = None
        item._get_validation_method()(item,*args,**kw)
        return {'status': 'success','message':'item validated', 'data':result}