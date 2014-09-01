
#you will need to import these
from modules.channel import Channel
from exception import *
 

 
class Facebook(Channel):
        ''' Implements Facebook Api '''
        def __init__(self):
                self.__fields__ = ["Message"]   # and whatever the plugin requires for sending a message
 
        def VerifyCredentials(self):
                # this method should check if the auth info available in the .publish file valid
                # and return True if it checks out and false if it fails
 
        def GetKeys(self):
                # You can look at this function from any other plugin, u'll just need to make a few changes
                # which are channel specific
 
        def Authorize(self):
                # here ask user for authentication info and save it in the .publish file
                # how to do that can be seen if u look at any existing plugins
                # Finally after saving the auth info
                # call VerifyCredentials and check if the given info is worth it
                # if it fails do :
                # raise AuthorizationError({'Wordpress':'Authorization Failed'})
                # i.e raise the AuthorizationError exception and pass a dict with channel name as key
                # and value as the message to be returned to ui
       
        def VerifyFields(self, fields):
                # fields parameter passed is a dictionary of the format :
                # {field1:value, field2:value, ...}
                # here the plugin required fields are checked if they are valid
                # returns True/False
                # for eg: checks if the message passed is empty or not
 
        def SendMsg(self, Message):
                # Message: this is a dictionary in the format
                # {field1:value, field2:value, ...}
                # and here do what is necessary to send message to this channel
                # finally return message like
                # return {'Wordpress':'Blog posted'}
                # return {'Wordpress':'Blog posting failed'}
                # return {'Wordpress':'Unable to access network/server'}
                # u get the idea right.... should return a dict
                # with key as the channel name and value as the message to be returned
 
        # add whichever other methods you want to create
 
# and after declaring the class
__plugin__ = Facebook  # the channel name
__cname__ = "facebook"      #or whichever channel