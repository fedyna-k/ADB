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
mongo_database.drop_collection("json_movies")

# Create collection following the movie.jsonc file structure
# Get all movies without automatic _id
movie_cursor = mongo_database.movies.find({}, {"_id": 0})

for movie in movie_cursor:
    # Get the basic information
    struct = {
        "mid": movie["mid"],
        "isAdult": movie["isAdult"],
        "startYear": movie["startYear"],
        "endYear": movie["endYear"],
        "runtimeMinutes": movie["runtimeMinutes"],
        "titles": {
            "type": movie["titleType"],
            "primary": movie["primaryTitle"],
            "original": movie["originalTitle"],
            "locale": []
        }
    }

    # Get all locale titles
    titles = mongo_database.titles.aggregate([
        {"$match": { "mid": {"$eq": movie["mid"]} }},
        {"$sort": { "ordering": 1 }}
    ])
    for title in titles:
        struct["titles"]["locale"].append({
            "title": title["title"],
            "region": title["region"],
            "language": title["language"],
            "types": title["types"],
            "attributes": title["attributes"],
            "isOriginal": title["isOriginalTitle"]
        })
    
    # Get all genres
    genres = mongo_database.genres.find({ "mid": movie["mid"] }, {"_id": 0, "genre": 1})
    struct["genres"] = [elem["genre"] for elem in genres]

    # Get all characters
    characters = mongo_database.characters.find({ "mid": movie["mid"] }, {"_id": 0, "mid": 0})
    

    print(struct)
    break