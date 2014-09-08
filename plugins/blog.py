import xmlrpclib
import ConfigParser

from termcolor import colored
from socket import gaierror
from modules.ui import ui_print, ui_prompt
from modules.channel import Channel
from modules.exception import *
from binascii import hexlify, unhexlify

class Blog(Channel):
    ''' Implements a Blog Api '''
    def __init__(self):
        self.__fields__ = ["Message","Title"]    

    def GetAuthInfo(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        if cfg.has_section('Blog'):
            self.url = cfg.get('Blog', 'URL')
            self.username = cfg.get('Blog', 'Username')
            self.password = unhexlify(cfg.get('Blog', 'Password'))
        else:
            self.url = self.username = self.password = ''

    def VerifyCredentials(self):
        ''' Tries to access the given URL exists '''       
        self.GetAuthInfo()
        try:
            server = xmlrpclib.ServerProxy(self.url)
        except xmlrpclib.Error:
            raise NetworkError('Unable to access network')
        except IOError:
            return False

        try:
            server.metaWeblog.getRecentPosts('', self.username, self.password, 1)
            return True
        except (xmlrpclib.Fault, gaierror):
            raise NetworkError('Unable to access network')
        except IOError:
            return False
    
    def Authorize(self):
        ''' Get user blog authentication data '''
        ui_print (colored('Authorizing Blog Account...', 'yellow'))
        self.url = ui_prompt("Blog URL : ")
        self.username = ui_prompt("Username : ")
        self.password = ui_prompt("Password : ", mask = True)

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
            raise AuthorizationError('Authorization Failed')
       
    def VerifyFields(self, Blog):
        Message = Blog['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False
 
    def SendMsg(self, Blog):
        blogid = ""
        status_published = 1
        title = Blog['Title']
        content = Blog['Message']
        data = {'title': title, 'description': content}
        
        self.GetAuthInfo()
        ui_print (colored('Posting on blog {}...'.format(self.url), 'blue'))
        try:
            server = xmlrpclib.ServerProxy(self.url)
        except xmlrpclib.Error:
            raise NetworkError('Unable to access Server')

        try:
            server.metaWeblog.newPost(blogid, self.username, self.password, data, status_published)
            ui_print (colored('Successfully Posted', 'green'))
        except (xmlrpclib.Fault, gaierror):
            ui_print (colored('Blog Posting Failed', 'red'))

__plugin__ = Blog 
__cname__ = "blog"      
