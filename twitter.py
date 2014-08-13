import ConfigParser
import tweepy

from channel import Channel
from binascii import hexlify, unhexlify

class Twitter(Channel):
    ''' Implements Twitter Api '''

    def VerifyCredentials(self):
        ''' Verify Users Credentials '''
        self.GetKeys()
        self.api = self.TwitterApi()
        
        try:
            name =  self.api.me().name
            return True, name
        except tweepy.error.TweepError:
            print 'Invalid Credentials'
            return False

    def GetKeys(self):
        ''' Read Keys from Config file '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        self.CON_KEY = unhexlify(cfg.get('Twitter', 'Consumer Key'))
        self.CON_SEC = unhexlify(cfg.get('Twitter', 'Consumer Secret'))
        self.TOKEN = unhexlify(cfg.get('Twitter', 'Token Key'))
        self.TOKEN_SEC = unhexlify(cfg.get('Twitter', 'Token Secret'))
        
    def TwitterApi(self):
        '''  Create a Twitter Api Instance '''
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth.set_access_token(self.TOKEN, self.TOKEN_SEC)
        return tweepy.API(auth)


    def Authorize(self):
        ''' Authorize the application with Twitter '''
        self.GetKeys()
        auth = tweepy.OAuthHandler(self.CON_KEY, self.CON_SEC)
        auth_url = auth.get_authorization_url()

        print "Please Authorize the application : " + auth_url
        pin = raw_input("Enter the pin : ")

        ''' Request Access Token from Twitter '''
        try:
            auth.get_access_token(pin)
        except tweepy.error.TweepError, e:
            print e.message.msg, ', Please try again later'
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
        
        keys = [('Token Key', self.TOKEN), ('Token Secret', self.TOKEN_SEC)]
        return keys
        

    def SendMsg(self, Message):
        ''' Sent Message to Twitter '''
        if self.VerifyCredentials():
            try:
                self.api.update_status(Message)
                print 'Status Updated Successfully on Twitter'
            except tweepy.error.TweepError, e:
                print e.message[0]['message']
        else:
            print "Please Authorize the application with your Twitter account"
