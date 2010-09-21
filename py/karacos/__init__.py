
import os
import gettext
import ConfigParser
homedir_pydir = __path__[0][0:__path__[0].rfind('karacos')]
print "karacos.homedir_pydir = %s" % homedir_pydir
homedir = homedir_pydir[0:homedir_pydir.rfind('py')]
print "%s" % __path__
print "karacos.homedir = %s" % homedir

class container(dict):
    """
    """
kc_props = container()
kc_props.homedir = homedir
## BINDING translation method in __builtins__

__builtins__['_'] = gettext.gettext
__builtins__['kc_props'] = kc_props

import simplejson as json

# TODO: handles server definition
if 'KC_SERVER_NAME' not in os.environ:
    os.environ['KC_SERVER_NAME'] = 'default'
if os.environ['KC_SERVER_NAME'] == None or os.environ['KC_SERVER_NAME'] =='':
    os.environ['KC_SERVER_NAME'] = 'default'
    
_srvdir = os.path.join(homedir,'server',os.environ['KC_SERVER_NAME'])
if not os.path.exists(_srvdir):
    print "%s isn't a server directory, aborting start" % os.environ['KC_SERVER_NAME']
    import sys
    sys.exit()
    
_confdir = os.path.join(_srvdir,'conf')
print "Reading config from %s" % os.path.join(_confdir,'karacos.conf')
config = ConfigParser.RawConfigParser()
config.read(os.path.join(_confdir,'karacos.conf'))

import core

from logging import getLogger
log = getLogger(__name__)

if config.has_section('system'):
    if config.has_option('system', 'mode'):
        if config.get('system','mode') == 'dev':
            log.info('System mode is DEV')

db = container()
db.server_url = "http://localhost:5984"
db.sysdb_name = "karacos2_sysdb"
if config.has_section('db'):
    if config.has_option('db', 'server'):
        db.server_url = config.get('db', 'server')
        log.info("DB Server found in conf : '%s'" % db.server_url)
    if config.has_option('db', 'sysdb_name'):
        db.sysdb_name = config.get('db', 'sysdb_name')
        log.info("DB name found in conf : '%s'" % db.sysdb_name)
db.server = None
db.sysdb = None
webdb = container()
webdb.actions = container()
import _db

import http
import objects

base = db['Base'].get_by_name(db.sysdb_name)
if base == None:
    db.sysbase = db['Base'].create(db.sysdb_name)
else:
    db.sysbase = base

import wsgi

apps = core.apps.InitApps()

serving = http._Serving()

