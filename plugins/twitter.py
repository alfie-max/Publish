import os
import ConfigParser
import tweepy
import tempfile
import webbrowser

from modules.consumer import *
from modules.exception import *
from modules.channel import Channel
from binascii import hexlify, unhexlify
from PIL import Image, ImageDraw, ImageFont


class Twitter(Channel):
    ''' Implements Twitter Api '''
    def __init__(self):
        self.CON_KEY = unhexlify(CKEY)
        self.CON_SEC = unhexlify(CSEC)
        self.__fields__ = ['Message']
        
    def VerifyCredentials(self):
        ''' Verify Users Credentials '''
        self.GetAuthInfo()
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        self.api = tweepy.API(auth)
 
        try:
            self.api.verify_credentials()
            return True
        except tweepy.error.TweepError:
            return False

    def GetAuthInfo(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        if cfg.has_section('Twitter'):
            self.TOKEN = unhexlify(cfg.get('Twitter', 'Token Key'))
            self.TOKEN_SEC = unhexlify(cfg.get('Twitter', 'Token Secret'))
        else:
            self.TOKEN = self.TOKEN_SEC = ''

    def Authorize(self):
        ''' Authorize the application with Twitter '''
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)

        try:
            auth_url = auth.get_authorization_url()
        except tweepy.error.TweepError:
            raise Failed({'Twitter':'Unable to access network'})

        ''' Request Access Token from Twitter '''
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(auth_url)
        finally:
            os.dup2(savout, 1)

        pin = raw_input("Enter the pin : ")
        try:
            auth.get_access_token(pin)
        except tweepy.error.TweepError, e:
            raise AuthorizationError(__cname__)
        
        self.TOKEN = auth.access_token.key
        self.TOKEN_SEC = auth.access_token.secret

        if not self.VerifyCredentials():
            raise AuthorizationError({'Twitter':'Authorization Failed'})
        
        ''' Update Config file with Token Keys '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        if not cfg.has_section('Twitter'):
            cfg.add_section('Twitter')
        cfg.set('Twitter', 'Token Key', hexlify(self.TOKEN))
        cfg.set('Twitter', 'Token Secret', hexlify(self.TOKEN_SEC))
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)

    def Text2Img(self, Message):
        ''' Creates an image containing the Message '''
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
        ''' Slices the Message and creates paragraphs '''
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
        try:
            self.api.update_status(Message)
            return True
        except tweepy.error.TweepError, e:
            Image = self.Text2Img(Message)
            try:
                self.api.update_with_media(Image)
                os.unlink(Image)
                return True
            except tweepy.error.TweepError:
                os.unlink(Image)
                return False

    def VerifyFields(self, msg):
        Message = msg['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False

    def SendMsg(self, msg):
        ''' Sent Message to Twitter '''
        Message = msg['Message']
        Message = Message.strip()

        self.GetAuthInfo()
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        self.api = tweepy.API(auth)
        
        if self.Tweet(Message):
            return {'Twitter':'Message Sent'}
        else:
            return {'Twitter':'Message Sending Failed'}

__plugin__ = Twitter
__cname__ = 'twitter'
