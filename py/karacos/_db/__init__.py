from logging import getLogger
log = getLogger(__name__)
import karacos

class Exception(karacos.core.Exception):
    """
    Base exception class for Db
    """
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

import wrapper

if 'db' in karacos.config.sections():
    if 'server_url' in karacos.config.items('db'):
        karacos.db.server_url = karacos.config.get('db', 'server_url')
    if 'sysdb_name' in karacos.config.items('db'):
        karacos.db.sysdb_name = karacos.config.get('db', 'sysdb_name')
karacos.db.server = wrapper.Server(karacos.db.server_url)
if karacos.db.sysdb_name not in karacos.db.server:
    log.info("sysdb not created, creating")
    karacos.db.server.create(karacos.db.sysdb_name)
karacos.db.sysdb = karacos.db.server[karacos.db.sysdb_name]


import ViewsProcessor

def isaction(func):
        """
        Decorator pour les methodes d'instances qui seront publiees pour cet objet (actions).
        """
        log.info("@isaction : func = %s" % func.__name__)
        
        def wrapper(*args, **kwds):
            def get_action(wrapped_function,instance):
                func_in_instance = eval("instance.%s" % func.__name__)
                result = {'action':func.__name__}
                if 'label' in dir(wrapped_function):
                    result['label'] = wrapped_function.label
                if 'get_form' in dir(func_in_instance):
                    result['form'] = func_in_instance.get_form(instance)
                elif 'form' in dir(wrapped_function):
                    result['form'] = wrapped_function.form
                else:
                    result['form'] = {}
                
                result['doc'] = wrapped_function.__doc__
                result['acturl'] = instance._get_action_url()
                #if KaraCos.conf['system']['mode'] == 'dev':
                #    result['acturl'] = './_self/'
                return result
            
            if args[0] == "get_action":
                return get_action(args[1],args[2])
                
            instance = args[0]
            log.info("Wrapper : %s , %s , %s , %s" % (func.__name__,instance['name'],args,kwds))
            
            
        #    func.isaction = True
            #KaraCos._Db.actions[kctype].append(func.__name__)
            returnData = False
            if karacos.serving.get_session() != None:
                if func.__name__ in instance.get_user_actions(instance.__domain__.get_user_auth()):
                    returnData = True
            if returnData:
                return func(*args, **kwds)
            else:
                raise karacos.http.HTTPError(status=403,message=_("Ressource non autorisee"))
                return  {}#'status':'failure', 'message':_('Unauthorised Method'),
#                    'errors':{}} 
        
        wrapper.func = func
        if 'label' in dir(func):
            wrapper.label = func.label
        if 'get_form' in dir(func):
            wrapper.get_dyn_form = func.get_form
        elif 'form' in dir(func):
            wrapper.form = func.form
        wrapper.__doc__ = _(func.__doc__)
        def get_action(currentparent):
            return wrapper('get_action',wrapper,currentparent)
        
        wrapper.get_action = get_action
        wrapper.isaction = True
        
        
        
        return wrapper