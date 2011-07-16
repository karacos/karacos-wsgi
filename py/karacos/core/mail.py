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
        
        server = smtplib.SMTP(karacos.config.get('mail','smtp_server'),
                              karacos.config.get('mail','smtp_server_port'))
        server.ehlo()
        if karacos.config.has_option('mail', 'smtp_ssl'):
            if karacos.config.get('mail', 'smtp_ssl') == "True" or karacos.config.get('mail', 'smtp_ssl'):
                server.starttls()
                server.ehlo()
        if karacos.config.has_option('mail', 'smtp_password'):
            src = karacos.config.get('mail','from_addr')
            password = karacos.config.get('mail','smtp_password')
            server.login(src, password) 
        server.sendmail(karacos.config.get('mail','from_addr'), destmail, msg)
        print "mail sent"
        server.close() 
    except Exception,e:
        import sys
        print sys.exc_info()
        raise e
def send_domain_mail(domain, destmail, msg):
        server = smtplib.SMTP(domain['site_email_service_host'],
                              domain['site_email_service_port'])
        server.ehlo()
        if 'site_email_service_secure' in domain:
            if domain['site_email_service_secure'] or domain['site_email_service_secure'] == True:
                server.starttls()
                server.ehlo()
        if 'site_email_service_password' in domain:
            server.login(domain['site_email_service_username'], domain['site_email_service_password']) 
        server.sendmail(domain['site_email_from'], destmail, msg)
        server.close()