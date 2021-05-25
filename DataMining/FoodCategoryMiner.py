import dask.dataframe as dd
import re
import CouchDBApi as db
import json
from datetime import datetime
import mmap
import os
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

food_category_filename = 'features/generic-food.csv' 
data_train          = dd.read_csv(food_category_filename)
foodname_list       = list(data_train['FOOD NAME'])
foodgroup_list      = list(data_train['GROUP'])
foodsubgroup_list   = list(data_train['SUB GROUP'])

FoodGroup = {}
FoodGroupLow = {}
FoodNameDict = {}
# build food category tree
for group in foodgroup_list:
    FoodGroup[group] = {}
for i in range(0, len(foodgroup_list)):
    group = foodgroup_list[i]
    subgroup = foodsubgroup_list[i]
    FoodGroup[group][subgroup] = {}
for i in range(0, len(foodname_list)):
    group = foodgroup_list[i]
    subgroup = foodsubgroup_list[i]
    foodname = foodname_list[i]
    FoodGroup[group][subgroup][foodname] = 0
    if not subgroup in FoodGroupLow:
        FoodGroupLow[subgroup] = {}
    FoodGroupLow[subgroup][foodname] = 0
    FoodNameDict[foodname] = 0

def ApproximateCheckFoodByText(text):
    counts = []
    for i in range(0, len(foodname_list)):
        counts.append(0)
    text = text.lower()
    for i in range(0, len(foodname_list)):
        name = foodname_list[i]
        name = name.lower()
        ifPharse = name.find(' ')>=0
        count = 0
        nameshort = name
        if name[-1] == 's': nameshort = name[0:-1]
        if ifPharse == True:
            count += text.count(name)
        else:
            c = 0
            if len(name) >= 4 and text.find(name) == 0:
                continue
            words = re.split('[ !,?.\'\"@#$%^&*()-=_+\{\}|\\:;></~`]', text)
            for w in words:
                if len(w) < len(nameshort): continue
                if len(w) > len(name): continue
                if w == name or w == nameshort:
                    c += 1
            count = c
        #if count > 0: print(i, name)
        counts[i] = count
    return counts

#
tweetCountByDate = {}
#
foodWordCountByDate = {}
for name in foodname_list:
    foodWordCountByDate[name] = {}
    foodWordCountByDate[name]['total'] = 0

def CheckFoodByTweetJson(tweet):
    text = tweet['text']
    counts = ApproximateCheckFoodByText(text)
    # time line
    created_at = tweet['created_at']
    date = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')
    year = date.strftime('%Y')
    month = date.strftime('%m')
    dateString = year+'-'+month
    #
    if dateString in tweetCountByDate: tweetCountByDate[dateString] += 1
    else: tweetCountByDate[dateString] = 1
    #
    for foodIndex in range(0, len(foodname_list)):
        foodname = foodname_list[foodIndex]
        count = counts[foodIndex]
        if count == 0: continue
        if dateString in foodWordCountByDate[foodname]:
            foodWordCountByDate[foodname][dateString] += count
        else:
            foodWordCountByDate[foodname][dateString] = count
        foodWordCountByDate[foodname]['total'] += count
        

def CheckFoodByUser(userId):
    tweets = db.get_tweet_by_user('tweet_data', userId)
    if tweets['all_records'] != None:
        for t in tweets['all_records']:
            tweet = t['value']
            CheckFoodByTweetJson(tweet)


user_file_name = 'data/userid.data'
dataFileSize = os.path.getsize(user_file_name)
blockSize = int(dataFileSize/comm_size)
blockSizeTiny = int(blockSize/comm_size)


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
            userInfo = CheckFoodByUser(userId)
            
            print('user:', userId, ' prefercence cal over.')


outFileName = 'data/food_category_count'+str(rank)+'.json'
with open(outFileName, 'w') as f:
    json.dump(foodWordCountByDate, f)


print('end')