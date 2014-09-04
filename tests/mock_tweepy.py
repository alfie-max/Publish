class OAuthHandler(object):

   def __init__(self, consumer_key, consumer_secret, callback=None, secure=True):
       self.access_token = self.Access_Token()

   def get_authorization_url(self):
      return 'http://www.example.com'

   def get_access_token(self, pin):
      self.access_token.key = 'key'
      self.access_token.secret = 'secret'


   def set_access_token(self, token_key, token_secret):
      self.access_token.key = token_key
      self.access_token.secret = token_secret

   class Access_Token(object):
      def __init__(self):
         self.key = ''
         self.secret = ''
   
class API(object):
   
    def __init__(self, auth):
        pass
      
    def verify_credentials(self):
        pass

    def update_status(self, msg):
        if len(msg) > 25:
            raise error.TweepError

    def update_with_media(self, msg):
        pass

class error(object):
    class TweepError(Exception): pass

def raw_input(msg):
    return ''
