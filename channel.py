class Channel(object):
    "Implements a basic Channel"
    def SendMsg(self, Message):
        raise NotImplementedError()

    def Authorize(self):
        raise NotImplementedError()
