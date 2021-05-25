import CouchDBApi as db
import json

user_filename = 'data/cur_userid.data'
index = 0
zeroCount = 0
outfile = open('data/tweets_cur.data', 'w')
with open(user_filename, 'r', encoding='utf-8') as f:
    while(True):
        line = f.readline()
        if not line: break
        userId = line.strip()
        index += 1
        tweets = db.get_tweet_by_user('tweet_data', userId)
        if tweets['all_records'] != None:
            for t in tweets['all_records']:
                tweet = t['value']
                rawJson = json.dumps(tweet)
                outfile.write(rawJson)
                outfile.write('\n')
        if tweets['tweet_number'] == 0: zeroCount += 1
        print('load data', index, userId, 'num ', tweets['tweet_number'])
        #if index >= 1: break
print('zero count', zeroCount)
outfile.close()