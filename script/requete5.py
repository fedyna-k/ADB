#! /usr/bin/env python

"""
---------------------
Script for 5th query.
---------------------
Usage : ./requete5.py [full|tiny]

Defaults to full database.
"""


from utils.common import *


mongo_database = get_database(("full", "tiny"), True)


# Get all known movies
known = mongo_database.ratings.find({
    "numVotes": {"$gt": 200000}
}, {"_id": 0, "mid": 1})

# Classify the stars based on Avatar released date
# We use sets as sets allow fast operation on unique elements
known_before = set()
known_after = set()
for movie in known:
    startYear = mongo_database.movies.find_one({"mid": movie["mid"]})["startYear"]
    principals = mongo_database.principals.find({"mid": movie["mid"]}, {"_id": 0, "pid": 1})
    principals = set(extract("pid", principals))

    if startYear < 2009:
        known_before |= principals

    if startYear > 2009:
        known_after |= principals

# Get the raising stars
raising_stars = list(known_after - known_before)

# Get Avatar mid
avatar = mongo_database.movies.find_one({"primaryTitle": "Avatar"}, {"_id": 0, "mid": 1})["mid"]

# Get only those who were in Avatar.
avatar_raising_stars = mongo_database.principals.find({
    "mid": avatar,
    "pid": {"$in": raising_stars}
}, {"_id": 0, "pid": 1})
avatar_raising_stars = extract("pid", avatar_raising_stars)

# Get the names
raising_stars_names = mongo_database.persons.find({
    "pid": {"$in": avatar_raising_stars}
}, {"primaryName": 1, "_id": 0})
raising_stars_names = extract("primaryName", raising_stars_names)

print(raising_stars_names)