#! /usr/bin/env python

from common import *

# Get all movies that were released in Spain
spanish_movies = mongo_database.titles.find({ "region": "ES" }, {"mid": 1, "_id": 0})
spanish_movies = extract("mid", spanish_movies)

# Get all writers that wrote those movies
spanish_writers = mongo_database.writers.find({ "mid": {"$in": spanish_movies} }, {"pid": 1, "_id": 0})
spanish_writers = extract("pid", spanish_writers)

# Get the other writers
non_spanish_writers = mongo_database.writers.find({ "pid": {"$nin": spanish_writers} }, {"pid": 1, "_id": 0})
non_spanish_writers = extract("pid", non_spanish_writers)

# Get those names
non_spanish_writers_names = mongo_database.persons.find({ "pid": {"$in": non_spanish_writers} }, {"primaryName": 1, "_id": 0})
non_spanish_writers_names = extract("primaryName", non_spanish_writers_names)

# Print results
print(f"{' Requete 3 ':~^50}\n")
print("Writers that didn't like Spain :", non_spanish_writers_names, "\n")