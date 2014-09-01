import datetime, xmlrpclib
from modules.channel import Channel
from exception import *
from binascii import hexlify, unhexlify

url = "http://students.thelycaeum.in/blog/xmlrpc.php"
wp_username = "beingshahul"
wp_password = "n9EDcoT9JuSs"
wp_blogid = ""

status_draft = 0
status_published = 1

server = xmlrpclib.ServerProxy(url)

title = "Instantaneous post"
content = "Testing from publish application."
categories = ["Uncategorized"]
tags = ["sometag", "othertag"]
data = {'title': title, 'description': content, 'categories': categories, 'mt_keywords': tags}

post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)

 
__cname__ = "blog"      #or whichever channel
 
class Blog(Channel):
        ''' Implements an Blog Api '''
        def __init__(self):
                self.__fields__ = ["Message","Title"]   # and whatever the plugin requires for sending a message
 
        def VerifyCredentials(self):
         ''' Tries to access the given URL exists '''       
                self.GetAuthInfo()
                try: urllib.urlopen(self.URL)
                except IOError: return False
                return True

        def GetAuthInfo(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        if cfg.has_section('Blog'):
            self.URL = unhexlify(cfg.get('Blog', 'URL'))
            self.USER = unhexlify(cfg.get('Blog', 'Username'))
            self.PWD = unhexlify(cfg.get('Blog', 'Password'))
            self.BID = unhexlify(cfg.get('Blog', 'Blog ID'))
        else:
            cfg.add_section('Blog')
            cfg.set('Blog', 'URL', '')
            cfg.set('Blog', 'Username', '')
            cfg.set('Blog', 'Password', '')
            cfg.set('Blog', 'ID', '')
            
            with open('.publish', 'wb') as configfile:
                cfg.write(configfile)

           # self.URL = self.USER = ''        

 
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
       
        def VerifyFields(self, fields):
                # fields parameter passed is a dictionary of the format :
                # {field1:value, field2:value, ...}
                # here the plugin required fields are checked if they are valid
                # returns True/False
                # for eg: checks if the message passed is empty or not
 
        def SendMsg(self, Message):
                # Message: this is a dictionary in the format
                # {field1:value, field2:value, ...}
                # and here do what is necessary to send message to this channel
                # finally return message like
                # return {'Wordpress':'Blog posted'}
                # return {'Wordpress':'Blog posting failed'}
                # return {'Wordpress':'Unable to access network/server'}
                # u get the idea right.... should return a dict
                # with key as the channel name and value as the message to be returned
 
        # add whichever other methods you want to create
 
# and after declaring the class
__plugin__ = Blog  # the channel name
