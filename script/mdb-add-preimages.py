from utils.common import *

database = get_database(("full","tiny"))

collections = database.list_collection_names()
for collection in collections:
    database.command("collMod", collection, changeStreamPreAndPostImages={"enabled": True})