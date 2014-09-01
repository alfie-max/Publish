import datetime, xmlrpclib
from modules.channel import Channel
from exception import *
from binascii import hexlify, unhexlify


class Blog(Channel):
        ''' Implements an Blog Api '''
        def __init__(self):
                self.__fields__ = ["Message","Title"]   # and whatever the plugin requires for sending a message
 
        def GetAuthInfo(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        if cfg.has_section('Blog'):
            self.url = cfg.get('Blog', 'URL')
            self.username = cfg.get('Blog', 'Username')
            self.password = unhexlify(cfg.get('Blog', 'Password'))
            
        else:
            cfg.add_section('Blog')
            cfg.set('Blog', 'URL', '')
            cfg.set('Blog', 'Username', '')
            cfg.set('Blog', 'Password', '')
            with open('.publish', 'wb') as configfile:
                cfg.write(configfile)

           # self.URL = self.USER = ''        



        def VerifyCredentials(self):
         ''' Tries to access the given URL exists '''       
                self.GetAuthInfo()
                try: urllib.urlopen(self.url)
                except IOError: return False
                return True

        
 
        def GetKeys(self):
                # You can look at this function from any other plugin, u'll just need to make a few changes
                # which are channel specific
 
        def Authorize(self):
                # here ask user for authentication info and save it in the .publish file
                # how to do that can be seen if u look at any existing plugins
                # Finally after saving the auth info
                # call VerifyCredentials and check if the given info is worth it
                # if it fails do :
                # raise AuthorizationError({'Wordpress':'Authorization Failed'})
                # i.e raise the AuthorizationError exception and pass a dict with channel name as key
                # and value as the message to be returned to ui

        """ Get user blog authentication data """
        print "Please Authenticate your Blog Account"
        self.url = raw_input("Blog URL : ")
        self.username = raw_input("Username : ")
        self.password = getpass("Password : ")

        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        if not cfg.has_section('Blog'):
            cfg.add_section('Blog')
        cfg.set('Blog', 'URL', self.url)
        cfg.set('Blog', 'Username', self.username)
        cfg.set('Blog', 'Password', hexlify(self.password))
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)

        if not self.VerifyCredentials():
            raise AuthorizationError(__cname__)
       
        def VerifyFields(self, Blog):
        Message = Blog['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False
 
        def SendMsg(self, Blog):
        status_draft = 0
        status_published = 1
        blogid = ""

        server = xmlrpclib.ServerProxy(self.url)

        title = Blog['Title']
        content = Blog['Message']

        categories = ["Uncategorized"]
        tags = ["sometag", "othertag"]
        data = {'title': title, 'description': content, 'categories': categories, 'mt_keywords': tags}

        post_id = server.metaWeblog.newPost(blogid, self.username, exlify(self.password), data, status_published)





__plugin__ = Blog  # the channel name
__cname__ = "blog"      #or whichever channel
