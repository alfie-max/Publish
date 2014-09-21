import pytest
import mock_channel

C = mock_channel.Ch()

def test_GetAuthInfo():
    with pytest.raises(NotImplementedError):
        C.GetAuthInfo()

def test_Reset():
    with pytest.raises(NotImplementedError):
        C.Reset()

def test_VerifyCredentials():
    with pytest.raises(NotImplementedError):
        C.VerifyCredentials()

def test_Authorize():
    with pytest.raises(NotImplementedError):
        C.Authorize()

def test_VerifyFields():
    with pytest.raises(NotImplementedError):
        C.VerifyFields(['Test Field'])

def test_SendMsg():
    with pytest.raises(NotImplementedError):
        C.SendMsg('Test Message')
