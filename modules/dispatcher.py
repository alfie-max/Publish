from os import unlink
from configobj import ConfigObj
from twitter import Twitter
from mail import Email
from tests.ch_mock import Blog, Facebook

def Dispatch(channels, msgFile):
    msgConfig = ConfigObj(msgFile)
    Message = msgConfig['Message']

    reply = {}
    for channel in channels:
        if channel == 'Twitter':
            chObj = Twitter()
            reply['Twitter'] = chObj.SendMsg(Message)
        if channel == 'Facebook':
            chObj = Facebook()
            reply['Facebook'] = chObj.SendMsg(Message)
        if channel == 'Blog':
            blog = {}
            blog['Topic'] = msgConfig['Topic']
            blog['Message'] = msgConfig['Message']
            chObj = Blog()
            reply['Blog'] = chObj.SendMsg(blog)
        if channel == 'Email':
            mail = {}
            mail['Subject'] = msgConfig['Subject']
            mail['To_Email'] = msgConfig['To_Email']
            mail['Message'] = msgConfig['Message']
            chObj = Email()
            reply['Email'] = chObj.SendMsg(mail)

    unlink(msgFile)            
    return reply

def Authenticate(channel):
    if channel == 'Twitter':
        chObj = Twitter()
        reply = chObj.Authorize()
        return reply
    if channel == 'Email':
        chObj = Email()
        reply = chObj.Authorize()
        return reply
    
