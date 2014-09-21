import tweepy
class OAuthHandler(tweepy.OAuthHandler):

   def __init__(self, consumer_key, consumer_secret, callback=None, secure=True):
       self.access_token = self.Access_Token()

   def get_authorization_url(self):
      return 'http://www.example.com'

   def get_access_token(self, pin):
      self.access_token.key = ''
      self.access_token.secret = ''

   def set_access_token(self, token_key, token_secret):
      self.access_token.key = token_key
      self.access_token.secret = token_secret

   class Access_Token(object):
      def __init__(self):
         self.key = ''
         self.secret = ''
   
class error(tweepy.TweepError):
   def __init__(self):pass
   class TweepError(Exception):pass

class API(tweepy.OAuthHandler):
   
   def __init__(self, auth):
      pass
      
   def verify_credentials(self):
      pass

   def update_status(self, msg):
      if len(msg) > 25:
         raise error.TweepError([{u'message': u'Too Long.', u'code': 185}])

   def update_with_media(self, msg):
      pass

def ui_prompt(msg, mask=None):
   return ''
