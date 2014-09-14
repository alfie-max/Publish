import os
import urllib
import urllib2
import urlparse
import facebook
import webbrowser
import ConfigParser
import BaseHTTPServer

from modules.consumer import *
from modules.exception import *
from termcolor import colored
from modules.channel import Channel
from binascii import hexlify, unhexlify
from modules.ui import ui_print, ui_prompt
 

 
class Facebook(Channel):
        ''' Implements Facebook Api '''
    def __init__(self):
        self.__fields__ = ["Message"]   
        
    def GetAuthInfo(self):
         ''' Read Keys from Config file '''
        global ACCESS_TOKEN
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')

        if cfg.has_section('Facebook'):
            ACCESS_TOKEN = unhexlify(cfg.get('Facebook', 'Access Token'))            
        else:
            ACCESS_TOKEN = ''

    def Reset(self):
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        if not cfg.has_section('Facebook'):
            cfg.add_section('Facebook')
        cfg.set('Facebook', 'Access Token', '')
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)     

    def VerifyCredentials(self):
        self.GetAuthInfo()
        fb = facebook.GraphAPI()
        fb.access_token = ACCESS_TOKEN
        try:
            fb.get_object('me')
            return True
        except urllib2.URLError:
            raise NetworkError('Unable to access network')
        except facebook.GraphAPIError:
            return False

    def GetKeys(self):
        facebook_graph = facebook.GraphAPI(oauth_access_token)
    def Authorize(self):
          """ Get Facebook authentication data """
        print "Please Authenticate your Facebook Account"
        self.appid= raw_input("Enter your Facebook APP ID ")
        self.appsecret  = getpass("App Secret : ")
        self.profileid = raw_input("Profile ID : ")
        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        if not cfg.has_section('Facebook'):
            cfg.add_section('Facebook')
        cfg.set('Facebook', 'App ID', self.appid)
        cfg.set('Facebook', 'App Secret', hexlify(self.appsecret))
        cfg.set('Facebook', 'Password', self.profileid)
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)
        if not self.VerifyCredentials():
            raise AuthorizationError(__cname__)

    def VerifyFields(self, fields):
        Message = Facebook['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False
    def SendMsg(self, Message):
        try:
        fb_response = facebook_graph.put_wall_post(Message,profile_id  = self.profileid )
        print fb_response
        except facebook.GraphAPIError as e:
        print 'Something went wrong:'

 

__plugin__ = Facebook  
__cname__ = "facebook"      
