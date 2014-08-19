from os import unlink
from configobj import ConfigObj
from tests.ch_mock import Twitter

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
