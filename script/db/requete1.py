#! /usr/bin/env python

from common import *

# Find jean and his characters
jean = mongo_database.persons.find_one({
    "primaryName": "Jean Reno"
})
not_really_jean = mongo_database.characters.find({
    "pid": jean["pid"]
})
not_really_jean = extract("mid", not_really_jean)

# Find the movies associated with jean
movies_where_jean_is_not_really_jean = mongo_database.movies.find({
    "mid": { "$in": not_really_jean }
})
movies_where_jean_is_not_really_jean = extract("primaryTitle", movies_where_jean_is_not_really_jean)

print(f"{' Requete 1 ':~^50}\n")
print(movies_where_jean_is_not_really_jean, end="\n\n")