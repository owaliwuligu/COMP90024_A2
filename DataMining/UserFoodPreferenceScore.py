import dask.dataframe as dd
import re
import CouchDBApi as db
import json
import mmap
import os
from datetime import datetime
from MiningLogger import MiningLogger, MiningSaver, minerlog
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

user_foodpreference_saver = MiningSaver('data/user_food_preference.data', level='info', when='D')

sentiment_term_dict = {}

food_sentiment_filename = 'features/food-sentiment-term.csv' 
with open(food_sentiment_filename, 'r', encoding='utf-8') as f:
    while(True):
        line = f.readline()
        if not line: break
        term = line.lower().strip('\n"')
        if term.find(' '):
            terms = term.split(' ')
            for t in terms:
                sentiment_term_dict[term] = 1
        else:
            sentiment_term_dict[term] = 1


def SentimentCheckByText(text):
    senti = 0
    text = text.lower()
    words = re.split('[ !,?.\'\"@#$%^&*()-=_+\{\}|\\:;></~`]', text)
    for w in words:
        if w in sentiment_term_dict:
            senti += 1
    return senti

userTweetCountByDate = {}
userSentiScoreByDate = {}

def SentimentCheckByTweetJson(tweet):
    text = tweet['text']
    score = SentimentCheckByText(text)
    # time line
    created_at = tweet['created_at']
    date = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')
    year = date.strftime('%Y')
    month = date.strftime('%m')
    dateString = year+'-'+month
    #
    if dateString in userTweetCountByDate:
        userTweetCountByDate[dateString] += 1
    else:
        userTweetCountByDate[dateString] = 1
    userTweetCountByDate['total'] += 1
    #
    if dateString in userSentiScoreByDate:
        userSentiScoreByDate[dateString] += score
    else:
        userSentiScoreByDate[dateString] = score
    userSentiScoreByDate['total'] += score




def SentimentCheckByUser(userId):
    global userSentiScoreByDate
    global userTweetCountByDate
    userTweetCountByDate = {}
    userSentiScoreByDate = {}
    userTweetCountByDate['total'] = 0
    userSentiScoreByDate['total'] = 0
    
    userInfo = {}
    #
    tweets = db.get_tweet_by_user('tweet_data', userId)
    if tweets['all_records'] != None:
        for t in tweets['all_records']:
            tweetJson = t['value']
            SentimentCheckByTweetJson(tweetJson)

            coor = (0,0)
            if tweetJson['coordinates'] != None:
                if 'type' in tweetJson['coordinates']:
                    if tweetJson['coordinates']['type'] == 'Point':
                        coorStr = tweetJson['coordinates']['coordinates']
                        coor = (coorStr[0], coorStr[1])
            #
            if 'coordinates' in userInfo:
                if 'coordinates' in tweetJson and tweetJson['coordinates'] != None:
                    userInfo['coordinates'] = tweetJson['coordinates']
            else:
                userInfo['coordinates'] = tweetJson['coordinates']
            if 'place' in userInfo:
                if 'place' in tweetJson and tweetJson['place'] != None:
                    userInfo['place'] = tweetJson['place']
            else:
                userInfo['place'] = tweetJson['place']
            if 'user' in userInfo:
                if 'user' in tweetJson and tweetJson['user'] != None:
                    userInfo['user'] = tweetJson['user']
                    if 'entities' in userInfo['user']:
                        del userInfo['user']['entities']
            else:
                userInfo['user'] = tweetJson['user']
            
        # ratio
        ratioDict = {}
        for date in userSentiScoreByDate:
            score = userSentiScoreByDate[date]
            num = userTweetCountByDate[date]
            ratio = float(score) / num
            ratioDict[date] = round(ratio, 4)
        userInfo['food_preference'] = ratioDict
        userInfo['tweet_count'] = userTweetCountByDate
        # place
        if 'place' in tweetJson and tweetJson['place'] != None:
            placeStr = tweetJson['place']['full_name']
            placeStr = placeStr.lower()
            places = placeStr.split(' ')
            for p in places:
                placeName = p.strip(' ,')
                
        user_foodpreference_saver.logger.info(json.dumps(userInfo))
    return userInfo


user_file_name = 'data/user_realtime.data'
dataFileSize = os.path.getsize(user_file_name)
blockSize = int(dataFileSize/comm_size)
blockSizeTiny = int(blockSize/comm_size)


resJson = {}
with open(user_file_name, 'r', encoding='utf-8') as f:
    #
    map = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
    #
    for fileSegIndex in range(comm_size):
        map.seek(fileSegIndex*blockSize + rank*blockSizeTiny)
        if rank != 0 or (rank==0 and fileSegIndex!=0): first_line = map.readline()
        
        blockEnd = fileSegIndex*blockSize + (rank + 1) * blockSizeTiny
        index = map.tell()
        # read block file
        while index <= blockEnd and index < dataFileSize:
            line_b = map.readline()
            line = line_b.decode('utf-8')
            userId = line.strip()
            index += len(line_b)

            #
            userInfo = SentimentCheckByUser(userId)
            resJson[userId] = userInfo

            print('user:', userId, ' prefercence cal over.')


outFileName = 'data/user_food_preference'+str(rank)+'.json'
with open(outFileName, 'w') as f:
    json.dump(resJson, f)


print('end')