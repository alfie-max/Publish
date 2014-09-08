class SMTP(object):
    def __init__(self, server):
        pass
        
    def ehlo(self):
        pass

    def starttls(self):
        pass

    def login(self, username, password):
        pass
    
    def sendmail(self, fromaddr, toaddr, mail):
        pass

class SMTPException(Exception):pass

def ui_prompt(msg, mask=None):
    return ''
