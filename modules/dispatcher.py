from os import unlink
from configobj import ConfigObj
from twitter import Twitter

def Dispatch(channels, msgFile):
    msgConfig = ConfigObj(msgFile)
    Message = msgConfig['Message']

    reply = {}
    for channel in channels:
        if channel == 'Twitter':
            chObj = Twitter()
            reply['Twitter'] = chObj.SendMsg(Message)

    unlink(msgFile)            
    return reply

def Authenticate(channel):
    if channel == 'Twitter':
        chObj = Twitter()
        reply = chObj.Authorize()
        return reply
    
