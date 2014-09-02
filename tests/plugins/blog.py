class Blog(object):
    def __init__(self):
    	self.__fields__ = ['Message']

    def VerifyFields(self, fields):
        return False

__plugin__ = Blog
__cname__ = 'blog'
