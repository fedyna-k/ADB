#! /usr/bin/env python


"""
----------------
Preimages script
----------------
Use it to add preimage recordings in MongoDB.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.common import *


database = get_database(("full","tiny"))

# Loop through all collections of the database and run command
# to add the valid option.
# All the options provided on forums were too old, check the mongodb
# docs to make sure the option is the right one.
collections = database.list_collection_names()
for collection in collections:
    database.command("collMod", collection, changeStreamPreAndPostImages={"enabled": True})