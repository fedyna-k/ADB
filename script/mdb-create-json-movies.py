#! /usr/bin/env python


"""
--------------------------
JSON movie creator script.
--------------------------
Create all JSON movies following the movie.jsonc file.

This operation can take some time depending on
the database size. On my computer it took about 12h
to compute all movies for the full database, whereas
it took only 5s for the tiny one.

Note that it doesn't add the indexes.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.join import *
from sys import stdout


# Get database and prepare it
mongo_database = get_database(("full", "tiny"))
collections = mongo_database.list_collection_names()
mongo_database.drop_collection("json_movies")


# Create collection following the movie.jsonc file structure

# Get all movies without automatic _id
movie_cursor = mongo_database.movies.find({}, {"_id": 0})
batch = []

total = mongo_database.movies.count_documents({})
total_length = len(str(total))
current = 0

for movie in movie_cursor:
    # Add joined movie to batch and count
    batch.append(movie_join(movie, mongo_database))
    current += 1
    stdout.write(f"\rMovies done : {str(current).zfill(total_length)}/{total} ({round(100 * current / total, 2)} %)")

    # If batch is full, insert it to database and flush it
    if len(batch) == 100:
        mongo_database.json_movies.insert_many(batch)
        batch = []

# Insert the remaining joined movies
if len(batch) != 0:
    mongo_database.json_movies.insert_many(batch)

print("")