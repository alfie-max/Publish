import ConfigParser
import tweepy
import tempfile
import cookielib

from os import unlink
from urllib2 import URLError
from termcolor import colored
from mechanize import Browser
from bs4 import BeautifulSoup
from os.path import expanduser
from modules.consumer import *
from modules.exception import *
from modules.channel import Channel
from modules.ui import ui_print, ui_prompt
from binascii import hexlify, unhexlify
from PIL import Image, ImageDraw, ImageFont


class Twitter(Channel):
    ''' Implementation of Twitter Api '''
    def __init__(self):
        ''' Twitter class Constructor '''
        self.CON_KEY = unhexlify(CKEY)
        self.CON_SEC = unhexlify(CSEC)
        self.__fields__ = ['Message']
        
    def VerifyCredentials(self):
        '''
        Verifies Users Credentials stored in the config file.
        Returns True/False
        '''
        try:
            self.GetAuthInfo()
        except TypeError:
            return False
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        self.api = tweepy.API(auth)
 
        try:
            self.api.verify_credentials()
            return True
        except tweepy.error.TweepError:
            return False

    def GetAuthInfo(self):
        '''
        Read Stored API Keys from config file.
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        
        if cfg.has_section('Twitter'):
            self.TOKEN = unhexlify(cfg.get('Twitter', 'Token Key'))
            self.TOKEN_SEC = unhexlify(cfg.get('Twitter', 'Token Secret'))
        else:
            self.TOKEN = self.TOKEN_SEC = ''


    def Reset(self):
        '''
        Resets stored API Keys in config file to None.
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        
        if not cfg.has_section('Twitter'):
            cfg.add_section('Twitter')
        cfg.set('Twitter', 'Token Key', '')
        cfg.set('Twitter', 'Token Secret', '')
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)
        
    def Authorize(self):
        '''
        Authorize the application with Twitter.
        '''
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)

        try:
            auth_url = auth.get_authorization_url()
        except tweepy.error.TweepError:
            raise NetworkError('Unable to access network')

        ui_print (colored('Authorizing Twitter Account...', 'yellow'))
        username = ui_prompt("Username : ")
        password = ui_prompt("Password : ", mask = True)

        ''' Initialize mechanize browser instance '''
        br = Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        ''' Opens browser and authenticate account '''
        try:
            br.open(auth_url)
        except URLError:
            raise NetworkError('Unable to access network')

        br.form = list(br.forms())[0]
        br.form['session[username_or_email]'] = username
        br.form['session[password]'] = password

        try:
            response = br.submit()
        except URLError:
            br.close()
            raise NetworkError('Unable to access network')

        content = response.get_data()

        soup = BeautifulSoup(content)
        code = soup.find('code')

        if code:
            pin = code.text
            br.close()
        else:
            br.form = list(br.forms())[1]
            try:
                response = br.submit()
            except URLError:
                br.close()
                raise NetworkError('Unable to access network')

            content = response.get_data()
            br.close()
            soup = BeautifulSoup(content)
            code = soup.find('code')
            if code:
                pin = code.text
            else:
                raise AuthorizationError('Authorization Failed')

        try:
            auth.get_access_token(pin)
        except tweepy.error.TweepError, e:
            raise AuthorizationError('Authorization Failed')
        
        self.TOKEN = auth.access_token.key
        self.TOKEN_SEC = auth.access_token.secret
 
        ''' Update Config file with Token Keys '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Twitter'):
            cfg.add_section('Twitter')
        cfg.set('Twitter', 'Token Key', hexlify(self.TOKEN))
        cfg.set('Twitter', 'Token Secret', hexlify(self.TOKEN_SEC))
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

        if not self.VerifyCredentials():
            self.Reset()
            raise AuthorizationError('Authorization Failed')

    def Text2Img(self, Message):
        '''
        Creates an image containing the Message.
        '''
        fontname = 'plugins/Tahoma.ttf'
        fontsize = 22
        textColor = (102,117,127)
        bgColor = 'white'
        maxWidth = 500

        font = ImageFont.truetype(fontname, fontsize)
        lines, width, height = self.IntelliDraw(Message, font, maxWidth)
        imgHeight = (height +10) * len(lines)
        img = Image.new('RGB', (width + 35, imgHeight), bgColor)
        draw = ImageDraw.Draw(img)

        for i, line in enumerate(lines):
            draw.text((10, 0 + i*(height+10)), line, font = font, fill = textColor)

        filePath = tempfile.NamedTemporaryFile(suffix = '.png').name

        img.save(filePath)
        return filePath
        
    def IntelliDraw(self, msg, font, maxWidth):
        '''
        Slices a long message and creates paragraphs.
        '''
        testimg = Image.new('RGB', (1024, 728))
        drawer = ImageDraw.Draw(testimg)
        words = msg.split()
        lines = []
        lines.append(words)
        finished = False
        line = 0
        while not finished:
            thistext = lines[line]
            newline = []
            innerFinished = False
            while not innerFinished:
                if drawer.textsize(' '.join(thistext) ,font)[0] > maxWidth:
                    newline.insert(0, thistext.pop(-1))
                else:
                    innerFinished = True
            if len(newline) > 0:
                lines.append(newline)
                line = line + 1
            else:
                finished = True
        tmp = []
        for i in lines:
            tmp.append( ' '.join(i) )
        lines = tmp
        (width, height) = drawer.textsize(lines[0], font)
        return (lines, width, height)

    def Tweet(self, Message):
        '''
        Handles Sending of message
        '''
        try:
            self.api.update_status(Message)
            return True
        except tweepy.error.TweepError, e:
            dup_msg = False
            try:
                if e.message[0]['code'] == 187:
                    raise Failed('Duplicate Message')
            except AttributeError:
                pass
            if not dup_msg:
                Image = self.Text2Img(Message)
                try:
                    self.api.update_with_media(Image)
                    unlink(Image)
                    return True
                except tweepy.error.TweepError:
                    unlink(Image)
                    return False

    def VerifyFields(self, msg):
        '''
        Verifies passed fields to follow requirements of Twitter.
        '''
        Message = msg['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False

    def SendMsg(self, msg):
        '''
        Sent Message to Twitter.
        '''
        Message = msg['Message']
        Message = Message.strip()
        
        self.GetAuthInfo()
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        self.api = tweepy.API(auth)
        ui_print (colored('Sending Twitter Message...', 'blue'))
        if self.Tweet(Message):
            ui_print (colored('Successfully Sent', 'green'))
        else:
            ui_print (colored('Sending Failed', 'red'))

__plugin__ = Twitter
__cname__ = 'twitter'
__cfgfile__ = expanduser('~') + '/.publish'
