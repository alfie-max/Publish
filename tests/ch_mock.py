class Twitter():
    def SendMsg(self, Message):
        print Message
        return "Hurray.... Dispatcher works"

class Email():
    def SendMsg(self, Subject, To_Email, Message):
        print Subject
        print Message
        print To_Email
