import pytest
from ..plugins import fb
import mock_facebook
import mock_webbrowser
import mock_cfg

fb.ConfigParser = mock_cfg
fb.facebook = mock_facebook
fb.webbrowser = mock_webbrowser
fb.__cfgfile__ = 'tests/.publish'

F = fb.Facebook()

def test_get_auth_info():
    F.GetAuthInfo()

def test_VerifyCredentials():
    F.VerifyCredentials()

def test_reset():
    F.Reset()

def test_verifyFields():
    F.VerifyFields({'Message':'Test Message'})

def test_verifyFields_failed():
    F.VerifyFields({'Message':''})

def test_SendMsg():
    F.SendMsg({'Message' : 'None'})

def test_SendMsg_fail():
    F.SendMsg({'Message' : 'error'})

def test_SendMsg_fail2():
    try:
        F.SendMsg({'Message' : 'neterror'})
    except Exception:
        pass

def test_Authorize():
    try:
        F.Authorize()
    except SystemExit:
        pass
