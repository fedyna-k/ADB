"""
Module that contains functions to create threads for SQLite to MongoDB sync.
"""


# Guard clause from launch
if __name__ == "__main__":
    raise ImportError("This file must be imported.")


from threading import Lock, Thread
from pymongo.database import Database
import sys
import sqlite3


# Helper function
apply_keys = lambda k, v : dict(map(lambda i, j : (i, j), k, v))


def acknowledge(message: str) -> None:
    """
    Print a message preceded by [ OK ] tag
    """
    print(f"[ \x1b[92mOK\x1b[0m ] {message}")


def __get_sql_database() -> None:
    """
    Connect to sql database (thread safe).
    :return: A cursor pointing toward the sql database.
    """
    current_path = sys.path[0]

    if sys.argv[1] == "tiny":
        sql_database = sqlite3.connect(current_path + '/../databases/tiny.db').cursor()
    elif sys.argv[1] == "full":
        sql_database = sqlite3.connect(current_path + '/../databases/full.db').cursor()

    return sql_database


def __delete(table_name: str, row_data: list[str], columns: list[str], sem: Lock, mdb_database: Database) -> None:
    """
    --Thread function-- Delete given row in MongoDB.
    :param: table_name - The altered table
    :param: row_data - The deleted row
    :param: columns - The name of the table columns
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    mdb_database[table_name].delete_one(apply_keys(columns, row_data))
    
    acknowledge(f"Deleted row in MongoDB '{table_name}' collection")
    sem.release()


def __insert(table_name: str, row_id: int, sem: Lock, mdb_database: Database) -> None:
    """
    --Thread function-- Insert given row in MongoDB.
    :param: table_name - The altered table
    :param: row_id - The new row id
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    sql_database = __get_sql_database()
    cursor = sql_database.execute(f"select * from {table_name} where rowid={row_id}")
    columns = [row[0] for row in cursor.description]
    row = cursor.fetchone()

    mdb_database[table_name].insert_one(apply_keys(columns, row))

    acknowledge(f"Inserted row in MongoDB '{table_name}' collection")
    sem.release()


def __update(table_name: str, row_id: int, row_data_before: list[str], columns: list[str], sem: Lock, mdb_database: Database) -> None:
    """
    --Thread function-- Update given row in MongoDB.
    :param: table_name - The altered table
    :param: row_id - The altered row id
    :param: row_data_before - The altered row before update
    :param: columns - The name of the table columns
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    sql_database = __get_sql_database()
    cursor = sql_database.execute(f"select * from {table_name} where rowid={row_id}")
    row = cursor.fetchone()

    mdb_database[table_name].find_one_and_replace(apply_keys(columns, row_data_before), apply_keys(columns, row))

    acknowledge(f"Updated row in MongoDB '{table_name}' collection")
    sem.release()


def start_delete_thread(table_name: str, row_data: list[str], columns: list[str], sem: Lock, mdb_database: Database) -> None:
    """
    Start a Thread that deletes given row in MongoDB.
    :param: table_name - The altered table
    :param: row_data - The deleted row
    :param: columns - The name of the table columns
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    Thread(target=__delete, args=(table_name, row_data, columns, sem, mdb_database)).start()


def start_insert_thread(table_name: str, row_id: int, sem: Lock, mdb_database: Database) -> None:
    """
    Starts a Thread that inserts given row in MongoDB.
    :param: table_name - The altered table
    :param: row_id - The new row id
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    Thread(target=__insert, args=(table_name, row_id, sem, mdb_database)).start()


def start_update_thread(table_name: str, row_id: int, row_data_before: list[str], columns: list[str], sem: Lock, mdb_database: Database) -> None:
    """
    Starts a Thread that updates given row in MongoDB.
    :param: table_name - The altered table
    :param: row_id - The altered row id
    :param: row_data_before - The altered row before update
    :param: columns - The name of the table columns
    :param: sem - The semaphore used for CLI sync
    :param: mdb_database - The MongoDB database
    """
    Thread(target=__update, args=(table_name, row_id, row_data_before, columns, sem, mdb_database)).start()