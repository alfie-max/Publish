class Facebook(object):
    def __init__(self):
    	self.__fields__ = ['Message']
        print "I am the facebook channel"

    def VerifyCredentials(self):
    	return True

    def SendMsg(self, msg):
      return 0

__plugin__ = Facebook
__cname__ = 'facebook'