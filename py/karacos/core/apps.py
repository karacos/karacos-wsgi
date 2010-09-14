'''
Created on 14 sept. 2010

@author: nico
'''
import os, sys
import karacos
import ConfigParser
_appsdirs = [os.path.join(karacos.homedir,'apps'), os.path.join(karacos._srvdir,'deploy')]
def listApps():
    _apps = {}
    for _appsdir in _appsdirs:
        for dir in os.listdir(_appsdir):
            if os.path.exists(os.path.join(_appsdir,dir,'__init__.py')):
                _apps[dir] = _appsdir
    return _apps

class InitApps(dict):
    def __init__(self):
        #import Apps in KaraCos.Apps Namespace and configure it 
        self.log = karacos.core.log.getLogger(self)
        self.log.debug('--> Starting Application Initializer')
        self.apps = listApps()
        self.log.debug("listApps: %s" % self.apps)
        for _app in self.apps.keys():
            self.init_app(self.apps[_app],_app)
        self.log.debug('--> Ended Application Initializer')
        
    def init_app(self,app_dir,app_name):
        """
        Initialise application
        """
        try:
            if app_name in self:
                self.log.info('[%s]: --> Application already initialized' % app_name)
                return
            self.log.info('[%s]: --> Initializing Application' % app_name)
            #if (KaraCos.Apps.get(app_name) == None:
            #    return
            appconf = os.path.join(app_dir,app_name,'conf','App.conf')
            conf = ConfigParser.RawConfigParser()
            conf.read(appconf)
            if 'system' in conf.sections():
                try:
                    require = conf.get('system','require')
                    require = require.split(",")
                    self.log.info('[%s]: --> Requiring %s' % (app_name,require))
                    for required_app in require:
                        required_app = required_app.strip()
                        try:
                            self.log.info('[%s]: --> Loading required app [%s]' % (app_name,required_app))
                            self.init_app(self.apps[required_app],required_app)
                        except:
                            self.log.log_exc(sys.exc_info(),'error')
                except:
                    pass
            self.set_system_path(app_dir,app_name)
            self[app_name] = __import__(app_name, globals(), locals(), [], -1)
            app = self[app_name]
            app.name = app_name
            app.dir = app_dir
            self.log.info("[%s]: --> Application loaded successfully" % app.name)
        except Exception, e:
            self.log.warn('[%s]: --> loading failed' % app_name)
            self.log.log_exc(sys.exc_info(),'error')
    
    def set_system_path(self,appdir,appname):
        """
        Setting system path
        """
        self.log.debug('Starting set_system_path')
        sys.path.append(appdir)
        self.log.debug('Setting %s in system.path' % appdir)
        libdir = os.path.join(appdir,appname,'lib','Python')
        if os.path.exists(libdir):
            self.log.debug('Setting %s in system.path' % libdir)
            sys.path.append(libdir)