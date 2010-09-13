# -*- coding: utf-8 -*-
import urllib
from oauth2 import Consumer
from webob import Request, Response

from wsgioauth import calls
from wsgioauth.provider import Application, Storage
from wsgioauth.utils import CALLS
from wsgioauth.provider import Storage, Token

ROUTES = {
    u'getConsumers': calls.getConsumers,
    u'getRequestTokens': calls.getRequestTokens,
    u'getAccessTokens': calls.getAccessTokens,
    u'provisionConsumer': calls.provisionConsumer,
    u'provisionRequestToken': calls.provisionRequestToken,
    u'provisionAccessToken': calls.provisionAccessToken,
    u'deleteConsumer': calls.deleteConsumer,
    u'deleteRequestToken': calls.deleteRequestToken,
    u'deleteAccessToken': calls.deleteAccessToken,
    }

def getMockStorage():
    from wsgioauth.provider import OAUTH_CLASSES
    OAUTH_CLASSES['consumer'] = Consumer
    OAUTH_CLASSES['request_token'] = Token
    return Storage


def echo_app(environ, start_response):
    """Simple app that echos a POST request"""
    req = Request(environ)
    resp = Response(urllib.urlencode(req.params))
    return resp(environ, start_response)

def echo_app_factory(*global_conf, **local_conf):
    return echo_app

STORAGE = None

def app_factory(*global_conf, **local_conf):
    CALLS.update(ROUTES)
    global STORAGE
    if STORAGE is None:
        storage_cls = getMockStorage()
        STORAGE = storage_cls(local_conf)
    def storage_lookup(environ, conf):
        return STORAGE
    return Application(storage_lookup, **local_conf)

def filter_factory(app, *global_conf, **local_conf):
    """This function returns a wsgioauth.provider.Filter services factory."""
    from wsgioauth.mock import getMockStorage
    global STORAGE
    if STORAGE is None:
        storage_cls = getMockStorage()
        STORAGE = storage_cls(local_conf)
    def storage_lookup(environ, conf):
        return STORAGE
    from wsgioauth.provider import Middleware
    return Middleware(app, storage_lookup, **local_conf)

