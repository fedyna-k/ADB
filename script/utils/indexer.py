"""
Indexer module.
Use it to add indexes to MongoDB.
"""


# Guard clause from launch
if __name__ == "__main__":
    raise ImportError("This file must be imported.")


import pymongo
from pymongo.database import Database


def add_all_indexes(database: Database) ->  None:
    """
    Add index on all collection for a given database.
    The database should be in a SQL-like pattern.
    :param: database - The MongoDB database.
    """
    collections = database.list_collection_names()
    for collection in collections:
        # Get all "columns" based on first entry
        keys = list(database[collection].find_one({}, {"_id": 0}).keys())
        index_keys = list(map(lambda a: pymongo.IndexModel(a), keys))
        database[collection].create_indexes(index_keys)


def add_json_movie_indexes(database: Database) -> None:
    """
    Add index on all "useful" fields for the json_movie collection.
    :param: database - The MongoDB database.
    """
    keys = ["mid", "isAdult", "startYear", "endYear", "runtimeMinutes", "averageRating", "numVotes", "titles.primary", "titles.type", "titles.original"]
    index_keys = list(map(lambda a: pymongo.IndexModel(a), keys))
    database.json_movies.create_indexes(index_keys)