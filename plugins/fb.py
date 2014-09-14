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
        self.__fields__ = ["Message"]   # and whatever the plugin requires for sending a message
        
    def GetAuthInfo(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        if cfg.has_section('Facebook'):
            self.appid = cfg.get('Facebook', 'Application ID')
            self.appsecret = unhexlify(cfg.get('Facebook', 'App Secret'))
            self.profileid = cfg.get('Facebook', 'Profile ID')
            
        else:
            cfg.add_section('Facebook')
            cfg.set('Facebook', 'Application ID', '')
            cfg.set('Facebook', 'App Secret', '')
            cfg.set('Facebook', 'Profile ID', '')
            with open('.publish', 'wb') as configfile:
                cfg.write(configfile)

           # self.URL = self.USER = ''        

    def VerifyCredentials(self):
        oauth_args = dict(client_id     = self.appid,
                  client_secret = self.appsecret,
                  grant_type    = 'client_credentials')
        oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
        oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]
 
        try:
        oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'] [0]  
        except KeyError:
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
