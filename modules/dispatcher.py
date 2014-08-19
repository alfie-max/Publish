from os import unlink
from configobj import ConfigObj
from twitter import Twitter
from tests.ch_mock import Email

def Dispatch(channels, msgFile):
    msgConfig = ConfigObj(msgFile)
    Message = msgConfig['Message']

    reply = {}
    for channel in channels:
        if channel == 'Twitter':
            chObj = Twitter()
            reply['Twitter'] = chObj.SendMsg(Message)
        if channel == 'Email':
            Subject = msgConfig['Topic']
            To_Email = msgConfig['To_Email']
            chObj = Email()
            reply['Email'] = chObj.SendMsg(Subject, To_Email, Message)

    unlink(msgFile)            
    return reply

def Authenticate(channel):
    if channel == 'Twitter':
        chObj = Twitter()
        reply = chObj.Authorize()
        return reply
    
