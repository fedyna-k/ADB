import pymongo

mongo_client = pymongo.MongoClient()
# mongo_database = mongo_client.BDA
mongo_database = mongo_client.BDAtiny

def extract(column, cursor):
    return list(map(lambda row: row[column], cursor))