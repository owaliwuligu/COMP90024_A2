#!/usr/bin/python
import requests
import json


def get_all_dbs():
    """Get all databases of CouchDB

    :return: all databases of CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/_all_dbs"
    r = requests.get(url)
    if r.status_code == 200:
        print "Successfully get all databases."
    else:
        print "Fail to get all databases."
    print "status code: "+str(r.status_code)
    return r.content


def get_db(database):
    """Get the target database info

    :param database: the target database name
    :return: the target database info
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database
    r = requests.get(url)
    if r.status_code == 200:
        print "Successfully get the database info."
    else:
        print "Fail to get the database info."
    print "status code: "+str(r.status_code)
    return r.content


def get_all_docs(database):
    """Get all document contents of target database

    :param database: the target database name
    :return: all document contents returned from CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database+"/_all_docs"
    r = requests.get(url)
    if r.status_code == 200:
        print "Successfully get all document contents."
    else:
        print "Fail to get all document contents."
    print "status code: "+str(r.status_code)
    return r.content


def get_doc(database, doc_id):
    """Get the target document content

    :param database: the target database name
    :param doc_id: the target document id
    :return: the document content returned from CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database+"/"+doc_id
    r = requests.get(url)
    if r.status_code == 200:
        print "Successfully get the document content."
    else:
        print "Fail to get the document content."
    print "status code: "+str(r.status_code)
    return r.content


def upload_doc(database, doc):
    """Upload the document into CouchDB

    :param database: the target database name
    :param doc: the document content as JSON String format
    :return: the upload result returned from CouchDB
    """
    url = "http://admin:616161@172.26.133.30:5984/"+database
    r = requests.post(url, headers={'Content-Type': 'application/json'}, data=doc)
    if r.status_code == 201:
        print "Successfully upload the document."
    else:
        print "Fail to upload the document."
    print "status code: "+str(r.status_code)
    return r.content


# content = get_all_docs("tweet_data")
# print content

# tweet_data_file = open("sniffer.data", mode='r')
# tweet_data = tweet_data_file.readline()
# while tweet_data:
#     res = upload_doc("tweet_data", tweet_data)
#     print res
#     tweet_data = tweet_data_file.readline()
