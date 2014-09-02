#from tests.exception import *

class Email(object):
    def __init__(self):
    	self.__fields__ = ['Message']

    def VerifyCredentials(self):
    	return False

    def Authorize(self):
    	raise AuthorizationError("UnAuthorized")

__plugin__ = Email
__cname__ = 'email'
