import urllib2

class GraphAPI(object):
    def __init__(self):
        self.access_token = 'None'

    def get_object(self, obj):
        return True

    def put_wall_post(self, msg):
        if msg == 'None':
            return True
        if msg == 'error':
            raise GraphAPIError('error')
        if msg == 'neterror':
            raise urllib2.URLError('error')

class GraphAPIError(Exception):pass
