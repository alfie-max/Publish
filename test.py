from twitter import Twitter

Message = "Hello World"
tweet = Twitter(Message)
k = tweet.GetKeys()
print k
