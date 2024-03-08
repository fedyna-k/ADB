#! /usr/bin/env python


"""
---------------------------
SQLite table import script.
---------------------------
Create all SQLite tables based on CSV files.

Provides a small CLI to make table creation
much faster and safer.
"""


# Guard clause from import
if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


from utils.sql import *
import sqlite3


# Read from argv
if sys.argv[1] == "--help":
    print("Usage : python3 table_creator.py <database> <csv file|dir> [...<csv file|dir>]")
    exit(0)

if len(sys.argv) < 3:
    raise SyntaxError("Please use correct syntax.\nFor further help, type : python3 table_creator.py --help")


# Connect to data-base
db = sqlite3.connect(sys.argv[1] + ".db")
cursor = db.cursor()
    

print(f"{' Createur de table ':-^63}")
print("\nPour valider le type proposé, appuyez sur ENTRER, sinon entrez un nouveau type.")
print("Si un type n'a pas pu être déterminé à partir de la base, il faut le renseigner.")


paths = get_all_path()
tables = {}
primary_keys_tables = {}
tables_requests = {}
tables_without_fk = []


# Create all tables
for path in paths:
    # Open CSV file
    with open(path, "r", encoding="utf8") as file:
        # Get all basic pieces of informations
        table_name = get_table_name(path)
        tables[table_name] = []
        header = get_header(file)
        first_entry = process_entry(file.readline())
        
        request = "("

        print(f"\n{' ' + table_name + ' ':=^63}\n")
        print(f"{'Argument name':^20}|{'Recommanded type':^20}|{'Entered type':^20}")
        print(f"{'':-^63}")

        # Ask for all column types
        for title, entry in zip(header, first_entry):
            tables[table_name].append(title)
            recommanded_type = get_recommanded_type(entry)
            inputed_type = get_inputed_type(title, recommanded_type)
        
            request += title + " " + inputed_type + ", "

        # Ask for primary keys
        primary_keys = tuple(input("Entrez les clés primaires (séparées par ',') : ").split(","))
        if primary_keys != ("",):
            primary_keys_tables[table_name] = primary_keys
            request += f"PRIMARY KEY ({', '.join(primary_keys)})"
        else:
            primary_keys_tables[table_name] = "AUTOCREATED"
            request = request[:-2]

        tables_requests[table_name] = request


# Add foreign keys
for table in tables.keys():
    print(f"\nPour la table {table}...")
    print(f"Rappel des colonnes : {', '.join(tables[table])}\n")
    foreign_keys = tuple(input("Entrez les clés étrangères (séparées par ',') : ").split(","))

    # No foreign keys where provided
    if foreign_keys == ("",):
        tables_without_fk.append(table)
        tables_requests[table] += ");"
        continue

    # Link the foreign keys to corresponding tables
    for key in foreign_keys:
        fk_table = get_table(tables, primary_keys_tables, key)
        tables_requests[table] += f", FOREIGN KEY ({key}) REFERENCES {fk_table}({primary_keys_tables[fk_table][0]})"
        
    tables_requests[table] += ");"


# Create all tables
for table in tables_without_fk:
    cursor.execute("CREATE TABLE " + table + tables_requests[table])

for table in tables.keys():
    if not (table in tables_without_fk):
        cursor.execute("CREATE TABLE " + table + tables_requests[table])


print("\nAjouts des valeurs ...\n")


# Add all data
for path in paths:
    with open(path, "r", encoding="utf8") as file:
        table_name = get_table_name(path)
        print("Table : " + table_name + "...")
        # Get rid of header
        file.readline()

        while (line := file.readline()):
            values = process_entry(line)
            value_count = len(values)
            cursor.execute("INSERT INTO " + table_name + " VALUES (" + ", ".join(["?"] * value_count) + ")", values)


cursor.close()
db.commit()
db.close()