# -*- coding: utf-8 -*-
import xmlrpclib
from oauth2 import Consumer, Token
from wsgioauth.xmlrpc import xmlrpc

__all__ = (
    'getConsumers', 'getRequestTokens', 'getAccessTokens',
    'provisionConsumer', 'provisionRequestToken', 'provisionAccessToken',
    'deleteConsumer', 'deleteRequestToken', 'deleteAccessToken',
    )

def get_tokens(container, keys=[]):
    tokens = {}
    if keys == []:
        keys = container.keys()
    for k, v in container.iteritems():
        if k in keys:
            tokens[k] = dict(key=v.key, secret=v.secret)
    return tokens

# 
# The following are get type XML-RPC functions.
# 

@xmlrpc
def getConsumers(store, keys=[]):
    """A way to list all the consumers."""
    return get_tokens(store.consumers, keys)

@xmlrpc
def getRequestTokens(store, keys=[]):
    """List all or grab one or more request token in the storage."""
    return get_tokens(store.request_tokens, keys)

@xmlrpc
def getAccessTokens(store, keys=[]):
    """List all or grab one or more access token in the storage."""
    return get_tokens(store.access_tokens, keys)

# 
# The following XML-RPC functions are used to provision consumers and tokens.
# 

@xmlrpc
def provisionConsumer(store, params={}):
    """Provision a consumer and return the key and secret."""
    # retrieve the variables from the params argument
    key = params.get('key', None)
    secret = params.get('secret', None)
    # title = params.get('title', '')
    # description = params.get('description', '')
    # email = params.get('email', None)

    # call the storage abstration to add a consumer
    consumer = store.add_consumer(key, secret) #, title=title, description=description)
    return {consumer.key: {'key': consumer.key, 'secret': consumer.secret}}

@xmlrpc
def provisionRequestToken(store, params={}):
    """provision a token and return the key and secret"""
    # retrieve the variables from the params argument
    # key = params.get('key', None)
    # secret = params.get('secret', None)
    # callback = params.get('callback', None)
    # verifier = params.get('verifier', None)

    token = store.add_request_token(**params)
    response_data = {'key': token.key, 'secret': token.secret}
    if token.callback:
        response_data['callback'] = token.callback
    if token.verifier:
        response_data['verifier'] = token.verifier

    return response_data

@xmlrpc
def provisionAccessToken(store, params={}):
    """provision a token and return the key and secret"""
    # retrieve the variables from the params argument
    # key = params.get('key', None)
    # secret = params.get('secret', None)
    # callback = params.get('callback', None)
    # verifier = params.get('verifier', None)

    token = store.add_access_token(**params)
    response_data = {'key': token.key, 'secret': token.secret}
    return response_data

# 
# The following are used to delete consumers and tokens.
# 

@xmlrpc
def deleteConsumer(store, key):
    """Delete a consumer from the storage."""
    try:
        del store.consumers[key]
    except KeyError:
        raise xmlrpclib.Fault(-1, "The requested consumer does not exist.")
    # according to the xml-rpc spec, we need to return something
    return True

@xmlrpc
def deleteRequestToken(store, key):
    """Delete a request token from the storage."""
    try:
        del store.request_tokens[key]
    except KeyError:
        raise xmlrpclib.Fault(-1, "The requested request token does not exist.")
    # according to the xml-rpc spec, we need to return something
    return True

@xmlrpc
def deleteAccessToken(store, key):
    """Delete an access token from the storage."""
    try:
        del store.access_tokens[key]
    except KeyError:
        raise xmlrpclib.Fault(-1, "The requested access token does not exist.")
    # according to the xml-rpc spec, we need to return something
    return True
