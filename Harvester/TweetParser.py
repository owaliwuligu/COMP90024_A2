from TweetTool import TweetTool
import json
from datetime import datetime
import copy

class TweetWrapper:
    del_key = [
        'in_reply_to_status_id',
        'in_reply_to_status_id_str',
        'in_reply_to_user_id',
        'in_reply_to_user_id_str',
        'in_reply_to_screen_name',
        'timestamp_ms',
        'id',
        'quoted_status'
    ]
    del_user_key = [
        'description', 'translator_type', 'protected',
        'verified', 'profile_background_image_url',
        'profile_background_image_url_https', 'profile_background_tile',
        'profile_link_color', 'profile_sidebar_border_color',
        'profile_sidebar_fill_color', 'profile_text_color',
        'profile_use_background_image', 'profile_image_url',
        'profile_image_url_https', 'profile_banner_url',
        'default_profile_image', 'contributors_enabled', 'is_translator',
        'is_translation_enabled', 'profile_background_color', 'has_extended_profile',
        'withheld_in_countries', 'follow_request_sent', 'utc_offset',
        'time_zone', 'following', 'notifications'
    ]
    del_place_key = [
        'url', 'bounding_box', 'attributes'
    ]
    del_media_key = [
        'id_str', 'media_url_https', 'url', 'display_url', 'expanded_url', 'sizes', 'indices'
    ]
    del_mention_key = [
        'screen_name', 'name', 'id_str', 'indices'
    ]
    shorten_key = [
        ('id_str', 'id'),
        ('possibly_sensitive', 'is_sensitive')
    ]
    def shortenRawJson(tweetJson):
        rawJson = {}
        try:
            for key in TweetWrapper.del_key:
                if key in tweetJson: del tweetJson[key]
            if TweetTool.IsValidJsonKey(tweetJson, 'user'):
                for key in TweetWrapper.del_user_key:
                    if key in tweetJson['user']: del tweetJson['user'][key]
            if TweetTool.IsValidJsonKey(tweetJson, 'place'):
                for key in TweetWrapper.del_place_key:
                    if key in tweetJson['place']: del tweetJson['place'][key]
            for keyPair in TweetWrapper.shorten_key:
                if keyPair[0] in tweetJson:
                    tweetJson[keyPair[1]] = tweetJson.pop(keyPair[0])
            # extended tweet
            if TweetTool.IsValidJsonKey(tweetJson, 'extended_tweet'):
                # convert full text
                if 'full_text' in tweetJson['extended_tweet']:
                    tweetJson['text'] = tweetJson['extended_tweet'].pop('full_text')
                if 'entities' in tweetJson['extended_tweet']:
                    tweetJson['entities'] = tweetJson['extended_tweet'].pop('entities')
                if 'extended_entities' in tweetJson['extended_tweet']:
                    tweetJson['extended_entities'] = tweetJson['extended_tweet'].pop('extended_entities')
                #del tweetJson['extended_tweet']
            
            # shorten media
            if TweetTool.IsValidJsonKey(tweetJson, 'entities') and TweetTool.IsValidJsonKey(tweetJson['entities'], 'media'):
                for m in range(len(tweetJson['entities']['media'])):
                    for key in TweetWrapper.del_media_key:
                        if key in tweetJson['entities']['media'][m]: del tweetJson['entities']['media'][m][key]
            if TweetTool.IsValidJsonKey(tweetJson, 'extended_entities') and TweetTool.IsValidJsonKey(tweetJson['extended_entities'], 'media'):
                for m in range(len(tweetJson['extended_entities']['media'])):
                    for key in TweetWrapper.del_media_key:
                        if key in tweetJson['extended_entities']['media'][m]: del tweetJson['extended_entities']['media'][m][key]
            # shorten user_mentions
            if TweetTool.IsValidJsonKey(tweetJson, 'entities') and TweetTool.IsValidJsonKey(tweetJson['entities'], 'user_mentions'):
                for m in range(len(tweetJson['entities']['user_mentions'])):
                    for key in TweetWrapper.del_mention_key:
                        if key in tweetJson['entities']['user_mentions'][m]: del tweetJson['entities']['user_mentions'][m][key]
            
            
            #
            #rawJson = copy.deepcopy(tweetJson)
            rawJson = json.dumps(tweetJson)
        except Exception as e:
            print('shortenRawJson error', e)
        return rawJson






'''
obj['id']           = tweetJson['id_str']
            obj['text']         = tweetJson['text']
            obj['uid']          = tweetJson['user']['id']
            obj['uname']        = tweetJson['user']['screen_name']
            obj['count']        = {}
            obj['count']['quote']       = tweetJson['quote_count']
            obj['count']['relpy']       = tweetJson['reply_count']
            obj['count']['retweet']     = tweetJson['retweet_count']
            obj['count']['fav']         = tweetJson['favorite_count']

            obj['lang'] = tweetJson['lang']
            obj['isFav'] = tweetJson['favorited']
            obj['isRe'] = tweetJson['retweeted']
            obj['isSensi'] = tweetJson['possibly_sensitive']
            
            #
            obj['created_at'] = ''
            if tweetJson['created_at']:
                createTime = tweetJson['created_at']
                obj['created_at'] = datetime.strptime(createTime,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
            #
            if tweetJson['coordinates'] and tweetJson['coordinates']['coordinates']:
                obj['coordinate'] = tweetJson['coordinates']['coordinates']
            # HashTag
            obj['hashTags'] = []
            if tweetJson['entities']['hashTags']:
                for tag in tweetJson['entities']['hashTags']:
                    obj['hashTags'].append(tag['text'])
            # extended mode
            if 'extended_tweet' in tweetJson.keys():
                obj['text'] = tweetJson['extended_tweet']['full_text']
                if tweetJson['extended_tweet']['entities'] != None and tweetJson['extended_tweet']['entities']['hashtags'] != None:
                    obj['hashTags'] = []
                    for tag in tweetJson['extended_tweet']['entities']['hashtags']:
                        obj['hashTags'].append(tag['text'])
'''