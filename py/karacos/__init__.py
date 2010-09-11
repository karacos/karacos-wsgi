
import os
homedir = __path__[0][0:__path__[0].rfind('/py/karacos')]
print "karacos.homedir = %s" % homedir

import core
import http
import wsgi