import os
import tweepy
import binascii
import config

global CON_KEY, CON_SEC, TOKEN, TOKEN_SEC

def Get_Keys(keys_f):
    """

    Get the Consumer keys and Token keys from the file

    """
    keysFile = open(keys_f, "r")
    
    try:
        keys = keysFile.read().split("\n")
        for i,key in enumerate(keys) :
            keys[i] = binascii.unhexlify(key[3:])
        return keys[:4]
    finally:
        keysFile.close()


def Get_Token_Keys(keys_f, CON_KEY, CON_KEY_SEC):
    """

    Get the Token keys using Consumer keys

    """
    auth = tweepy.OAuthHandler(CON_KEY,CON_KEY_SEC)
    authUrl = auth.get_authorization_url()

    print "Please Authorize : " + authUrl
    pin = raw_input("Enter the pin to verify : ")

    auth.get_access_token(pin)
    global TOKEN
    global TOKEN_SEC
    TOKEN = binascii.hexlify(auth.access_token.key)
    TOKEN_SEC = binascii.hexlify(auth.access_token.secret)

    keysFile = open(keys_f, "r")
    try:
        keys = keys_file.read().split("\n")
        keys[2] = "tk=" + TOKEN
        keys[3] = "ts=" + TOKEN_SEC
        newKeys = "\n".join(keys)

        try:
            newKeysfile = open(keys_f, "w")
            newKeysFile.write(newKeys)
        finally:
            newKeysFile.close()
    finally:
        keysFile.close()


def Twitter_Api(CON_KEY, CON_SEC, TOKEN, TOKEN_SEC):
    '''

    Create a Twitter api to access user Twitter account

    '''
    auth = tweepy.OAuthHandler(CON_KEY, CON_SEC)
    auth.set_access_token(TOKEN, TOKEN_SEC)
    return tweepy.API(auth)

def Tweet(Message):
    '''

    Main Function

    '''
    keys_f = os.environ.get(
            'HOME',
            os.environ.get(
                'USERPROFILE',
                '')) + os.sep + '.twitter_oauth'
    
    if not os.path.isfile(keys_f):
        config.Create_Key_File()

    CON_KEY, CON_SEC, TOKEN, TOKEN_SEC = Get_Keys(keys_f)        

    if len(TOKEN) == 0 or len(TOKEN_SEC) == 0 :
        print "Token keys missing"
        Get_Token_Keys(keys_f, CON_KEY, CON_SEC)

    API = Twitter_Api(CON_KEY, CON_SEC, TOKEN, TOKEN_SEC)
    API.update_status(Message)
