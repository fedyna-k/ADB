#! /usr/bin/env python

"""
---------------------
Script for 4th query.
---------------------
Usage : ./requete4.py [full|tiny]

Defaults to full database.
"""


from utils.common import *


mongo_database = get_database(("full", "tiny"), True)


# Get the maximum roles played by one actor in same movie
max_different_roles = mongo_database.characters.aggregate([
    {"$group" : {
        "_id": ["$mid", "$pid"],
        "count": {"$sum": 1}
    }},
    {"$group": {
        "_id": "_id",
        "max": {"$max": "$count"}
    }}
])
max_different_roles = list(max_different_roles)[0]["max"]

# Get the pid of the actors
swiss_knife_actors = mongo_database.characters.aggregate([
    {"$group" : {
        "_id": ["$mid", "$pid"],
        "pid": {"$first": "$pid"},
        "count": {"$sum": 1}
    }},
    {"$match": { "count": {"$eq": max_different_roles} }}
])
swiss_knife_actors = extract("pid", swiss_knife_actors)

# Get the names of thoses actors
actor_names = mongo_database.persons.find({
    "pid": {"$in": swiss_knife_actors}
}, {"primaryName": 1, "_id": 0})
actor_names = extract("primaryName", actor_names)

# Print results
print(f"{' Requete 4 ':~^50}\n")
print(actor_names)