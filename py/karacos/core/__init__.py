class Exception(Exception):
    """
    Base exception class for Db
    """
    def __init__(self, value=None):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


import log
import apps
import mail