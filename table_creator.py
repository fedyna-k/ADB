import sqlite3
import sys
import os
import re
from typing import TextIO


# Guard closes
if __name__ != "__main__":
    raise ImportError("This script must be launched as main.")

if sys.argv[1] == "--help":
    print("Usage : python3 table_creator.py <database> <csv file|dir> [...<csv file|dir>]")
    exit(0)

if len(sys.argv) < 3:
    raise SyntaxError("Please use correct syntax.\nFor further help, type : python3 table_creator.py --help")


def get_all_path() -> list[str]:
    """
    Get all paths given in argv.
    Scan all directories given.
    :return: - All the path leading to files
    """
    paths = []
    for given_path in sys.argv[2:]:
        # It is a file
        if os.path.exists(given_path) and os.path.isfile(given_path):
            paths.append(given_path)

        # It is a directory
        if os.path.exists(given_path) and os.path.isdir(given_path):
            for file in os.listdir(given_path):
                if os.path.isfile(given_path + "/" + file):
                    paths.append(given_path + "/" + file)

    return paths


# Helper functions
process_header = lambda e: e.replace(",", "").replace("(", "").replace(")", "").replace("'", "")
get_table_name = lambda e: (e.split("/")[-1]).split(".")[0].upper()

def process_entry(line):
    args = []
    current = ""
    i = 0
    in_quote = False

    while i < len(line):
        if not in_quote and line[i] == ",":
            args.append(current)
            current = ""
            i += 1
            continue

        if line[i] == '"':
            in_quote = not in_quote
            i += 1
            continue

        current += line[i]
        i += 1

    args.append(current)

    return args


def get_header(file: TextIO) -> list[str]:
    """
    Get raw table header and entries.
    :return: - Header and entries
    """
    header = file.readline()

    header = "".join(list(map(process_header, header)))[1:-2]
    header = header.split('""')

    return header


def get_recommanded_type(entry: str) -> str:
    """
    Get recommanded type based on given entry.
    If no type can be found, return "-".
    :return: - The recommande type
    """
    if entry == "":
        return "-"
    
    if re.match("[0-9]*\.[0-9]+", entry):
        return "REAL"

    if re.match("[0-9]+", entry):
        return "INT"
    
    return "TEXT"


def get_inputed_type(title: str, recommanded_type: str) -> str:
    """
    Ask for input until valid one is given
    :return: - The inputed type
    """
    while True:
        print(f"{title:^20}|{recommanded_type:^20}| ", end="")
        inputed_type = input("")
        if inputed_type == "":
            inputed_type = recommanded_type

        if inputed_type != "-" and inputed_type in ["INT", "TEXT", "REAL"]:
            break
    
    return inputed_type


def get_table(tables: dict, primary_keys: dict, key: str) -> str:
    """
    Ask for input until valid one is given
    :return: - The table
    """
    while True:
        fk_table = input(f"Entrez la table associée à {key} : ")

        if fk_table in tables.keys() and len(primary_keys[fk_table]) == 1:
            break

        print("Table non existante ou ne contenant pas une clé étrangère simple.")
    
    return fk_table


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
    with open(path, "r", encoding="utf8") as file:
        table_name = get_table_name(path)
        tables[table_name] = []
        header = get_header(file)
        first_entry = process_entry(file.readline())
        
        request = "("

        print(f"\n{' ' + table_name + ' ':=^63}\n")
        print(f"{'Argument name':^20}|{'Recommanded type':^20}|{'Entered type':^20}")
        print(f"{'':-^63}")

        for title, entry in zip(header, first_entry):
            tables[table_name].append(title)
            recommanded_type = get_recommanded_type(entry)
            inputed_type = get_inputed_type(title, recommanded_type)
        
            request += title + " " + inputed_type + ", "

        primary_keys = tuple(input("Entrez les clés primaires (séparées par ',') : ").split(","))
        primary_keys_tables[table_name] = primary_keys
        request += f"PRIMARY KEY ({', '.join(primary_keys)})"

        tables_requests[table_name] = request


# Add foreign keys
for table in tables.keys():
    print(f"\nPour la table {table}...")
    print(f"Rappel des colonnes : {', '.join(tables[table])}\n")
    foreign_keys = tuple(input("Entrez les clés étrangères (séparées par ',') : ").split(","))

    if foreign_keys == ("",):
        tables_without_fk.append(table)
        tables_requests[table] += ");"
        continue

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

print("\nAjouts des valeus ...\n")

# Add all data
for path in paths:
    with open(path, "r", encoding="utf8") as file:
        table_name = get_table_name(path)
        print("Table : " + table_name + "...")
        values = list(map(process_entry, file.readlines()[1:]))
        value_count = len(values[0])

        cursor.executemany("INSERT INTO " + table_name + " VALUES (" + ", ".join(["?"] * value_count) + ")", values)

cursor.close()
db.close()