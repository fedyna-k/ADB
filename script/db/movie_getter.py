#! /usr/bin/env python

# Common declarations

import pymongo
import sys
import time

def extract(column, cursor):
    return list(map(lambda row: row[column], cursor))

mongo_client = pymongo.MongoClient()

# CLI code

if len(sys.argv) < 2:
    print("Usage : movie_getter [-f|-t]")
    sys.exit(1)

if sys.argv[1] == "-t":
    mongo_database = mongo_client.BDAtiny
else:
    mongo_database = mongo_client.BDA

collections = mongo_database.list_collection_names()

# Same function as mongo_db_structured.py in order to reconstruct
# the same movie and compare time.
def movie_join(movie):
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
    characters_pid = extract("pid", characters.clone())
    characters_actors = mongo_database.persons.find({ "pid": {"$in": characters_pid } }, {"_id": 0, "pid": 1, "primaryName": 1})
    characters_actors = list(characters_actors)
    struct["characters"] = [{
        "pid": char["pid"],
        "name": char["name"],
        "actor": actor["primaryName"]
    } for char in characters for actor in characters_actors if char["pid"] == actor["pid"]]
    
    # Get all writers
    writers = mongo_database.writers.find({ "mid": movie["mid"] }, {"_id": 0, "mid": 0})
    writers_pid = extract("pid", writers.clone())
    writers_names = mongo_database.persons.find({ "pid": {"$in": writers_pid } }, {"_id": 0, "pid": 1, "primaryName": 1})
    writers_names = list(writers_names)
    struct["writers"] = [{
        "pid": writ["pid"],
        "name": pers["primaryName"]
    } for writ in writers for pers in writers_names if pers["pid"] == writ["pid"]]
    
    # Get all directors
    directors = mongo_database.directors.find({ "mid": movie["mid"] }, {"_id": 0, "mid": 0})
    directors_pid = extract("pid", directors.clone())
    directors_names = mongo_database.persons.find({ "pid": {"$in": directors_pid } }, {"_id": 0, "pid": 1, "primaryName": 1})
    directors_names = list(directors_names)
    struct["directors"] = [{
        "pid": direc["pid"],
        "name": pers["primaryName"]
    } for direc in directors for pers in directors_names if pers["pid"] == direc["pid"]]

    # Get all principals
    principals = mongo_database.principals.find({ "mid": movie["mid"] }, {"_id": 0, "mid": 0})
    principals_pid = extract("pid", principals.clone())
    principals_names = mongo_database.persons.find({ "pid": {"$in": principals_pid } }, {"_id": 0, "pid": 1, "primaryName": 1})
    principals_names = list(principals_names)
    struct["principals"] = [{
        "pid": princ["pid"],
        "name": pers["primaryName"],
        "category": princ["category"],
        "job": princ["job"]
    } for princ in principals for pers in principals_names if pers["pid"] == princ["pid"]]

    # Episodes (for full only)
    if "episodes" in collections:
        episodes = mongo_database.episodes.find({"parentMid": movie["mid"]}, {"_id":0, "parentMid":0})
        episodes_mid = extract("mid", episodes.clone())
        episodes_info = mongo_database.movies.find({ "mid": {"$in": episodes_mid } }, {"_id": 0})
        episodes_info = list(episodes_info)
        struct["episodes"] = [{
            "mid": episode["mid"],
            "seasonNumber": episode["seasonNumber"],
            "episodeNumber": episode["episodeNumber"],
            "primaryTitle": info["primaryTitle"],
            "isAdult": info["isAdult"],
            "startYear": info["startYear"],
            "endYear": info["endYear"],
            "runtimeMinutes": info["runtimeMinutes"]
        } for episode in episodes for info in episodes_info if episode["mid"] == info["mid"]]

    return struct


# Get a good batch of movies (entire database for tiny one)
movies_to_find = mongo_database.movies.aggregate([{"$sample": {"size": 1000}}])
movies_to_find = extract("mid", movies_to_find)
direct_time = 0
homemade_time = 0
current = 0
for movie in movies_to_find:
    # Get movie from structured collection
    start = time.monotonic_ns()
    mongo_database.json_movies.find_one({ "mid": {"$eq": movie} })
    direct_time += time.monotonic_ns() - start

    # Get movie from homemade natural joins
    start = time.monotonic_ns()
    movie = mongo_database.movies.find_one({ "mid": {"$eq": movie} })
    movie_join(movie)
    homemade_time += time.monotonic_ns() - start

    current += 1
    sys.stdout.write(f"\rMovies done : {str(current).zfill(4)}/{1000} ({round(100 * current / 1000, 2)} %)")


print("\nMean time for batch of size 1000:")
print(f"Direct time:\t{round(direct_time / 1000)}ns")
print(f"Homemade time:\t{round(homemade_time / 1000)}ns")