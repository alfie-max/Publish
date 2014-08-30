from tests.exception import *

class Email(object):
    def __init__(self):
    	self.__fields__ = ['Message']
        print "I am the email channel"

    def VerifyCredentials(self):
    	return False

    def Authorize(self):
    	raise AuthorizationError("UnAuthorized")

__plugin__ = Email
__cname__ = 'email'