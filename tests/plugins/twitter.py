class Twitter(object):
    def __init__(self):
    	self.__fields__ = ['Message']

    def VerifyCredentials(self):
    	return False

    def Authorize(self):
        pass   	

    def VerifyFields(self, fields):
        return True

    def SendMsg(self, msg):
      return {'':''}

__plugin__ = Twitter
__cname__ = 'twitter'
