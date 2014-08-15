from twitter import Twitter

def broadcast(Message):
    reply = "\n  Summary\n+++++++++++\n"
    for channel in Message.keys():
        if channel == 'Twitter':
            tweet = Twitter()
            if tweet.SendMsg(Message[channel]):
                reply += "Message posted on Twitter\n"
            else:
                reply += "Message sending failed on Twitter\n"
        elif channel == 'Facebook':
            if True:
                reply += "Message posted on Facebook\n"
            else:
                reply += "Message sending failed on Facebook\n"
                
    return reply[:-1]
