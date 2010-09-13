# -*- coding: utf-8 -*-
from urllib import urlencode
from urlparse import parse_qsl

import httplib2
import oauth2
from webob import Request, Response
from webob.exc import HTTPFound, HTTPNotFound, HTTPUnauthorized
try:
    from wsgiref.simple_server import make_server
except ImportError:
    raise ImportError("""
wsgiref is required to run this example, but not required by the wsgioauth
package.  You must install wsgiref before you can run this file.  One way to
install it is through easy_install by using the following command in your
console:  easy_install wsgiref
""")

from wsgioauth.consumer import Client

# The following are the actual example use-case URLs. For the purposes of
#   this example, we have reassigned the domains to the associated
#   application.
# CALLBACK_URL = "http://printer.example.com/request_token_ready"
# REQUEST_TOKEN_URL = "https://photos.example.net/request_token"
# AUTHORIZATION_URL = "http://photos.example.net/authorize"
# ACCESS_TOKEN_URL = # "https://photos.example.net/access_token"
# PROTECTED_RESOURCE_URL = "http://photos.example.net/photo"

CALLBACK_URL = "http://localhost:61080/request_token_ready"
# localhost:8080 is available by running protected_resource.py
REQUEST_TOKEN_URL = "http://localhost:61080/request_token"
AUTHORIZATION_URL = "http://localhost:61080/authorize"
ACCESS_TOKEN_URL = "http://localhost:61080/access_token"
PROTECTED_RESOURCE_URL = "http://localhost:61080/photo"
RESOURCE_PARAMETERS = {'file': 'vacation.jpg', 'size': 'original'}

consumer = ('dpf43f3p2l4k3l03', # key
            'kd94hf93k423kf44', # secret
            )

template = """<html><body>%s</body></html>"""

class ConsumerApp(object):
    """Example that does a single user consumption of the protected resource.
    This example application will not handle two or more OAuth processes
    at a time."""

    consumer = oauth2.Consumer(*consumer)
    request_token = None
    access_token = None

    def fetch_request_token(self):
        """Fetch a request token from the service provider.  The request
        token is used to obtain authorization."""
        # Get a client and give it a callback.  If the call back isn't
        #   given it will be set to 'oob', which means out-of-band. But if
        #   the callback hasn't really been registered out-of-band, then an
        #   error will be raised.
        client = self.get_client(callback_url=CALLBACK_URL)

        resp, content = client.request(REQUEST_TOKEN_URL)
        # Capture the request token
        self.request_token = oauth2.Token.from_string(content)

    def fetch_access_token(self, verifier):
        # Assign the verifier to the request token so that the client can use
        #   it without explicitly being told to do so.
        self.request_token.verifier = verifier

        # Get a client that will use the consumer and request token to obtain
        #   the access token. 
        client = self.get_client()

        resp, content = client.request(ACCESS_TOKEN_URL)
        # Capture the access token
        self.access_token = oauth2.Token.from_string(content)
        # Null out the request token, because it is now useless anyways.
        self.request_token = None

    def get_client(self, **kwargs):
        """Create a client from the most recent information."""
        token = None

        # Determines which token we should use, if any.
        if self.access_token is not None:
            token = self.access_token
        elif self.request_token is not None:
            token = self.request_token

        return Client(self.consumer, token, **kwargs)

    def index_page(self, request):
        """The front-page or index page... click the link on this page to
        initialize the OAuth process.  Return to the page to see the saved
        access token."""
        # Create a link to the OAuth *thing*. In this case the resouce is
        #   similar to RPC, but could just as well be an actual file.
        body = """<a href="/print_vacation">Print my vacation image</a>"""
        body += "<br />"

        # Display any information we might have about the consumer and access
        #   token.  This is very unsecure of course, but handy for display
        #   purposes.
        body += ("<div><b>consumer</b>: <i>key</i> = %s, <i>secret</i> = "
            "%s</div>" % (self.consumer.key, self.consumer.secret))
        if self.access_token is not None:
            body += ("<div><b>access token</b>: <i>key</i> = %s, "
                "<i>secret</i> = %s</div>" % (self.access_token.key,
                self.access_token.secret))

        body = template % body
        return Response(body)

    def print_vacation(self, request):
        """Uses OAuth to do... well nothing sophisticated, but hopefully
        you will get the point.  If the access token doesn't exist, we
        initialize the process for obtaining it."""
        if self.access_token is None:
            # The access token is required to gain access to the protected
            #   resource.
            if self.request_token is None:
                self.fetch_request_token()
                # Redirect the user to the service provider's authorization
                #   URL with the token key as payload; so that the service
                #   provider can associate the user with a particular request
                #   token.
                location = '?'.join([AUTHORIZATION_URL, "oauth_token=%s" %
                    self.request_token.key])
                response = HTTPFound(location=location)
            else:
                # okay... why are you here? O.o
                response = HTTPFound("%s/" % request.host_url)
        else:
            # Because we have an access token, we can now make a request to
            #   the protected resource. 
            client = self.get_client()

            resp, content = client.request(PROTECTED_RESOURCE_URL, "POST",
                urlencode(RESOURCE_PARAMETERS))

            # Create the response body for this page based on the protected
            #   resource data.
            body = ""
            resp_data = dict(parse_qsl(content))
            # Display the protected resource's response data on the page.
            body += '<br />'.join([ "<div><b>%s</b></div>%s</div>" %
                (k, v) for k, v in resp_data.iteritems() ])

            # Create a link back to the index page.
            body += """<br /><a href="/">Back to the index page.</a>"""

            body = template % body
            response = Response(body)

        return response

    def __call__(self, environ, start_response):
        # Create a WebOb like request object.
        request = Request(environ)

        # Route the path to the associated method.
        if request.path_info == '/':
            response = self.index_page(request)
        elif request.path_info == '/print_vacation':
            response = self.print_vacation(request)
        elif request.path_info == '/request_token_ready':
            # The request_token is ready. This simply means that we have all
            #   the information we need to use the request token to retrieve
            #   the access token.
            self.fetch_access_token(request.params['oauth_verifier'])
            response = HTTPFound(location='%s/print_vacation' %
                request.host_url)
        else:
            response = HTTPNotFound()
        return response(environ, start_response)


if __name__ == '__main__':
    app = ConsumerApp()
    server = make_server('localhost', 61081, app)
    print "Serving the oauth consumer application at http://localhost:61081/"
    server.serve_forever()
