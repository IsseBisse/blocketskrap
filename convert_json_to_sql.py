import json
import sys

from DatabaseHandler import DatabaseHandler, DEFAULT_CONFIG

def read_json(path):
    print(f"Opening {path}...")
    with open(path) as file:
        text = file.read()
        json_data = json.loads(text)
        print("JSON data read successfully!")
    return json_data

def connect_to_db():
    print("Connecting to db... ", end="")
    db_handler = DatabaseHandler({**DEFAULT_CONFIG, "database": "vehicle_ad_db"})
    db_handler.connect()
    print("Done!")

    return db_handler

def insert_to_database(db_handler, json_data):
    print(f"Inserting {len(json_data)} items into database...")

    print("Done!")

def main(path):
    json_data = read_json(path)
    db_handler = connect_to_db()

    insert_to_database(db_handler, json_data)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])

    else:
        print("Incorrect number of arguments!")