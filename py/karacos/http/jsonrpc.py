'''
Created on 14 sept. 2010

@author: nico
'''

class ErrorOrigin:
    'XXX-RPC error origins'
    Server    = 1
    Application    = 2
    #server can return only 1 and 2
    Transport    = 3
    Client    = 4
    
class ErrorCode:
    "XXX-RPC server-generated error codes"
    Unknown = 0
    #these must be used if origin is server
    IllegalService    = 1
    ServiceNotFound    = 2
    ClassNotFound    = 3
    MethodNotFound    = 4
    ParameterMismatch    = 5
    PermissionDenied    = 6