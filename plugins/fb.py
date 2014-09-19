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

APP_ID = unhexlify(APP_ID)
APP_SEC = unhexlify(APP_SEC)
ACCESS_TOKEN = None

class Facebook(Channel):
    ''' Implememts Facebook Api '''
    def __init__(self):
        ''' Facebook class Constructor '''
        self.__fields__ = ['Message']

    def GetAuthInfo(self):
        '''
        Reads authentication data required from config file
        '''
        global ACCESS_TOKEN
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)

        if cfg.has_section('Facebook'):
            ACCESS_TOKEN = unhexlify(cfg.get('Facebook', 'Access Token'))            
        else:
            ACCESS_TOKEN = ''
            
    def Reset(self):
        '''
        Resets auth data in config file
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Facebook'):
            cfg.add_section('Facebook')
        cfg.set('Facebook', 'Access Token', '')
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

    def VerifyCredentials(self):
        '''
        Verifies Users Credentials stored in the config file.
        Returns True/False
        '''
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
        '''
        Authorize the application with Facebook.
        '''
        global ACCESS_TOKEN
        ACCESS_TOKEN = None
        ENDPOINT = 'graph.facebook.com'
        REDIRECT_URI = 'http://127.0.0.1:8080/'
        
        ''' Requirements for Facebook Authentication '''
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

        def get_url(path, args=None):
            args = args or {}
            if ACCESS_TOKEN:
                args['access_token'] = ACCESS_TOKEN
            if 'access_token' in args or 'client_secret' in args:
                endpoint = "https://" + ENDPOINT
            else:
                endpoint = "http://" + ENDPOINT
            return endpoint + path + '?' + urllib.urlencode(args)

        def get(path, args):
            return urllib2.urlopen(get_url(path, args=args)).read()
        
        ''' Steps to authenticate '''
        ui_print (colored('Authorizing Facebook Account...', 'yellow'))
        auth_url = get_url('/oauth/authorize',
                           {'client_id' : APP_ID,
                            'redirect_uri' : REDIRECT_URI,
                            'scope' : 'publish_actions'})

        ''' Silence webbrowser messages '''
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(auth_url)
        finally:
            os.dup2(savout, 1)

        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 8080), RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()

        ''' Update Config file with Token Keys '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Facebook'):
            cfg.add_section('Facebook')
        cfg.set('Facebook', 'Access Token', hexlify(ACCESS_TOKEN))
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

        if not self.VerifyCredentials():
            raise AuthorizationError('Authorization Failed')

    def VerifyFields(self, msg):
        '''
        Verifies passed fields to follow requirements of Facebook.
        '''
        Message = msg['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False

    def SendMsg(self, msg):
        '''
        Sent Message to Facebook.
        '''
        Message = msg['Message']
        Message = Message.strip()
        
        self.GetAuthInfo()
        fb = facebook.GraphAPI()
        fb.access_token = ACCESS_TOKEN
        ui_print (colored('Sending Facebook Message...', 'blue'))
        try:
            fb.put_wall_post(Message)
            ui_print (colored('Successfully Sent', 'green'))
        except urllib2.URLError:
            raise NetworkError('Unable to access network')
        except facebook.GraphAPIError:
            ui_print (colored('Sending Failed', 'red'))

__plugin__ = Facebook
__cname__ = 'facebook'
__cfgfile__ = '.publish'
