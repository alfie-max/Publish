import xmlrpclib

def ServerProxy(url):
    server = Server()
    return server

def ui_prompt(msg, mask=None): return ''
def ui_print(msg): return ''

class Server(object):
    def __init__(self):
        self.metaWeblog = metaWeblog()

class metaWeblog(object):
    def __init__(self):pass
    def getRecentPosts(self, n, username, password, count):pass
    def newPost(self, blogid, username, password, data, status):pass

class Fault(Exception):pass

