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


Created on 7 janv. 2010

@author: nico
'''

import karacos
import logging
log = logging.getLogger(__name__)

class AuthMeta(karacos.db['ChildMeta']):
    """
    Meta Class for all auth types
    """
    def __call__(self, *args, **kw):
        """
        A l'appel du constructeur
        """
        log.info("BEGIN AuthMeta.__call__ ")
        instance = karacos.db['ChildMeta'].__call__(self, *args, **kw)
        log.info("END AuthMeta.__call__ ")
        return instance
    
    
karacos.db['AuthMeta'] = AuthMeta