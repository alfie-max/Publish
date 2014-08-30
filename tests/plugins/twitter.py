class Twitter(object):
    def __init__(self):
    	self.__fields__ = ['Message']
        print "I am the twitter channel"

    def VerifyCredentials(self):
    	return False

    def Authorize(self):
   		pass   	

    def SendMsg(self, msg):
      return 0

__plugin__ = Twitter
__cname__ = 'twitter'