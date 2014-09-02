class Facebook(object):
    def __init__(self):
    	self.__fields__ = ['Message']

    def VerifyCredentials(self):
    	return True

    def VerifyFields(self, fields):
        return True

    def SendMsg(self, msg):
      return 0

__plugin__ = Facebook
__cname__ = 'facebook'
