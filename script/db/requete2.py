#! /usr/bin/env python

from common import *

# Find all the millenials movies
millenials_movies = mongo_database.movies.find({
    "startYear" : {
        "$gt": 1999,
        "$lt": 2010
    } 
}, { "mid": 1, "_id": 0 })
millenials_movies = extract("mid", millenials_movies)

# Find all horror movies
horror_millenial_movies = mongo_database.genres.find({
    "genre": "Horror",
    "mid": {"$in": millenials_movies}
}, { "mid": 1, "_id": 0 })
horror_millenial_movies = extract("mid", horror_millenial_movies)

# Get top 3 spooks
true_spooks = mongo_database.ratings.aggregate([
    {"$match": {
        "mid": {"$in": horror_millenial_movies}
    }},
    {"$sort": {
        "averageRating": -1
    }},
    {"$limit": 3}
])
true_spooks = extract("mid", true_spooks)

# Get the names
true_spooks = mongo_database.movies.find({
    "mid": {"$in": true_spooks}
}, { "primaryTitle": 1, "_id": 0 })
true_spooks = extract("primaryTitle", true_spooks)

print(f"{' Requete 2 ':~^50}\n")
print("Three best horror movies :", true_spooks)