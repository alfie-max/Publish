import ConfigParser
import smtplib

from getpass import getpass
from channel import Channel
from termcolor import colored
from binascii import hexlify, unhexlify
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class Email(Channel):
    ''' Implements an Email Api '''
    def SetupServer(self):
        """ Setup the mail server """
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
            self.server.ehlo()
            self.server.starttls()
            return True
        except:
            return False

    def GetAuthInfo(self):
        """ Read user login info from file """
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
                
    def VerifyCredentials(self):
        """ Tries to login with available login info """
        self.SetupServer()
        self.GetAuthInfo()
        try:
            self.server.login(self.username, self.password)
            return True
        except:
            return False

    def ComposeMail(self, Subject, toAddr, Message):
        """  Compose an email message"""
        mail = MIMEMultipart()
        mail['From'] = self.username
        mail['To'] = toAddr
        mail['Subject'] = Subject
        mail.attach(MIMEText(Message, 'plain'))
        return mail.as_string()

    def Authorize(self):
        """ Get user mail authentication data """
        print "Please Authenticate your Email Account"
        self.username = raw_input("Email Id : ")
        self.password = getpass("Password : ")
        
        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        if not cfg.has_section('Email'):
            cfg.add_section('Email')
        cfg.set('Email', 'Email Id', self.username)
        cfg.set('Email', 'Password', hexlify(self.password))
        with open('.publish', 'wb') as configfile:
            cfg.write(configfile)

        if self.VerifyCredentials():
            return colored('Authentication Successful', 'green')
        else:
            return colored('Authentication Failed', 'red')



    def SendMsg(self, Subject, To_Email, Message):
        """ Send mail to given addresses """
        toAddrs = To_Email.split(',')

        if self.SetupServer():
            if self.VerifyCredentials():
                fromAddr = self.username
                reply = {}
                for toAddr in toAddrs:
                    toAddr = toAddr.strip()
                    mail = self.ComposeMail(Subject, toAddr, Message)
                    try:
                        self.server.sendmail(fromAddr, toAddr, Message)
                        reply[toAddr] = 'Success'
                    except:
                        reply[toAddr] = 'Failed'
                return reply
            else:
                return colored('Authentication failed', 'red')
        else:
            return colored('Unable to access mail server', 'red')
