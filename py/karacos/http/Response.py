'''
Created on 10 sept. 2010

@author: KaragNi
'''
import webob
class Response(webob.Response):
    '''
    classdocs
    '''
    def __init__(self,*args,**kw):
        
        webob.Response.__init__(self,*args, **kw)
        
        self.__instance__ = None
        self.__result__ = None
        self.__action__ = None