"""
Common module for queries.
Imports pymongo and defines the utils functions.
"""


# Guard clause from launch
if __name__ == "__main__":
    raise ImportError("This file must be imported.")


import pymongo
from pymongo.database import Database
from sys import argv


mongo_client = pymongo.MongoClient("mongodb://localhost:27017,localhost:27041,localhost:27042/?replicaSet=rs0")


def get_database(arguments: tuple[str, str]|None = None, optional=False, argv_index=1) -> Database:
    """
    Get database based on sys.argv[argv_index] if arguments is provided.
    Defaults to BDA (the full database).
    :param: arguments - The arguments to listen to. First must be for full, second for tiny.
    :param: optional - Is the argument optional? If so, default to BDA.
    :param: argv_index - The position in sys.argv.
    :return: The corresponding database.
    """
    if arguments is None or len(argv) == 1 and optional:
        return mongo_client.BDA
    
    if len(arguments) != 2:
        raise TypeError(f"'arguments' array must be of size 2 (given was {len(arguments)})")

    if argv[argv_index] == arguments[1]:
        return mongo_client.BDAtiny
    elif argv[argv_index] == arguments[0]:
        return mongo_client.BDA
    else:
        raise SyntaxError(f"Given argument does not correspond to a valid choice: '{arguments[0]}' or '{arguments[1]}' ({argv[argv_index]} given)")


def extract(field: str, cursor: pymongo.CursorType) -> list:
    """
    Extract a field from a pymongo cursor. Note that if you want to reuse the cursor, you must pass a clone (can be slow).
    :param: field - The field key
    :param: cursor - The pymongo cursor (from a find or aggregate)
    :return: A list of all fields for the cursor.
    """
    return list(map(lambda row: row[field], cursor))
