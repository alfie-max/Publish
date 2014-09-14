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

    def Authorize(self):
        global ACCESS_TOKEN
        ACCESS_TOKEN = None
        ENDPOINT = 'graph.facebook.com'
        REDIRECT_URI = 'http://127.0.0.1:8080/'
        
        ''' Requirements for facebook authentication '''
        class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                global ACCESS_TOKEN

                code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
                code = code[0] if code else None
                if code is None:
                    self.wfile.write('Sorry, authentication failed.')
                    raise AuthorizationError('Authorization Failed')
                response = get('/oauth/access_token',
                               {'client_id' : APP_ID,
                                'redirect_uri' : REDIRECT_URI,
                                'client_secret' : APP_SEC,
                                'code' : code})

                ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
                self.wfile.write('You have successfully logged in to facebook.'
                                 'You can close this window now.')
            def log_message(self, format, *args):
                return

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
