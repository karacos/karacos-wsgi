"""
    KaraCos - web platform engine - http://karacos.org/
    Copyright (C) 2009-2010  Nicolas Karageuzian - Cyril Gratecis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__license__ = 'AGPL'
import cherrypy
import smtplib
import karacos
import random
import string
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def valid_email(email):
    import re
    reg = re.compile('([\w\.\-]+@[\w][\w\.\-]+)')
    return reg.match(email)

def send_mail(destmail, msg):
    """
    """
    try:
        server = smtplib.SMTP(karacos.config['mail']['smtp_server'],karacos.config['mail']['smtp_server_port'])
        server.ehlo()
        server.sendmail(karacos.config['mail']['from_addr'], destmail, msg)
        print "mail sent"
    except Exception,e:
        import sys
        print sys.exc_info()
        raise e
        