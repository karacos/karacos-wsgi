
import os
import gettext
import ConfigParser
homedir = __path__[0][0:__path__[0].rfind('/py/karacos')]
print "karacos.homedir = %s" % homedir

class container(dict):
    """
    """

## BINDING translation method in __builtins__

__builtins__['_'] = gettext.gettext

import simplejson as json

# TODO: handles server definition
_confdir = os.path.join(homedir,'server','default','conf')
print "Reading config from %s" % os.path.join(_confdir,'karacos.conf')
config = ConfigParser.RawConfigParser()
config.read(os.path.join(_confdir,'karacos.conf'))

import core

from logging import getLogger
log = getLogger(__name__)


db = container()
db.server_url = "http://localhost:5984"
db.sysdb_name = "karacos2_sysdb"
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

serving = http._Serving()

