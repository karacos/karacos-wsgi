'''
Created on 14 sept. 2010

@author: KaragNi
'''

from BaseHTTPServer import BaseHTTPRequestHandler
response_codes = BaseHTTPRequestHandler.responses.copy()

import karacos

def file_generator_limited(fileobj, count, chunk_size=65536):
    """Yield the given file object in chunks, stopping after `count`
    bytes has been emitted.  Default chunk size is 64kB. (Core)
    """
    remaining = count
    while remaining > 0:
        chunk = fileobj.read(min(chunk_size, remaining))
        chunklen = len(chunk)
        if chunklen == 0:
            return
        remaining -= chunklen
        yield chunk

def valid_status(status):
    """Return legal HTTP status Code, Reason-phrase and Message.
    
    The status arg must be an int, or a str that begins with an int.
    
    If status is an int, or a str and  no reason-phrase is supplied,
    a default reason-phrase will be provided.
    """
    
    if not status:
        status = 200
    
    status = str(status)
    parts = status.split(" ", 1)
    if len(parts) == 1:
        # No reason supplied.
        code, = parts
        reason = None
    else:
        code, reason = parts
        reason = reason.strip()
    
    try:
        code = int(code)
    except ValueError:
        raise ValueError("Illegal response status from server "
                         "(%s is non-numeric)." % repr(code))
    
    if code < 100 or code > 599:
        raise ValueError("Illegal response status from server "
                         "(%s is out of range)." % repr(code))
    
    if code not in response_codes:
        # code is unknown but not illegal
        default_reason, message = "", ""
    else:
        default_reason, message = response_codes[code]
    
    if reason is None:
        reason = default_reason
    
    return code, reason, message

def validate_since():
    """Validate the current Last-Modified against If-Modified-Since headers.
    
    If no code has set the Last-Modified response header, then no validation
    will be performed.
    """
    response = karacos.serving.get_response()
    lastmod = response.headers.get('Last-Modified')
    if lastmod:
        status, reason, msg = valid_status(response.status)
        
        request = karacos.serving.get_request()
        
        since = request.headers.get('If-Unmodified-Since')
        if since and since != lastmod:
            if (status >= 200 and status <= 299) or status == 412:
                raise karacos.http.HTTPError(412)
        
        since = request.headers.get('If-Modified-Since')
        if since and since == lastmod:
            if (status >= 200 and status <= 299) or status == 304:
                if request.method in ("GET", "HEAD"):
                    raise karacos.http.Redirect([], 304)
                else:
                    raise karacos.http.HTTPError(412)