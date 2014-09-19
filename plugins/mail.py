import smtplib
import ConfigParser

from termcolor import colored
from socket import gaierror, error
from modules.exception import *
from modules.channel import Channel
from modules.ui import ui_print, ui_prompt
from binascii import hexlify, unhexlify
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class Email(Channel):
    ''' Implements an Email Api '''
    def __init__(self):
        ''' Email class Constructor '''
        self.__fields__ = ['Subject', 'To_Email', 'Message']

    def SetupServer(self):
        '''
        Setups gmail server for sending mail.
        '''
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
        except (smtplib.SMTPException, gaierror, error):
            raise NetworkError('Unable to access network')

        try:
            self.server.ehlo()
            self.server.starttls()
            return True
        except (smtplib.SMTPException):
            return False

    def GetAuthInfo(self):
        '''
        Reads authentication data required from config file
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)

        if cfg.has_section('Email'):
            self.username = cfg.get('Email', 'Email Id')
            self.password = unhexlify(cfg.get('Email', 'Password'))
        else:
            self.username = self.password = ''

    def Reset(self):
        '''
        Resets auth data in config file
        '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        
        if not cfg.has_section('Email'):
            cfg.add_section('Email')
        cfg.set('Email', 'Email Id', '')
        cfg.set('Email', 'Password', '')
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)
                        
    def VerifyCredentials(self):
        '''
        Verifies Users Credentials stored in the config file.
        Returns True/False
        '''
        self.SetupServer()
        self.GetAuthInfo()
        try:
            self.server.login(self.username, self.password)
            return True
        except smtplib.SMTPException:
            return False

    def ComposeMail(self, Subject, toAddr, Message):
        '''
        Composes mail object using passed parameters and returns it
        '''
        mail = MIMEMultipart()
        mail['From'] = self.username
        mail['To'] = toAddr
        mail['Subject'] = Subject
        mail.attach(MIMEText(Message, 'plain'))
        return mail.as_string()

    def Authorize(self):
        '''
        Authorize the application with Gmail.
        '''
        ui_print (colored('Authorizing Email Account...', 'yellow'))
        self.username = ui_prompt("Username : ")
        self.password = ui_prompt("Password : ", mask = True)

        
        ''' Update Config file with User login Info '''
        cfg = ConfigParser.RawConfigParser()
        cfg.read(__cfgfile__)
        if not cfg.has_section('Email'):
            cfg.add_section('Email')
        cfg.set('Email', 'Email Id', self.username)
        cfg.set('Email', 'Password', hexlify(self.password))
        with open(__cfgfile__, 'wb') as configfile:
            cfg.write(configfile)

        if not self.VerifyCredentials():
            raise AuthorizationError('Authorization Failed')

    def VerifyFields(self, Mail):
        '''
        Verifies passed fields to follow requirements of Gmail
        '''
        To_Email = Mail['To_Email']
        if len(To_Email) !=0:
            status = True
        else:
            return False

        Message = Mail['Message']
        Message = Message.strip()
        if len(Message) != 0:
            status = True
        else:
            return False

        return status

    def SendMsg(self, Mail):
        '''
        Sent Message to Email.
        '''
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
                ui_print (colored('Login Failed', 'red'))
                return 1
            fromAddr = self.username
            for toAddr in To_Email:
                toAddr = toAddr.strip()
                ui_print(colored('Sending mail to {}...'.format(toAddr), 'blue'))
                mail = self.ComposeMail(Subject, toAddr, Message)
                try:
                    self.server.sendmail(fromAddr, toAddr, mail)
                    ui_print (colored('Successfully Sent', 'green'))
                except smtplib.SMTPException:
                    ui_print (colored('Sending Failed', 'red'))
        else:
            raise NetworkError('Unable to access Mail Server')


__plugin__ = Email
__cname__ = 'email'
__cfgfile__ = '.publish'
