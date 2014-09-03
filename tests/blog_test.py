from ..plugins import blog
import mock_xmlrpclib
blog.xmlrpclib = mock_xmlrpclib
blog.getparss = mock_xmlrpclib.getpass
blog.raw_input = mock_xmlrpclib.raw_input

blog = blog.Blog()

def test_SendMsg():
    blogmsg = {'Message':'Test Message', 'Title':'Some Title'}
    

def test_Verifyfields():
    blog.VerifyFields({'Message':'Test Message'})

def test_Verifyfields_fail():
    

def test_VerifyCredentials():
    

def test_Authorize():
    blog.Authorize()
