from twitter import Twitter

Message = "Good Evening Twitter, Again and Again"
tweet = Twitter()

#print tweet.VerifyCredentials()[1]

#tweet.Authorize()
if tweet.SendMsg(Message):
    pass
else :
    print 'Tweet Failed'
