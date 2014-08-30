from ..plugins.twitter import Twitter

T = Twitter()

def test_get_auth_info():
    T.GetAuthInfo()
