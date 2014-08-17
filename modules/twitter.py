import ConfigParser
import tweepy
import tempfile

from os import unlink
from channel import Channel
from binascii import hexlify, unhexlify
from PIL import Image, ImageDraw, ImageFont

class Twitter(Channel):
    ''' Implements Twitter Api '''

    def VerifyCredentials(self):
        ''' Verify Users Credentials '''
        self.GetKeys()
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        self.api = tweepy.API(auth)
        
        try:
            name =  self.api.me().name
            return True, name
        except tweepy.error.TweepError:
            return False

    def GetKeys(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        
        CKEY = '3765316f446d4c436f38734d61394e78436446463468514275'
        CSEC = '65775a364252343742573976326e4e6732474c7a397639416678516f68545665796e63676c7179776d5561506b77534e6c4c'

        self.CON_KEY = unhexlify(CKEY)
        self.CON_SEC = unhexlify(CSEC)
        
        if cfg.has_section('Twitter'):
            self.TOKEN = unhexlify(cfg.get('Twitter', 'Token Key'))
            self.TOKEN_SEC = unhexlify(cfg.get('Twitter', 'Token Secret'))
        else:
            cfg.add_section('Twitter')
            cfg.set('Twitter', 'Token Key', '')
            cfg.set('Twitter', 'Token Secret', '')
            with open('.publish', 'wb') as configfile:
                cfg.write(configfile)

            self.TOKEN = self.TOKEN_SEC = ''        

    def Authorize(self):
        ''' Authorize the application with Twitter '''
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)

        try:
            auth_url = auth.get_authorization_url()
        except tweepy.error.TweepError:
            print 'Unable to access network, Please try again later'
            return False

        print "Please Authorize the application with Twitter : " + auth_url

        ''' Request Access Token from Twitter '''
        pin = raw_input("Enter the pin : ")
        try:
            auth.get_access_token(pin)
        except tweepy.error.TweepError, e:
            print 'Authorization Failed, Please try again later'
            return False
        
        self.TOKEN = auth.access_token.key
        self.TOKEN_SEC = auth.access_token.secret
        
        ''' Update Config file with Token Keys '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        cfg.set('Twitter', 'Token Key', hexlify(self.TOKEN))
        cfg.set('Twitter', 'Token Secret', hexlify(self.TOKEN_SEC))
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)
        
        return True


    def Text2Img(self, Message):
        ''' Creates an image containing the Message '''
        fontname = 'modules/Tahoma.ttf'
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
                unlink(Image)
                return True
            except tweepy.error.TweepError:
                unlink(Image)
                return False


    def SendMsg(self, Message):
        ''' Sent Message to Twitter '''
        if self.VerifyCredentials():
            if self.Tweet(Message):
                return True
        else:
            if self.Authorize():
                if self.VerifyCredentials():
                    if self.Tweet(Message):
                        return True
        
        return False
