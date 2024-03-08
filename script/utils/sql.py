"""
Module that contains functions to create SQL table.
"""


import sys
import os
import re
from typing import TextIO


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


def get_table_name(path: str) -> str:
    """
    Get table name based on given CSV path.
    :param: path - The CSV path
    :return: The table name in all caps.
    """
    return (path.split("/")[-1]).split(".")[0].upper()


def __process_header(header: str) -> str:
    """
    Process header string, private helper function.
    :param: header - The raw header string
    :return: The header string with only the columns names and commas.
    """
    return header.replace(",", "").replace("(", "").replace(")", "").replace("'", "")


def get_header(file: TextIO) -> list[str]:
    """
    Get raw table header and entries.
    :param: file - The file stream
    :return: Header and entries
    """
    header = file.readline()

    header = "".join(list(map(__process_header, header)))[1:-2]
    header = header.split('""')

    return header


def get_recommanded_type(entry: str) -> str:
    """
    Get recommanded type based on given entry.
    If no type can be found, return "-".
    :param: entry - The column information
    :return: The recommanded type
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
    :param: title - The column name
    :param: recommanded_type - The type found by script
    :return: The inputed type
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
    :param: tables - All tables
    :param: primary_keys - The table name -> PK map
    :param: key - The foreign key
    :return: The table
    """
    while True:
        fk_table = input(f"Entrez la table associée à {key} : ")

        if fk_table in tables.keys() and len(primary_keys[fk_table]) == 1:
            break

        print("Table non existante ou ne contenant pas une clé étrangère simple.")
    
    return fk_table


def process_entry(row: str) -> list[str]:
    """
    Parse CSV row string.
    The csv module could have been used, but I like to recreate the wheel.
    :param: row - The row string
    :return: Row information.
    """
    row = row.replace("\r", "").replace("\n", "")

    information = []
    current = ""
    i = 0
    in_quote = False

    while i < len(row):
        if not in_quote and row[i] == ",":
            information.append(current)
            current = ""
            i += 1
            continue
        if row[i] == '"':
            in_quote = not in_quote
            i += 1
            continue
        current += row[i]
        i += 1

    information.append(current)
    return information
