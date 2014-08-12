import ConfigParser

from channel import Channel
from binascii import hexlify, unhexlify

class Twitter(Channel):
    "Implements Twitter Api"
    def __init__(self, Message):
        self.Message = Message       

    def GetKeys(self):
        cfg = ConfigParser.RawConfigParser()
        cfg.read('.publish')
        CON_KEY = unhexlify(cfg.get('Twitter', 'Consumer_Key'))
        CON_SEC = unhexlify(cfg.get('Twitter', 'Consumer_Secret'))
        TOKEN = unhexlify(cfg.get('Twitter', 'Token_Key'))
        TOKEN_SEC = unhexlify(cfg.get('Twitter', 'Token_Secret'))
        return CON_KEY, CON_SEC, TOKEN, TOKEN_SEC
