from ..plugins import mail
import mock_smtplib
import mock_cfg

mail.smtplib = mock_smtplib
mail.ui_prompt = mock_smtplib.ui_prompt
mail.ConfigParser = mock_cfg
mail.__cfgfile__ = 'tests/.publish'

mail = mail.Email()

def test_verifyCredentials():
    mail.VerifyCredentials()

def test_Verifyfields():
    mail.VerifyFields({'Message':'Test Message'})

def test_Verifyfields_fail():
    mail.VerifyFields({'Message':''})

def test_SendMsg():
    Mail = {'Message':'Some Message', 'Subject':'', 'To_Email':''}
    mail.SendMsg(Mail)

def test_Authorize():
    mail.Authorize()

def test_reset():
    mail.Reset()
