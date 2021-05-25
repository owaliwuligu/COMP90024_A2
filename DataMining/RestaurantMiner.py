import dask.dataframe as dd
import re
import CouchDBApi as db
import json
from datetime import datetime
from mpi4py import MPI
import mmap
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

restaurant_filename = 'features/restaurants.csv' 
data_train          = dd.read_csv(restaurant_filename)
shopname_list       = list(data_train['trading_name'])
x_list              = list(data_train['x_coordinate'])
y_list              = list(data_train['y_coordinate'])
address_list        = list(data_train['street_address'])
area_list           = list(data_train['clue_small_area'])

for i in range(0, len(shopname_list)):
    shopname_list[i] = shopname_list[i].lower()
#
shopCountByDate = {}

def CheckShopByTweetJson(tweet):
    text = tweet['text']
    # time line
    created_at = tweet['created_at']
    date = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')
    year = date.strftime('%Y')
    month = date.strftime('%m')
    dateString = year+'-'+month
    #
    
    text = text.lower()
    for i in range(0, len(shopname_list)):
        shopname = shopname_list[i]
        count = text.count(shopname)

        if not shopname in shopCountByDate:
            shopCountByDate[shopname] = {'total':0}
        shopCountByDate[shopname]['total'] += count
        if not dateString in shopCountByDate[shopname]:
            shopCountByDate[shopname][dateString] = 0
        shopCountByDate[shopname][dateString] += count

def CheckShopByUser(userId):
    tweets = db.get_tweet_by_user('tweet_data', userId)
    if tweets['all_records'] != None:
        for t in tweets['all_records']:
            tweet = t['value']
            CheckShopByTweetJson(tweet)



user_file_name = 'data/userid.data'
dataFileSize = os.path.getsize(user_file_name)
blockSize = int(dataFileSize/comm_size)
blockSizeTiny = int(blockSize/comm_size)


dataCount = 0
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
            userInfo = CheckShopByUser(userId)
            dataCount += 1
            print('user:', userId, ' prefercence cal over. ', dataCount)


for i in range(0, len(data_train)):
    shop = shopname_list[i]
    x = x_list[i]
    y = y_list[i]
    if shop in shopCountByDate:
        shopCountByDate[shop]['coordinates'] = [x,y]


outFileName = 'data/shop_count'+str(rank)+'.json'
with open(outFileName, 'w') as f:
    json.dump(shopCountByDate, f)


print('end')