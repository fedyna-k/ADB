#! /usr/bin/env python


"""
-----------------
Benchmark script.
-----------------
Use it to compare access time between json_movies
and movies using movie_join function.

Of course, accessing with json_movies is way faster
given that it can also be indexed and it already
contains the information.

Note that this speed induces a loss in memory.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.join import *
from time import monotonic_ns
from sys import stdout
from importlib import import_module


# Get database
mongo_database = get_database(("-f", "-t"), optional=True)

# Get a good batch of movies (entire database for tiny one)
movie_sample = mongo_database.movies.aggregate([{"$sample": {"size": 1000}}])
movie_sample = extract("mid", movie_sample)

# Var used to count time
direct_time = 0
homemade_time = 0
current = 0

# Compare for given batch
for movie in movie_sample:
    # Get movie from structured collection
    start = monotonic_ns()
    mongo_database.json_movies.find_one({ "mid": {"$eq": movie} })
    direct_time += monotonic_ns() - start

    # Get movie from homemade natural joins
    start = monotonic_ns()
    movie = mongo_database.movies.find_one({ "mid": {"$eq": movie} })
    movie_join(movie, mongo_database)
    homemade_time += monotonic_ns() - start

    current += 1
    stdout.write(f"\rMovies done : {str(current).zfill(4)}/{1000} ({round(100 * current / 1000, 2)} %)")


print("\nMean time for batch of size 1000:")
print(f"Direct time:\t{round(direct_time / 1000)}ns")
print(f"Homemade time:\t{round(homemade_time / 1000)}ns")