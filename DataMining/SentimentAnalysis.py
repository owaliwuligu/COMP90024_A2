import dask.dataframe as dd
import re
import CouchDBApi as db
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer
import time
import numpy as np
import pandas as pd
from textblob import TextBlob


startTime = time.time()
trainFileName = 'tmp/train_labeled.csv'

data_train      = dd.read_csv(trainFileName)
label_train_raw     = list(data_train['food'])
user_train          = list(data_train['user'])
tweets_train        = list(data_train['tweet'])

food_category_filename = 'features/generic-food.csv' 
data_train          = dd.read_csv(food_category_filename)
foodname_list       = list(data_train['FOOD NAME'])
foodgroup_list      = list(data_train['GROUP'])
foodsubgroup_list   = list(data_train['SUB GROUP'])

FoodGroup = {}
FoodGroupLow = {}
FoodNameDict = {}
# build food category tree
index = 0
for group in foodgroup_list:
    FoodGroup[group] = {}
    FoodGroup[group]['index'] = index
    index += 1
    FoodGroupLow[group] = {}
for i in range(0, len(foodgroup_list)):
    group = foodgroup_list[i]
    subgroup = foodsubgroup_list[i]
    FoodGroup[group][subgroup] = {}
for i in range(0, len(foodname_list)):
    group = foodgroup_list[i]
    subgroup = foodsubgroup_list[i]
    foodname = foodname_list[i]
    FoodGroup[group][subgroup][foodname] = 0
    FoodGroupLow[group][foodname] = 0
    FoodNameDict[foodname] = 0

def ConvertRawYToLabel(rawLabel, yList):
    for index, l in enumerate(rawLabel):
        for food in FoodGroup:
            if l == food:
                yList[index] = food['index']

def ConvertRawCountX(rawCountVec, xList):
    for index, line in enumerate(rawCountVec):
        for tupeStr in line.strip('[] ').split('),'):
            t = tuple(map( float, tupeStr.strip('() ').split(',') ))
            xList[index][int(t[0])] = t[1]

##
label_train = np.zeros(len(label_train_raw), np.int)
ConvertRawYToLabel(label_train_raw, label_train)

def sentimentScore(text):
    blob = TextBlob(text)
    sCount = 0
    polarityScore = 0
    subjetivityScore = 0
    for sentence in blob:
        sCount += 1
        polarityScore += sentence.sentiment['polarity']
        subjetivityScore += sentence.sentiment['subjectivity']
    return (polarityScore/sCount, subjetivityScore/sCount)



def MergeUserData(labelIn, userIn, tweetsIn):
    data_len = len(userIn)
    tweets_merge_dict = {}
    laber_merge_dict = {}
    for i in range(0, data_len):
        userId = userIn[i]
        if userId in tweets_merge_dict:
            tweets_merge_dict[userId] += ' '+tweetsIn[i]
        else:
            tweets_merge_dict[userId] = tweetsIn[i]
        #
        laber_merge_dict[userId] = labelIn[i]
    labelMerge = []
    userMerge = []
    tweetsMerge = []
    for userId in laber_merge_dict:
        userMerge.append(userId)
        labelMerge.append(laber_merge_dict[userId])
        tweetsMerge.append(tweets_merge_dict[userId])
    return labelMerge, userMerge, tweetsMerge

label_train_merge, user_train_merge, tweets_train_merge = MergeUserData(label_train, user_train, tweets_train)

t_label = label_train_merge
t_user = user_train_merge
t_tweets = tweets_train_merge   # tweets_train_merge  tweets_train
######

len_train = len(t_label)
##################################
ratioThresh1 = 3
min_dff = 1
for ratioThresh in range(3, 20):
    print('---------search filt df', min_dff)
    vectorizer = CountVectorizer(min_df=min_dff, stop_words='english', token_pattern=r'[^\s]+') #token_pattern=r'[^\s]+'
    X = vectorizer.fit_transform(t_tweets) 
    feature_name = vectorizer.get_feature_names()
    feature_dict = vectorizer.vocabulary_
    feature_len = len(feature_name)
    print('len', feature_len)
    #
    term_level = np.zeros([4, feature_len], np.int)
    term_levelByUser = np.zeros([4, feature_len], np.int)
    term_userCount = np.zeros(feature_len, np.int)

    score1 = np.zeros(len_train, np.float)
    for i in range(0, len_train):
        text = tweets_train[i]
        s1,s2 = sentimentScore(text)
        score1[i] = s1

    for i in range(0, len_train):
        term_row = X.getrow(i).toarray()[0]
        if score1[i] < 0.5: continue
        for indexTerm, countTerm in enumerate(term_row):
            if countTerm > 0:
                label = t_label[i]
                term_level[label][indexTerm] += countTerm
                term_levelByUser[label][indexTerm] += 1
                term_userCount[indexTerm] += 1
    term_level_ratio = np.zeros(feature_len, np.float)
    for termIndex in range(0, feature_len):
        classCount = []
        for i in range(0,4): classCount.append(term_levelByUser[i][termIndex])
        maxCount = max(classCount)
        sumCount = sum(classCount)
        maxIndex = classCount.index(maxCount)
        isLcalSensitive = True
        minRatio = 999.0
        for i in range(0,4):
            if i == maxIndex or classCount[i] == 0: continue
            ratio = maxCount / classCount[i]
            if ratio < minRatio:
                minRatio = ratio
        term_level_ratio[termIndex] = round(minRatio,2)

    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    feature_count = X.sum(axis=0).A1
    
    print('ratio thresh', ratioThresh)
    del_flag = np.zeros(feature_len, np.int)
    for termIndex in range(0, feature_len):
        termCount = feature_count[termIndex]
        termLocalRatio = term_level_ratio[termIndex]
        # del small df term
        if termLocalRatio >= ratioThresh: del_flag[termIndex] = 1
    real_feature_count = 0
    for termIndex in range(0, feature_len):
        if del_flag[termIndex] == 1: real_feature_count += 1
    print('real feature count', real_feature_count)
    
    x_train = [[] for i in range(0,len_train)]
    for i in range(0,len_train): x_train[i] = [0.0 for j in range(0, real_feature_count)]
    allZeroCount_train = 0
    allZeroCount_test = 0
    y_train = label_train_merge.copy()
    train_data_del_flag = np.zeros(len_train, np.int)
    for i in range(0, len_train):
        term_row = X.getrow(i).toarray()[0]
        realTermIndex = 0
        isAllZero = True
        for indexTerm, countTerm in enumerate(term_row):
            if del_flag[indexTerm] == 0: continue
            x_train[i][realTermIndex] = countTerm
            if countTerm > 0: isAllZero = False
            realTermIndex += 1
        if isAllZero == True:
            allZeroCount_train += 1
            train_data_del_flag[i] = 1


feature_count_tuple = list(zip(feature_name, feature_count, term_userCount, term_level_ratio))
feature_count_tuple.sort(key=lambda x:(-x[2],-x[3]))
#feature_count_tuple.sort(key=lambda x:(-x[3],-x[2]))

# write feature
fkey,fvalue,fuserCount, fquality, \
ftermLocation0,ftermLocation1,ftermLocation2,ftermLocation3 = zip(*feature_count_tuple)
dataCsv = pd.DataFrame({'name':fkey,'value':fvalue})
dataCsv.to_csv("features/food-sentiment-term.csv", index=False, sep=',')
#print(tfidf)

print('end')