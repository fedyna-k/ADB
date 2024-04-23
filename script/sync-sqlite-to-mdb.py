#! /usr/bin/env python


"""
-----------------------------
Synchronisation wrapper (S2M)
-----------------------------
Allow to impact change from SQLite to MongoDB.

Because SQLite can't trigger external interface, we have to
use this file as a CLI for INSERT, UPDATE, and DELETE.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.common import *
from utils.threads import *
from ctypes import *
import sqlite3
import sys


# Constants found on the web
SQLITE_DELETE =  9
SQLITE_INSERT = 18
SQLITE_UPDATE = 23


# Get databases
mdb_database = get_database(("full", "tiny"))
current_path = sys.path[0]
dll = CDLL(current_path + "/lib/sqlite3.dll")

# Get sqlite database in C
db = c_void_p()
if len(argv) == 2 and argv[1] == "tiny":
    dll.sqlite3_open((current_path + '/../databases/tiny.db').encode(), byref(db))
    sql_database = sqlite3.connect(current_path + '/../databases/tiny.db').cursor()
elif len(argv) == 2 and argv[1] == "full":
    dll.sqlite3_open((current_path + '/../databases/full.db').encode(), byref(db))
    sql_database = sqlite3.connect(current_path + '/../databases/full.db').cursor()
else:
    raise ArgumentError("Usage: ./sync-sqlite-to-mdb.py <full|tiny>")


# Semaphore used for CLI print synchronisation
sem = Lock()


def __sqlite_to_mongodb(user_data, operation, db_name, table_name, row_id):
    """
    SQLite update hook callback function.
    :param: user_data - The third param of the sqlite3_update_hook. (unused)
    :param: operation - One of the constants SQLITE_*.
    :param: db_name - The affected database. (unused)
    :param: table_name - The affected table.
    :param: row_id - The affected row ID.
    """
    sem.acquire()
    table_name = table_name.decode().lower()

    if operation == SQLITE_DELETE:
        acknowledge("Triggered delete hook")
        acknowledge(f"Starting delete thread on {table_name}:{row_id}")

        cursor = sql_database.execute(f"select * from {table_name} where rowid={row_id}")
        columns = [row[0] for row in cursor.description]
        row = cursor.fetchone()

        start_delete_thread(table_name, row, columns, sem, mdb_database)

    elif operation == SQLITE_INSERT:
        acknowledge("Triggered insert hook")
        acknowledge(f"Starting insert thread on {table_name}:{row_id}")

        start_insert_thread(table_name, row_id, sem, mdb_database)

    elif operation == SQLITE_UPDATE:
        acknowledge("Triggered update hook")
        acknowledge(f"Starting update thread on {table_name}:{row_id}")

        cursor = sql_database.execute(f"select * from {table_name} where rowid={row_id}")
        columns = [row[0] for row in cursor.description]
        row = cursor.fetchone()
        
        start_update_thread(table_name, row_id, row, columns, sem, mdb_database)


# Register hook
sqlite_to_mongodb = CFUNCTYPE(c_void_p, c_void_p, c_int, c_char_p, c_char_p, c_int64)(__sqlite_to_mongodb)
dll.sqlite3_update_hook(db, sqlite_to_mongodb, None)


# Create a small sqlite CLI
err = c_char_p()
while True:
    sem.acquire()

    request = input(f"\x1b[1m\x1b[92mSQLite:\x1b[0m \x1b[93m{argv[1]}\x1b[0m > ")
    if request in ["exit", "q"]:
        break
    if not (request.startswith("delete") or request.startswith("insert") or request.startswith("update")):
        print("\x1b[3m\x1b[91mThis CLI only does 'delete', 'insert' or 'update'.\x1b[0m")
        sem.release()
        continue

    sem.release()

    byte_string = request.encode()
    dll.sqlite3_exec(db, byte_string, None, None, byref(err))
    if err:
        print("\x1b[3m\x1b[91m" + err.value.decode() + "\x1b[0m")
        sem.release()