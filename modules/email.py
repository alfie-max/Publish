import ConfigParser
import smtplib

from channel import Channel
from binascii import hexlify, unhexlify

class Email(Channel):
    ''' Implements an Email Api '''
    def SetupServer(self):
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
            self.server.starttls()
            return True
        except:
            return False

    def GetAuthInfo(self):
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')

        if cfg.has_section('Email'):
            self.username = cfg.get('Email', 'Email Id')
            self.password = unhexlify(cfg.get('Email', 'Password'))
        else:
            cfg.add_section('Email')
            cfg.set('Email', 'Email Id', '')
            cfg.set('Email', 'Password', '')
            with open('.publish', 'wb') as configfile:
                cfg.write(configfile)

    def Authorize(self):
        self.GetAuthInfo()
        try:
            self.server.login(self.username, self.password)
            return True
        except:
            print "Please Authenticate your Email Account"
            self.username = raw_input("Email Id : ")
            self.password = raw_input("Password : ")
            try:
                self.server.login(self.username, self.password)
            except:
                return False

        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        cfg.set('Email', 'Email Id', self.username)
        cfg.set('Email', 'Password', hexlify(self.password))
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)

        return True


    def SendMsg(self, Message):
        toAddrs = Message['To']
        msg = Message['Body']

        if self.SetupServer():
            if self.Authorize():
                try:
                    fromAddr = self.username
                    self.server.sendmail(fromAddr, toAddrs, msg)
                    response = True
                except:
                    response = False
                finally:
                    try:
                        self.server.quit()
                    except:
                        pass
                return response
                
        return False
