from ..plugins import mail
import mock_smtplib
mail.smtplib = mock_smtplib
mail.getpass = mock_smtplib.getpass
mail.raw_input = mock_smtplib.raw_input

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
