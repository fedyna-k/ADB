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


known = mongo_database.ratings.find({
    "numVotes": {"$gt": 200000}
})