import ConfigParser
import tweepy

from channel import Channel
from binascii import hexlify, unhexlify

class Twitter(Channel):
    "Implements Twitter Api"
    def __init__(self):
        pass

    def SendMsg(self, Message):
        raise NotImplementedError()
