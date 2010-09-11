# -*- coding: utf-8 -*-
import os, random, string
import urllib
from collections import deque
from cStringIO import StringIO

from oauth2 import Error

__all__ = ['generate_string', 'random_word', 'xmlrpc_router',
    'get_normalized_parameters', 'repackage_request', 'NOnceList']

def generate_string(n=32):
    """Generate random hash *like* strings"""
    return ''.join([ random.choice(string.hexdigits) for x in xrange(n) ])

def random_word():
    """flipped out of:
    http://mail.python.org/pipermail/tutor/2001-June/006301.html
    WARNING to Windows users... bah, not worth the time :P
    """
    stat = os.stat('/usr/share/dict/words')
    # the filesize if the 7th element of the array
    flen = stat[6]
    f = open('/usr/share/dict/words')
    word = None
    while word is None:
        # seek to a random offset in the file
        f.seek(int(random.random() * flen))
        # do a single read with sufficient characters
        chars = f.read(50)
        # split it on white space
        wrds = string.split(chars)
        # the first element may be only a partial word so use the second
        # you can also make other tests on the word here
        if len(wrds[1]) > 5 and len(wrds[1]) < 9:
           word = wrds[1]
    return word

CALLS = {}

def xmlrpc_router(call_name):
    if call_name in CALLS.keys():
        return CALLS[call_name]
    return None

def get_normalized_parameters(request):
    """Return a string that contains the parameters that must be signed."""
    items = [ (k, v) for k, v in request.params.iteritems() if k != 'oauth_signature' ]
    encoded_str = urllib.urlencode(sorted(items))
    # Encode signature parameters per Oauth Core 1.0 protocol
    # spec draft 7, section 3.6
    # (http://tools.ietf.org/html/draft-hammer-oauth-07#section-3.6)
    # Spaces must be encoded with "%20" instead of "+"
    return encoded_str.replace('+', '%20')

def repackage_request(request):
    """Repackages the request into a request without oauth parameters."""
    new_request = request.copy()
    # first we need to deterime where the oauth stuff is in the request;
    #   then remove it without corrupting other request data

    # check for oauth in the Header
    if 'authorization' in request.headers:
        # check that the authorization header is oauth
        if request.headers['authorization'][:6] == 'OAuth ':
            del new_request.headers['authorization']

    # doesn't hurt to check in both places
    params = [(k,v) for k,v in request.params.iteritems() if not k.startswith('oauth_')]
    if request.method == 'GET': # modify the query string
        new_request.environ['QUERY_STRING'] = urllib.urlencode(params)
    elif request.method == 'POST': # modify the wsgi.input
        new_request.environ['wsgi.input'] = StringIO(urllib.urlencode(params))

    return new_request


class NOnceList(deque):
    """A ring buffer of nonce values"""

    def __init__(self, max_size=20000):
        deque.__init__(self)
        self.max_size = max_size

    def __setitem__(self, k, value):
        length = len(self)
        if length >= self.max_size or k > self.max_size:
            self.popleft()
            self.append(value)
        else:
            deque.__setitem__(self, k, value)

    def append(self, v):
        deque.append(self, v)
        if len(self) > self.max_size:
            self.popleft()
