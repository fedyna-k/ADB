"""
Module that contains functions to join movie table.
"""


from common import *


def __join_locale(movie: dict, database: Database) -> dict:
    """
    Join all locale title to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    titles = database.titles.aggregate([
        {"$match": {"mid": {"$eq": movie["mid"]}}},
        {"$sort": {"ordering": 1}}
    ])

    for title in titles:
        movie["titles"]["locale"].append({
            "title": title["title"],
            "region": title["region"],
            "language": title["language"],
            "types": title["types"],
            "attributes": title["attributes"],
            "isOriginal": title["isOriginalTitle"]
        })
    
    return movie


def __join_genres(movie: dict, database: Database) -> dict:
    """
    Join all genres to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    genres = database.genres.find(
        {"mid": movie["mid"]},
        {"_id": 0, "genre": 1}
    )
    movie["genres"] = [elem["genre"] for elem in genres]

    return movie


def __join_characters(movie: dict, database: Database) -> dict:
    """
    Join all characters to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    characters = database.characters.find(
        {"mid": movie["mid"]},
        {"_id": 0, "mid": 0}
    )
    characters_pid = extract("pid", characters.clone())

    characters_actors = list(database.persons.find(
        {"pid": {"$in": characters_pid}},
        {"_id": 0, "pid": 1, "primaryName": 1}
    ))

    # Join characters, persons and movies
    movie["characters"] = [
        {
            "pid": char["pid"],
            "name": char["name"],
            "actor": actor["primaryName"]
        }
            for char in characters
            for actor in characters_actors
            if char["pid"] == actor["pid"]
    ]

    return movie


def __join_writers(movie: dict, database: Database) -> dict:
    """
    Join all writers to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    writers = database.writers.find(
        {"mid": movie["mid"]},
        {"_id": 0, "mid": 0}
    )
    writers_pid = extract("pid", writers.clone())

    writers_names = list(database.persons.find(
        {"pid": {"$in": writers_pid}},
        {"_id": 0, "pid": 1, "primaryName": 1}
    ))

    # Join writers, persons and movies
    movie["writers"] = [
        {
            "pid": writ["pid"],
            "name": pers["primaryName"]
        }
        for writ in writers
        for pers in writers_names
        if pers["pid"] == writ["pid"]
    ]

    return movie


def __join_directors(movie: dict, database: Database) -> dict:
    """
    Join all directors to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    directors = database.directors.find(
        {"mid": movie["mid"]},
        {"_id": 0, "mid": 0}
    )
    directors_pid = extract("pid", directors.clone())

    directors_names = list(database.persons.find(
        {"pid": {"$in": directors_pid}},
        {"_id": 0, "pid": 1, "primaryName": 1}
    ))

    # Join directors, persons and movies
    movie["directors"] = [
        {
            "pid": direc["pid"],
            "name": pers["primaryName"]
        }
        for direc in directors
        for pers in directors_names
        if pers["pid"] == direc["pid"]
    ]

    return movie


def __join_principals(movie: dict, database: Database) -> dict:
    """
    Join all principals to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    principals = database.principals.find(
        {"mid": movie["mid"]},
        {"_id": 0, "mid": 0}
    )
    principals_pid = extract("pid", principals.clone())

    principals_names = list(database.persons.find(
        {"pid": {"$in": principals_pid}},
        {"_id": 0, "pid": 1, "primaryName": 1}
    ))

    # Join principals, persons and movies
    movie["principals"] = [
        {
            "pid": princ["pid"],
            "name": pers["primaryName"],
            "category": princ["category"],
            "job": princ["job"]
        }
        for princ in principals
        for pers in principals_names 
        if pers["pid"] == princ["pid"]
    ]

    return movie


def __join_episodes(movie: dict, database: Database) -> dict:
    """
    Join all episodes to a movie.
    :param: movie - The movie as dictionary.
    :param: database - The MongoDB database object.
    :return: The new dictionary
    """
    episodes = database.episodes.find(
        {"parentMid": movie["mid"]},
        {"_id":0, "parentMid":0}
    )
    episodes_mid = extract("mid", episodes.clone())

    episodes_info = list(database.movies.find(
        {"mid": {"$in": episodes_mid}},
        {"_id": 0}
    ))

    # Join episodes, persons and movies
    movie["episodes"] = [
        {
            "mid": episode["mid"],
            "seasonNumber": episode["seasonNumber"],
            "episodeNumber": episode["episodeNumber"],
            "primaryTitle": info["primaryTitle"],
            "isAdult": info["isAdult"],
            "startYear": info["startYear"],
            "endYear": info["endYear"],
            "runtimeMinutes": info["runtimeMinutes"]
        }
        for episode in episodes
        for info in episodes_info
        if episode["mid"] == info["mid"]
    ]

    return movie


def movie_join(movie: dict, database: Database) -> dict:
    """
    Get all joins between movies and the other tables
    that can give part of information.
    :param: movie - The movie entry from a cursor on movies collection.
    :return: The movie with all joins.
    """
    # Get the basic information
    movie = {
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

    movie = __join_locale(movie, database)
    movie = __join_genres(movie, database)
    movie = __join_characters(movie, database)
    movie = __join_writers(movie, database)
    movie = __join_directors(movie, database)
    movie = __join_principals(movie, database)

    if "episodes" in database.list_collection_names():
        movie = __join_episodes(movie, database)

    return movie