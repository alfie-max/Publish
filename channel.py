class Channel(object):
    "Implements a basic Channel"
    def SendMsg(self):
        raise NotImplementedError()

    def Authorize(self):
        raise NotImplementedError()
