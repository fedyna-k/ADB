#! /usr/bin/env python

from common import *

# Find all the millenials movies
millenials_movies = mongo_database.movies.find({ "startYear" : {"$gt": 1999, "$lt": 2010} }, {"mid": 1, "_id": 0})
millenials_movies = extract("mid", millenials_movies)
# Find all horror movies
horror_millenial_movies = mongo_database.genres.find({ "genre": "Horror", "mid": {"$in": millenials_movies} }, {"mid": 1, "_id": 0})
horror_millenial_movies = extract("mid", horror_millenial_movies)

# Get the top 3 spooky movies
true_spooks = [{}, {}, {}]
spooky_score = [0, 0, 0]
for spooks in horror_millenial_movies:
    score = mongo_database.ratings.find_one({ "mid": spooks })["averageRating"]
    # Insert spooky movie if it's spooky enough
    for i in range(3):
        if score > spooky_score[i]:
            true_spooks.insert(i, spooks)
            spooky_score.insert(i, score)
            true_spooks = true_spooks[:3]
            spooky_score = spooky_score[:3]
            break

true_spooks = mongo_database.movies.find({ "mid": {"$in": true_spooks} }, {"primaryTitle": 1, "_id": 0})
true_spooks = extract("primaryTitle", true_spooks)

print(f"{' Requete 2 ':~^50}\n")
print("Three best horror movies :", true_spooks)
print("Scores :", spooky_score, end="\n\n")