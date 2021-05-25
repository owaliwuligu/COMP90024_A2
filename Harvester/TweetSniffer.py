import logging
import tweepy
from tweepy.streaming import STREAM_VERSION, StreamListener
import json as js
import time
from ConfigHarvester import HarvesterConfig
from TweetParser import TweetWrapper
from TweetTool import TweetTool
from TweetLogger import TweetLogger, TweetLocalSaver
import CouchDBApi as db

#
auth = tweepy.OAuthHandler(HarvesterConfig.consumer_key, HarvesterConfig.consumer_secret)
auth.set_access_token(HarvesterConfig.access_token, HarvesterConfig.access_token_secret) 
api = tweepy.API(auth, proxy = HarvesterConfig.twitter_api_proxy)

#
log     = TweetLogger('log/sniffer.log', level='debug', when='D')
logerr  = TweetLogger('log/snifferError.log', level='error', when='D')
log.logger.warning('Sniffer begin')
#
saver   = TweetLocalSaver('data/sniffer.data', level='info', when='D')

#
class TweetListener(StreamListener):
    _index = 1
    def on_data(self, data):
        tweetJson = js.loads(data, encoding= 'utf-8')
        # retweets filter
        if not TweetTool.IsRetweet(tweetJson):
            #file.write(data)
            #dealStream(tweetJson, file)
            #
            rawJson = TweetWrapper.shortenRawJson(tweetJson)
            #
            saver.logger.info(rawJson)
            #
            db.upload_doc('tweet_data_realtime', rawJson)
            #
            log.logger.debug('Sniffer {0} id: {1} {2}'.format(self._index, tweetJson['id'], tweetJson['user']['id']))
            self._index += 1
        return True
    def on_error(self, statusCode):
        logerr.logger.error('Error code: {0}'.format(statusCode))

while(True):
    try:
        listener    = TweetListener()
        stream      = tweepy.Stream(auth, listener)
        stream.filter(locations = HarvesterConfig.bbox_victoria)
    except Exception as e:
        logerr.logger.error('Error code: {0}'.format(e))
        print('error', e)
        time.sleep(2)