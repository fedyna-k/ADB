#! /usr/bin/env python

import pymongo
import sys

# Client declaration
mongo_client = pymongo.MongoClient()

# Get chosen database and prepare insertion
if len(sys.argv) != 2 or len(sys.argv) == 2 and sys.argv[1] not in ['tiny', 'full']:
    print("Provide 'tiny' or 'full' as argument.")
    sys.exit(1)

if sys.argv[1] == "tiny":
    mongo_database = mongo_client.BDAtiny
else:
    mongo_database = mongo_client.BDA

collections = mongo_database.list_collection_names()
for collection in collections:
    keys = list(mongo_database[collection].find_one({}, {"_id": 0}).keys())
    mongo_database[collection].create_indexes(keys)