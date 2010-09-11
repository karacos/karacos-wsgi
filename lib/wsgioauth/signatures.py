# -*- coding: utf-8 -*-
from oauth2 import escape, SignatureMethod_HMAC_SHA1, SignatureMethod_PLAINTEXT

from wsgioauth.utils import get_normalized_parameters

class HMAC_SHA1(SignatureMethod_HMAC_SHA1):

    def signing_base(self, request, consumer, token):
        sig = (
            escape(request.method),
            escape(request.path_url),
            escape(get_normalized_parameters(request)),
        )

        key = '%s&' % escape(consumer.secret)
        if token:
            key += escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

PLAINTEXT = SignatureMethod_PLAINTEXT
