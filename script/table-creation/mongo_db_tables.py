#! /usr/bin/env python

import pymongo
import sqlite3

# Table names
TABLES = ["characters", "directors", "episodes", "genres", "knownformovies", "movies", "persons", "principals", "professions", "ratings", "titles", "writers"]

# SQLite client
sqlite_database = sqlite3.connect("databases/full.db")
sqlite_cursor = sqlite_database.cursor()

# Mongo db client
mongo_client = pymongo.MongoClient()
mongo_database = mongo_client.BDA

# Create all collections
# PyMongo requires an insert to create a collection
# So we send an insert request, creating the collection
# then we empty the collection using a delete without filters.
for table in TABLES:
    mongo_database[table].insert_one({})
    mongo_database[table].delete_many({})

apply_keys = lambda k, v : dict(map(lambda i, j : (i, j), k, v))

# Fill table with information
for table in TABLES:
    print(f"Cloning data from table {table}...")    # Sprinkle some UX
    data = sqlite_cursor.execute(f"select * from {table};")
    columns = [row[0] for row in data.description]
    while (batch := data.fetchmany(1000)) != []:
        batch = list(map(lambda row: apply_keys(columns, row), batch))
        mongo_database[table].insert_many(batch)


# Closing connections
sqlite_cursor.close()
sqlite_database.commit()
sqlite_database.close()

mongo_client.close()