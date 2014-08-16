import ConfigParser
import tweepy

from channel import Channel
from binascii import hexlify, unhexlify

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
        
    def Tweet(self, Message):
        try:
            self.api.update_status(Message)
            #print 'Status Updated Successfully on Twitter'
            return True
        except tweepy.error.TweepError, e:
            #print e.message[0]['message']
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
