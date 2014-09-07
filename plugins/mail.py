import ConfigParser
import smtplib

from socket import gaierror
from getpass import getpass
from modules.ui import ui_print
from modules.exception import *
from modules.channel import Channel
from binascii import hexlify, unhexlify
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class Email(Channel):
    ''' Implements an Email Api '''
    def __init__(self):
        self.__fields__ = ['Subject', 'To_Email', 'Message']

    def SetupServer(self):
        """ Setup the mail server """
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
        except (smtplib.SMTPException, gaierror):
            raise NetworkError('Unable to access network')

        try:
            self.server.ehlo()
            self.server.starttls()
            return True
        except (smtplib.SMTPException):
            return False

    def GetAuthInfo(self):
        """ Read user login info from file """
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')

        if cfg.has_section('Email'):
            self.username = cfg.get('Email', 'Email Id')
            self.password = unhexlify(cfg.get('Email', 'Password'))
        else:
            self.username = self.password = ''
                
    def VerifyCredentials(self):
        """ Tries to login with available login info """
        self.SetupServer()
        self.GetAuthInfo()
        try:
            self.server.login(self.username, self.password)
            return True
        except smtplib.SMTPException:
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
        ui_print ('Authorizing Email Account...')
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

        if not self.VerifyCredentials():
            raise AuthorizationError('Authorization Failed')

    def VerifyFields(self, Mail):
        Message = Mail['Message']
        Message = Message.strip()
        if len(Message) != 0:
            return True
        else:
            return False

    def SendMsg(self, Mail):
        """ Send mail to given addresses """
        Subject = Mail['Subject']
        To_Email = Mail['To_Email']
        if isinstance(To_Email,str):
            To_Email = To_Email.split(',')
        Message = Mail['Message']
        Message = Message.strip()
        
        if self.SetupServer():
            self.GetAuthInfo()
            try:
                self.server.login(self.username, self.password)
            except smtplib.SMTPException:
                ui_print ('Login Failed')
                return 1
            fromAddr = self.username
            for toAddr in To_Email:
                toAddr = toAddr.strip()
                ui_print('Sending mail to {}...'.format(toAddr))
                mail = self.ComposeMail(Subject, toAddr, Message)
                try:
                    self.server.sendmail(fromAddr, toAddr, mail)
                    ui_print ('Successfully Sent')
                except:
                    ui_print ('Sending Failed')
        else:
            raise NetworkError('Unable to access Mail Server')


__plugin__ = Email
__cname__ = 'email'
