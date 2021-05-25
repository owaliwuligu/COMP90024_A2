import tweepy
from tweepy.streaming import StreamListener
import json
import time
from ConfigHarvester import HarvesterConfig
from TweetParser import TweetWrapper
from TweetTool import TweetTool
from TweetLogger import TweetLogger, TweetLocalSaver
from queue import Queue
import CouchDBApi as db

#
auth = tweepy.OAuthHandler(HarvesterConfig.consumer_key, HarvesterConfig.consumer_secret)
auth.set_access_token(HarvesterConfig.access_token, HarvesterConfig.access_token_secret) 
#api = tweepy.API(auth, proxy = HarvesterConfig.twitter_api_proxy)
api = tweepy.API(auth)

#
#
log     = TweetLogger('log/spider.log',level='debug', when='D')
logerr  = TweetLogger('log/spiderError.log', level='error', when='D')
log.logger.warning('Spider begin')
#
saver   = TweetLocalSaver('data_dir/spider.data')

#
def limit_handled(cursor):
    while True:
        try:
            time.sleep(0.1)
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
    for tweet in limit_handled( tweepy.Cursor(api.user_timeline, user_id=uid).items() ):
        try:
            if not TweetTool.IsRetweet(tweet._json):
                rawJson = TweetWrapper.shortenRawJson(tweet._json)
                #print(rawJson)
                #print(index,'-----')
                index += 1
                saver.logger.info(rawJson)
                if index >= num:
                    print('finish spider', uid, ' num ', num)
                    break
        except Exception as e:
            print('spiderTweetByUserId error', e)
            logerr.logger.error('spiderTweetByUserId error {0}'.format(e))

def spiderTweetByUserName(uName, num=10):
    index = 0
    for tweet in limit_handled( tweepy.Cursor(api.user_timeline,  screen_name=uName).items() ):
        try:
            if not TweetTool.IsRetweet(tweet._json):
                rawJson = TweetWrapper.shortenRawJson(tweet._json)
                #print(rawJson)
                #print(index,'-----')
                index += 1
                db.upload_doc('tweet_data', rawJson)
                #saver.logger.info(rawJson)
                if index >= num:
                    print('finish spider', uName, ' num ', num)
                    break
        except Exception as e:
            print('spiderTweetByUserId error', e)
            logerr.logger.error('spiderTweetByUserId error {0}'.format(e))

def spiderFriendsByUserId(uid, num=10):
    index = 0
    userIds = []
    for user in limit_handled( tweepy.Cursor(api.friends, user_id=uid).items() ):
        try:
            userJson = user._json
            #print(userJson['name'])
            #print(index,'-----')
            userIds.append(userJson['id'])
            index += 1
            if index >= num:
                print('get user list by', uid, 'num ', num)
                return userIds
        except Exception as e:
            print('spiderFriendsByUserId error', e)
            logerr.logger.error('spiderFriendsByUserId error {0}'.format(e))


def searchTweetsByGeo(query, geo, num=10):
    index = 0
    for user in limit_handled( tweepy.Cursor(api.search, q=query, geocode=geo, count=num).items(num) ):
        try:
            rawJson = user._json
            print(rawJson)
            print(index,'-----')
            
            index += 1
            if index >= num:
                print('search query end: ', query, 'num ', num)
        except Exception as e:
            print('searchTweet error', e)
            logerr.logger.error('searchTweet error {0}'.format(e))

#searchTweetsByGeo("app", "5.29126,52.132633,15km", 10)
#spiderTweetByUserName('_biancalynn_', 2)
