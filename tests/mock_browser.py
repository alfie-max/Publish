class Browser(object):
    def __init__(self):
        form = {}

    def open(self, url):
        pass

    def set_handle_robots(self, status):
        pass

    def forms(self):
        forms = [{'session[username_or_email]':'', 'session[password]':''}]
        return forms

    def close(self):
        pass

    class submit(object):
        def __init__(self):
            pass

        def get_data(self):
            return '<code>0123456</code>'
