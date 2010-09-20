
import socket
import ssl
import httplib
import urllib
import karacos
from karacos.core.net import HttpProxyConnection

HTTPConnection = httplib.HTTPConnection

class HTTPSConnection(httplib.HTTPSConnection):
    # httplib.HTTPSConnection with proxy support
    def __init__(self, host, port = None, key_file = None, cert_file = None,
                 strict = None, http_proxy = None):
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file,
                                         strict)
        self.http_proxy = http_proxy

    def connect(self):
        if self.http_proxy:
            conn = HttpProxyConnection((self.host, self.port), self.http_proxy)
            conn.establish()
            sock = conn.socket
            #self.sock = httplib.FakeSocket(sock, ssl)
            #ssl = socket.ssl(sock, self.key_file, self.cert_file)
            self.sock = ssl.wrap_socket(sock)
            
        else:
            httplib.HTTPSConnection.connect(self)

class UrlHandler(object):
    http_timeout = 15
    proxy_host = None
    proxy_port = None
    
    def __init__(self,http_timeout=None,proxy_host=None,proxy_port=None):
        try:
            self.http_timeout = float(http_timeout)
        except:
            pass
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        
    
    def processRequest(self,method=None,url=None,data="",headers={}):
        socket.setdefaulttimeout(self.http_timeout)
        (protocol,resource) = urllib.splittype(url)
        (hostport,path) = urllib.splithost(resource)
        connexion = None
        if protocol.lower() == "http":
            (host,port) = urllib.splitnport(hostport, 80)
            import httplib
            if self.proxy_host != None and self.proxy_port != None :
                connexion = HTTPConnection(self.proxy_host, self.proxy_port, timeout=self.http_timeout)
                path = url
            else:
                connexion = HTTPConnection(host, port, timeout=self.http_timeout)
        elif protocol.lower() == "https" :
            (host,port) = urllib.splitnport(hostport, 443)
            connexion = HTTPSConnection(host, port)
            if self.proxy_host != None and self.proxy_port != None :
                connexion.http_proxy = [self.proxy_host,
                                        self.proxy_port]
        else:
            assert False, "Unhandled Protocol, please use HTTP or HTTPS"
        
            
        connexion.connect()
        connexion.request(method, path, body=data, headers=headers)
        response = connexion.getresponse()
        
        return response
