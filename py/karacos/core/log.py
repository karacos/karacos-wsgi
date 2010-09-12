'''
Created on 10 sept. 2010

@author: nico
'''
import logging
from logging import NOTSET
import sys, traceback
import karacos

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

def get_level(level_def):
    try:
        level_name = level_def
        level = LEVELS.get(level_name, logging.NOTSET)
        return level
        #logging.basicConfig(level=level)
    except:
        logging.critical(sys.exc_info())
        
class Logger(logging.getLoggerClass()):
    '''
    classdocs
    '''
    
    def __init__(self, name, level=NOTSET):
        '''
        Constructor
        '''
        logging.Logger.__init__(self, name, level)
    
    def log_exc(self,exc_info,level='info'):
        exceptionType, exceptionValue,exceptionTraceback = exc_info
        msg = 'raised %s : %s \n %s' % (exceptionType, exceptionValue,traceback.format_tb(exceptionTraceback))
        self.log(get_level(level),msg)


import logging.config
logging.setLoggerClass(Logger)



def getLogger(instance):
    return logging.getLogger("%s.%s" % (instance.__class__.__module__,instance.__class__.__name__))

logging.config.fileConfig("%s/logging.conf" % karacos._confdir)

