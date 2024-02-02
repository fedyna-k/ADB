import sqlite3
import sys
import os
import re


# Guard closes
if __name__ != "__main__":
    raise ImportError("This script must be launched as main.")

if sys.argv[1] == "--help":
    print("Usage : python3 table_creator.py <database> <csv file|dir> [...<csv file|dir>]")
    exit(0)

if len(sys.argv) < 3:
    raise SyntaxError("Please use correct syntax.\nFor further help, type : python3 table_creator.py --help")


# Add all files paths
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

# Helper function
process_header = lambda e: e.replace(",", "").replace("(", "").replace(")", "").replace("'", "")
process_entry = lambda e: e.split(",")

def get_recommanded_type(entry):
    if entry == "":
        return "-"
    
    if re.match("[0-9]*\.[0-9]+", entry):
        return "REAL"

    if re.match("[0-9]+", entry):
        return "INT"
    
    return "TEXT"


# Connect to data-base
db = sqlite3.connect(sys.argv[1] + ".db")
cursor = db.cursor()

print(f"{' Createur de table ':-^63}")
print("\nPour valider le type proposé, appuyez sur ENTRER, sinon entrez un nouveau type.")
print("Si un type n'a pas pu être déterminé à partir de la base, il faut le renseigner.")

for path in paths:
    with open(path, "r", encoding="utf8") as file:
        table_name = (path.split("/")[-1]).split(".")[0]
        header, *entries = file.readlines()

        header = "".join(list(map(process_header, header)))[1:-2]
        header = header.split('""')

        first_entry = process_entry(entries[0])
        
        request = "("

        print(f"\n{' ' + table_name + ' ':=^63}\n")

        print(f"{'Argument name':^20}|{'Recommanded type':^20}|{'Entered type':^20}")
        print(f"{'':-^63}")
        for title, entry in zip(header, first_entry):
            recommanded_type = get_recommanded_type(entry)

            while True:
                print(f"{title:^20}|{recommanded_type:^20}| ", end="")
                inputed_type = input("")
                if inputed_type == "":
                    inputed_type = recommanded_type

                if inputed_type != "-" and inputed_type in ["INT", "TEXT", "REAL"]:
                    break

            request += title + " " + inputed_type + ", "

        primary_keys = tuple(input("Entrez les clés primaires (séparées par ',') : ").split(","))
        
        request += f"PRIMARY KEY ({', '.join(primary_keys)}));"

        cursor.execute("CREATE TABLE " + table_name + request)
        