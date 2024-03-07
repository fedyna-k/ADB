#! /usr/bin/env python

from common import *

known = mongo_database.ratings.find({
    "numVotes": {"$gt": 200000}
})