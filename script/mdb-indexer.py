#! /usr/bin/env python

"""
-----------------------
Indexer utility script.
-----------------------
Use it to automaticaly add index to MongoDB database.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


import pymongo
import sys


# Client declaration
mongo_client = pymongo.MongoClient()


# Get chosen database and prepare insertion
if len(sys.argv) not in [2, 3] or len(sys.argv) in [2, 3] and sys.argv[1] not in ['tiny', 'full'] and sys.argv[2] not in [0, 1]:
    print("Usage: mongo_db_indexer <db: full|tiny> <json_movies only: 0|1>")
    sys.exit(1)

if sys.argv[1] == "tiny":
    mongo_database = mongo_client.BDAtiny
else:
    mongo_database = mongo_client.BDA


# Check if indexer has to index only json_movies or all database
if sys.argv[2] == "0":
    collections = mongo_database.list_collection_names()
    for collection in collections:
        keys = list(mongo_database[collection].find_one({}, {"_id": 0}).keys())
        mongo_database[collection].create_indexes(list(map(lambda a: pymongo.IndexModel(a), keys)))
else:
    keys = ["mid", "isAdult", "startYear", "endYear", "runtimeMinutes", "averageRating", "numVotes", "titles.primary", "titles.type", "titles.original"]
    mongo_database.json_movies.create_indexes(list(map(lambda a: pymongo.IndexModel(a), keys)))