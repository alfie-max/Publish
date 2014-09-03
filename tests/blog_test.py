from ..plugins import blog
import mock_xmlrpclib
blog.xmlrpclib = mock_xmlrpclib
blog.getpass = mock_xmlrpclib.getpass
blog.raw_input = mock_xmlrpclib.raw_input

blog = blog.Blog()

def test_SendMsg():
    blogmsg = {'Message':'Test Message', 'Title':'Some Title'}
    blog.SendMsg(blogmsg)

def test_Verifyfields():
    blog.VerifyFields({'Message':'Test Message'})

def test_Verifyfields_fail():
    blog.VerifyFields({'Message':''})

def test_VerifyCredentials():
    blog.VerifyCredentials()

def test_Authorize():
    blog.Authorize()
