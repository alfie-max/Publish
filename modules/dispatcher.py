from os import unlink
from configobj import ConfigObj
from twitter import Twitter

def Dispatch(channels, msgFile):
    msgConfig = ConfigObj(msgFile)
    Topic = msgConfig['Topic']
    To_Email = msgConfig['To_Email']
    Message = msgConfig['Message']
    unlink(msgFile)

    reply = {}
    for channel in channels:
        if channel == 'Twitter':
            chObj = Twitter()
            reply['Twitter'] = chObj.SendMsg(Message)
            
    return reply

def Authenticate(channel):
    if channel == 'Twitter':
        chObj = Twitter()
        reply = chObj.Authorize()
        return reply
    
