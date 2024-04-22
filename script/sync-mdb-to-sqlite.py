#! /usr/bin/env python


"""
-----------------------------
Synchronisation wrapper (M2S)
-----------------------------
Allow to impact change from MongoDB to SQLite.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.common import *
import sqlite3
import sys

# Get databases
mdb_database = get_database(("full", "tiny"))
current_path = sys.path[0]
if argv[1] == "tiny":
    sql_database = sqlite3.connect(current_path + '/../databases/tiny.db')
    sql_cursor = sql_database.cursor()
elif argv[1] == "full":
    sql_database = sqlite3.connect(current_path + '/../databases/full.db')
    sql_cursor = sql_database.cursor()


join_filter = lambda d, s=" and ": s.join([f"{k}='{v}'" for k, v in d.items() if k != "_id"])
get_c_v = lambda d: zip(*[(k, v) for k, v in d.items() if k != "_id"])


change_stream = mdb_database.watch(full_document_before_change="required")
for change in change_stream:
    if change["operationType"] == "insert":
        columns, values = get_c_v(change["fullDocument"])

        print(f"Added entry {values} to {change['ns']['coll']}")

        sql_cursor.execute(f"insert into {change['ns']['coll']} {str(columns)} values {str(values)}")
        sql_database.commit()
        
    if change["operationType"] == "replace":
        if change['ns']['coll'] == "movies":
            del change["fullDocument"]["mid"]

        if change['ns']['coll'] == "persons":
            del change["fullDocument"]["pid"]

        old = join_filter(change["fullDocumentBeforeChange"])
        new = join_filter(change["fullDocument"], ",")
        _, old_v = get_c_v(change['fullDocumentBeforeChange'])
        _, new_v = get_c_v(change['fullDocument'])

        print(f"Edit entry {str(old_v)} to {str(new_v)} in {change['ns']['coll']}")

        sql_cursor.execute(f"update {change['ns']['coll']} set {new} where {old}")
        sql_database.commit()

    if change["operationType"] == "delete":
        old = join_filter(change["fullDocumentBeforeChange"])
        _, old_v = get_c_v(change['fullDocumentBeforeChange'])

        print(f"Delete entry {str(old_v)} in {change['ns']['coll']}")

        sql_cursor.execute(f"delete from {change['ns']['coll']} where {old}")
        sql_database.commit()