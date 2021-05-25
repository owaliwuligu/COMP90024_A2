class TweetTool:
    def IsRetweet(tweetJson):
        isRet = False
        if 'retweeted' in tweetJson and tweetJson["retweeted"] == True: isRet = True
        if 'text' in tweetJson and tweetJson['text'].startswith('RT'): isRet = True
        return isRet
    def IsValidJsonKey(json, key):
        if key in json and json[key] != None and json[key] != {} : return True
        return False