from ..plugins import blog
import mock_xmlrpclib
blog.xmlrpclib = mock_xmlrpclib
blog.ui_prompt = mock_xmlrpclib.ui_prompt
blog.ui_print = mock_xmlrpclib.ui_print

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
