#! /usr/bin/env python


"""
-----------------------------
MongoDB table creator script.
-----------------------------
Create all mongodb tables based on sqlite tables.

This script also create all associated index as mongodb
only add index on the "_id" field.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


import sqlite3
from utils.common import *
from utils.indexer import add_all_indexes


# Table names
TABLES = ["characters", "directors", "episodes", "genres", "knownformovies", "movies", "persons", "principals", "professions", "ratings", "titles", "writers"]

# SQLite client
sqlite_database = sqlite3.connect("databases/full.db")
sqlite_cursor = sqlite_database.cursor()

# MongoDB database
mongo_database = get_database(("full", "tiny"))

# Helper function
apply_keys = lambda k, v : dict(map(lambda i, j : (i, j), k, v))

# Fill collections with information
for table in TABLES:
    print(f"Cloning data from table {table}...")    # Sprinkle some UX
    data = sqlite_cursor.execute(f"select * from {table};")
    columns = [row[0] for row in data.description]
    while (batch := data.fetchmany(1000)) != []:
        batch = list(map(lambda row: apply_keys(columns, row), batch))
        mongo_database[table].insert_many(batch)


# Closing connections for sqlite
sqlite_cursor.close()
sqlite_database.close()

print("Create all indexes...")
add_all_indexes(mongo_database)