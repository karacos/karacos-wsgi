# -*- coding: utf-8 -*-
import urlparse
try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl

import httplib2
import oauth2
from oauth2 import Consumer, Token

__all__ = ['Request', 'Client']

class Request(oauth2.Request):
    """OAuth version 1.0a request class."""
    version = '1.0a'

    @classmethod
    def from_consumer_and_token(cls, consumer, token=None,
        http_method=oauth2.HTTP_METHOD, http_url=None,
        parameters=None, callback=None):
        if not parameters:
            parameters = {}

        defaults = {
            'oauth_consumer_key': consumer.key,
            'oauth_timestamp': cls.make_timestamp(),
            'oauth_nonce': cls.make_nonce(),
            'oauth_version': cls.version,
        }

        defaults.update(parameters)
        parameters = defaults

        if token:
            parameters['oauth_token'] = token.key
            if token.verifier:
                # we have, so use it then null it
                parameters['oauth_verifier'] = token.verifier
                token.verifier = None
        else: # must be a request_token
            if callback is None and callback != 'oob':
                if not hasattr(consumer, 'callback'):
                    raise RuntimeError('Callback url is undefined.')
                else:
                    callback = 'oob'
            parameters['oauth_callback'] = callback

        return Request(http_method, http_url, parameters)


class Client(httplib2.Http):
    """OAuth version 1.0a client."""

    callback_url = 'oob' # out-of-band

    def __init__(self, consumer, token=None, cache=None, timeout=None,
        proxy_info=None, callback_url=None):

        if consumer is not None and not isinstance(consumer, Consumer):
            raise ValueError("Invalid consumer.")

        if token is not None and not isinstance(token, Token):
            raise ValueError("Invalid token.")

        self.consumer = consumer
        self.token = token
        self._signature = oauth2.SignatureMethod_HMAC_SHA1()

        if callback_url is not None:
            self.callback_url = callback_url

        httplib2.Http.__init__(self, cache=cache, timeout=timeout,
            proxy_info=proxy_info)

    def get_signature(self):
        return self._signature

    def set_signature(self, signature):
        if not isinstance(signature, SignatureMethod):
            raise ValueError("Invalid signature method.")
        self._signature = signature

    signature = property(get_signature, set_signature)

    def request(self, uri, method="GET", body=None, headers=None,
        redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None):

        if not isinstance(headers, dict):
            headers = {}

        if body and method == "POST":
            parameters = dict(parse_qsl(body))
        elif method == "GET":
            parsed = urlparse.urlparse(uri)
            parameters = parse_qs(parsed.query)
        else:
            parameters = None

        req = Request.from_consumer_and_token(self.consumer, token=self.token,
            http_method=method, http_url=uri, parameters=parameters,
            callback=self.callback_url)

        req.sign_request(self.signature, self.consumer, self.token)

        if method == "POST":
            body = req.to_postdata() 
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        elif method == "GET":
            uri = req.to_url()
        else:
            headers.update(req.to_header())

        return httplib2.Http.request(self, uri, method=method, body=body,
            headers=headers, redirections=redirections,
            connection_type=connection_type)
