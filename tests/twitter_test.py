from ..plugins import twitter
from mock_browser import Browser
import mock_tweepy
import mock_cfg

twitter.ConfigParser = mock_cfg
twitter.tweepy = mock_tweepy
twitter.Browser = Browser
twitter.ui_prompt = mock_tweepy.ui_prompt
twitter.__cfgfile__ = 'tests/.publish'

T = twitter.Twitter()

def test_get_auth_info():
    T.GetAuthInfo()

def test_VerifyCredentials():
    T.VerifyCredentials()

def test_Authorize():
    T.Authorize()

def test_verifyFields():
    T.VerifyFields({'Message':'Test Message'})

def test_verifyFields_failed():
    T.VerifyFields({'Message':''})

def test_SendMsg():
    T.SendMsg({'Message':'Test Message'})

def test_SendMsg_as_img():
    T.SendMsg({'Message':"""This is a long message to test sending as image.
    Make this long and long and long..... yes its really long"""})

def test_reset():
    T.Reset()
