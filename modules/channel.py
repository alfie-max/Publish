class Channel(object):
    "Implements a basic Channel"
    def __init__(self):
        ''' Initializes the channel object and 
        should have __fields__ variable with list of the fields
        channel requires for sending message
        eg:- __fields__ = ['Message','Topic']'''
        raise NotImplementedError()

    def GetAuthInfo(self):
        ''' Read auth info from .publish file '''
        raise NotImplementedError()

    def VerifyCredentials(self):        
        ''' Verify stored auth info and return True/False '''
        raise NotImplementedError()

    def Authorize(self):
        ''' Ask user for auth info and authorize the user 
        and finally check if given info is valid using VerifyCredentials
        if not raise exception AuthorizationError(__cname__)
        where __cname__ is the channel name variable every channel has'''
        raise NotImplementedError()

    def SendMsg(self, Message):
        ''' Sends the message to the channel '''
        raise NotImplementedError()
