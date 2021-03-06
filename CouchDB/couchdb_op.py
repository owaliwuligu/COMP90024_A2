#!/usr/bin/python
import requests
import json


def get_all_dbs():
    """Get all databases of CouchDB

    :return: all databases of CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/_all_dbs"
    r = requests.get(url)
    print("status code: " + str(r.status_code))
    if r.status_code == 200:
        print("Successfully get all databases.")
        return r.content
    else:
        print("Fail to get all databases.")
        return None


def get_db(database):
    """Get the target database info

    :param database: the target database name
    :return: the target database info
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database
    r = requests.get(url)
    print("status code: " + str(r.status_code))
    if r.status_code == 200:
        print("Successfully get the database info.")
        return r.content
    else:
        print("Fail to get the database info.")
        return None


def get_all_docs(database):
    """Get all document contents of target database

    :param database: the target database name
    :return: all document contents returned from CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database+"/_all_docs"
    r = requests.get(url)
    print("status code: " + str(r.status_code))
    if r.status_code == 200:
        print("Successfully get all document contents.")
        return r.content
    else:
        print("Fail to get all document contents.")
        return None


def get_doc(database, doc_id):
    """Get the target document content

    :param database: the target database name
    :param doc_id: the target document id
    :return: the document content returned from CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database+"/"+doc_id
    r = requests.get(url)
    print("status code: " + str(r.status_code))
    if r.status_code == 200:
        print("Successfully get the document content.")
        return r.content
    else:
        print("Fail to get the document content.")
        return None


def upload_doc(database, doc):
    """Upload the document into CouchDB

    :param database: the target database name
    :param doc: the document content as JSON String format
    :return: the upload result returned from CouchDB
    """
    if not json.loads(doc):
        return None
    url = "http://admin:616161@172.26.133.30:5984/"+database+"/"+json.loads(doc)['user']['id_str']
    r = requests.put(url, headers={'Content-Type': 'application/json'}, data=doc)
    print("status code: " + str(r.status_code))
    if r.status_code == 201:
        print("Successfully upload the document.")
        return r.content
    else:
        print("Fail to upload the document.")
        return None


def get_tweet_by_user(database, user_id):
    """Get the tweet number and latest tweet time of target user

    :param database: the target database name
    :param user_id: the target user id
    :return: dict with user_id, tweet_number, latest_tweet, all_records. The all_records is a list of JSON
            with format of [{"id":xxx,"key":xxx,"value":{"_id":xxx,"_rev":xxx,...}},{...},...]
    """
    url_count = "http://admin:616161@172.26.133.30:5984/" + database + "/_design/user_query/_view/user_count"
    url_time = "http://admin:616161@172.26.133.30:5984/"+database+"/_design/user_query/_view/user_latest"
    url_tweet = "http://admin:616161@172.26.133.30:5984/" + database + "/_design/user_query/_view/by_user_id"
    para = '{"startkey": "'+user_id+'", "endkey": "'+user_id+'"}'
    r_count = requests.post(url_count, headers={'Content-Type': 'application/json'}, data=para)
    r_time = requests.post(url_time, headers={'Content-Type': 'application/json'}, data=para)
    r_tweet = requests.post(url_tweet, headers={'Content-Type': 'application/json'}, data=para)
    print("status code: " + str(r_count.status_code) + "/" + str(r_time.status_code) + "/" + str(r_tweet.status_code))
    if r_count.status_code == 200 and r_time.status_code == 200 and r_tweet.status_code == 200:
        print("Successfully get the user record.")
        if json.loads(r_count.content)['rows']:
            res = {'user_id': user_id, 'tweet_number': json.loads(r_count.content)['rows'][0]['value'],
                   'latest_tweet': json.loads(r_time.content)['rows'][0]['value'],
                   'all_records': json.loads(r_tweet.content)['rows']}
            return res
        return {'user_id': user_id, 'tweet_number': 0, 'latest_tweet': None, 'all_records': None}
    else:
        print("Fail to get the user record.")
        return None


def get_preference(database, user_id):
    """Get the preference information of target user

    :param database: the target database name
    :param user_id: the target user id
    :return: dict with _id, coordinates.coordinates, food_preference, user
    """
    url = "http://admin:616161@172.26.133.30:5984/" + database + "/_design/query/_view/get_data"
    para = '{"startkey": "'+user_id+'", "endkey": "'+user_id+'"}'
    r = requests.post(url, headers={'Content-Type': 'application/json'}, data=para)
    print("status code: " + str(r.status_code))
    if r.status_code == 200:
        print("Successfully get the preference record.")
        return r.content
    else:
        print("Fail to get the user record.")
        return None


# content = get_tweet_by_user("tweet_data", "907883257802326016")
# print(content)

# tweet_data_file = open("sniffer.data", mode='r')
# tweet_data = tweet_data_file.readline()
# while tweet_data:
#     res = upload_doc("tweet_data", tweet_data)
#     print(res)
#     tweet_data = tweet_data_file.readline()

# content = get_preference("user_food_preference_score", "100143621")
# print(content)

# tweet_data_file = open("user_food_preference_score.json", mode='r')
# tweet_data = json.loads(tweet_data_file.read())
# count = 0
# for key, value in tweet_data.items():
#     count += 1
#     res = upload_doc("user_food_preference_score", json.dumps(value))
# print(count)
