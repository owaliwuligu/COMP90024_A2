import tweepy
from tweepy.streaming import StreamListener
import json as js
import time
from ConfigHarvester import HarvesterConfig
from TweetParser import TweetWrapper
from TweetTool import TweetTool
from TweetLogger import TweetLogger, TweetLocalSaver
from queue import Queue
import CouchDBApi as db

userid_mentiondict = {}
userid_thisturn = {}
userid_mentionfilt = {}
userid_mentionused = {}
userid_deepreal = {}
#
auth = tweepy.OAuthHandler(HarvesterConfig.consumer_key, HarvesterConfig.consumer_secret)
auth.set_access_token(HarvesterConfig.access_token, HarvesterConfig.access_token_secret) 
api = tweepy.API(auth)

# pre load userid_mentiondict
with open('data/user_mentionfilt.data', 'r') as fuser:
    while(True):
        userid = fuser.readline()
        if not userid: break
        userid = userid.strip()
        userid_mentionfilt[userid] = 1
with open('data/user_realtime.data', 'r') as fuser:
    while(True):
        userid = fuser.readline()
        if not userid: break
        userid = userid.strip()
        userid_deepreal[userid] = 1
with open('data/user_mentionused.data', 'r') as fuser:
    while(True):
        userid = fuser.readline()
        if not userid: break
        userid = userid.strip()
        userid_mentionused[userid] = 1
with open('data/user_mentionpending.data', 'r') as fuser:
    while(True):
        line = fuser.readline()
        if not line: break
        mentionId = line.strip().split(',')[0]
        userid_mentiondict[mentionId] = 1
        userid_thisturn[mentionId] = 1


#
log     = TweetLogger('log/spider_mentionexpanding.log',level='debug', when='D')
logerr  = TweetLogger('log/spider_mentionexpandingError.log', level='error', when='D')
log.logger.warning('Spider begin')
#
user_filt_saver   = TweetLocalSaver('data/user_mentionfilt.data', level='info', when='D')
user_used_saver   = TweetLocalSaver('data/user_mentionused.data', level='info', when='D')
user_mention_saver   = TweetLocalSaver('data/user_mentionpending.data', level='info', when='D')

#sniffer_filename = 'data/w/sniffer.data.2021-05-02_23'


#
def limit_handled(cursor):
    while True:
        try:
            #time.sleep(0.1)
            yield cursor.next()
        except tweepy.RateLimitError:
            print('limit_handled: Oh!! rate limit error!.')
            logerr.logger.error('limit_handled: Oh!! rate limit error!.')
            time.sleep(15 * 60)
        except StopIteration:
            print('limit_handled: Stop iteration!')
            logerr.logger.error('limit_handled: Stop iteration!')
            break
        except Exception as e:
            print('Unknow error.', e)
            logerr.logger.error('Error code: {0}'.format(e))
            time.sleep(1)
            break

def spiderTweetByUserId(uid, num=10):
    index = 0
    print('start mention expand', uid)
    for tweet in limit_handled( tweepy.Cursor(api.user_timeline, user_id=uid).items() ):
        try:
            if not TweetTool.IsRetweet(tweet._json):
                rawData = TweetWrapper.shortenRawJson(tweet._json)
                tweetJson = tweet._json
                #print(index,'-----')
                # mention expand
                if TweetTool.IsValidJsonKey(tweetJson, 'entities') and TweetTool.IsValidJsonKey(tweetJson['entities'], 'user_mentions'):
                    for m in range(len(tweetJson['entities']['user_mentions'])):
                        mentionId = tweetJson['entities']['user_mentions'][m]['id']
                        mentionId = str(mentionId)
                        if not mentionId in userid_mentiondict:
                            userid_mentiondict[mentionId] = 1
                            # save
                            user_mention_saver.logger.info(mentionId+','+uid)
                # db save
                db.upload_doc('tweet_data', rawData)
                
                index += 1
                if index >= num:
                    log.logger.debug('Finish mention expand '+str(uid)+' num '+str(num))
                    break
        except Exception as e:
            print('spiderTweetByUserId error', e)
            logerr.logger.error('spiderTweetByUserId error {0}'.format(e))

def checkMelbourne(uid, num=1):
    index = 0
    ifHasMel = False
    for tweet in limit_handled( tweepy.Cursor(api.user_timeline, user_id=uid).items(1) ):
        try:
            if not TweetTool.IsRetweet(tweet._json):
                rawData = TweetWrapper.shortenRawJson(tweet._json)
                tweetJson = tweet._json
                checkText = ''
                checkText += tweetJson['user']['location']
                if TweetTool.IsValidJsonKey(tweetJson, 'place'):
                    checkText += tweetJson['place']['full_name']
                    checkText += tweetJson['place']['name']
                checkText = checkText.lower()
                if checkText.find('victoria') >= 0 or \
                    checkText.find('australia') >= 0 or \
                    checkText.find('melbourne') >= 0:
                    ifHasMel = True
                    return True
                index += 1
                if index >= num:
                    break
        except Exception as e:
            print('spiderTweetByUserId error', e)
            logerr.logger.error('spiderTweetByUserId error {0}'.format(e))
    return ifHasMel


for userId in userid_thisturn:
    if userId in userid_deepreal: continue
    if userId in userid_mentionfilt: continue
    if userId in userid_mentionused: continue
    
    ifMel = checkMelbourne(userId, 1)
    if ifMel == False:
        print('mention flite', userId)
        userid_mentionfilt[userId] = 1
        user_filt_saver.logger.info(userId)
        continue
    spiderTweetByUserId(userId, 100)
    userid_deepreal[userId] = 1
    user_used_saver.logger.info(userId)
