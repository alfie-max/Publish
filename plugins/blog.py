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
        ''' Blog class Constructor '''
        self.__fields__ = ["Message","Title"]    

    def GetAuthInfo(self):
        '''
        Reads authentication data required from config file
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        
        if cfg.has_section('Blog'):
            self.url = cfg.get('Blog', 'URL')
            self.username = cfg.get('Blog', 'Username')
            self.password = unhexlify(cfg.get('Blog', 'Password'))
        else:
            self.url = self.username = self.password = ''

    def Reset(self):
        '''
        Resets auth data in config file
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Blog'):
            cfg.add_section('Blog')
        cfg.set('Blog', 'URL', '')
        cfg.set('Blog', 'Username', '')
        cfg.set('Blog', 'Password', '')
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

    def VerifyCredentials(self):
        '''
        Verifies Users Credentials stored in the config file.
        Returns True/False
        '''
        self.GetAuthInfo()
        try:
            server = xmlrpclib.ServerProxy(self.url)
        except IOError:
            server = xmlrpclib.ServerProxy('http://abc.xyz')

        try:
            server.metaWeblog.getRecentPosts('', self.username, self.password, 1)
            return True
        except (xmlrpclib.Fault, gaierror):
            raise NetworkError('Unable to access network')
        except (xmlrpclib.ProtocolError, IOError):
            return False
    
    def Authorize(self):
        '''
        Authorize the application with Blog.
        '''
        ui_print (colored('Authorizing Blog Account...', 'yellow'))
        self.url = ui_prompt("Blog URL : ")
        self.username = ui_prompt("Username : ")
        self.password = ui_prompt("Password : ", mask = True)

        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Blog'):
            cfg.add_section('Blog')
        cfg.set('Blog', 'URL', self.url)
        cfg.set('Blog', 'Username', self.username)
        cfg.set('Blog', 'Password', hexlify(self.password))
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

        if not self.VerifyCredentials():
            raise AuthorizationError('Authorization Failed')
       
    def VerifyFields(self, Blog):
        '''
        Verifies passed fields to follow requirements of Blog.
        '''
        Message = Blog['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False
 
    def SendMsg(self, Blog):
        '''
        Sent Message to Blog.
        '''
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
__cfgfile__ = '.publish'
