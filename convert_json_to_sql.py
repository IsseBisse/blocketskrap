from difflib import Match
import json
import re
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
    db_handler = DatabaseHandler({**DEFAULT_CONFIG, "database": "vehicle_ad_db"})
    db_handler.connect()

    return db_handler

def json_to_db_dict(json_item):
    # Add matching key-value-pairs
    db_dict = {key: json_item[key] if key in json_item else None for key in ["url", "heading", "price", "location", "description"]}

    # Manually add other key-value-pairs
    db_dict["ad_id"] = json_item["id"]

    general_info_patterns = {
        "fuel_type": (r"Bränsle([^ ]+)", None),
        "is_automatic": (r"Växellåda([^ ]+)", lambda string: string == "Automat"),
        "mileage": (r"Miltal([0-9 \-]+)", lambda string: int(string.split("-")[1].replace(" ", ""))),
        "model_year": (r"Modellår([0-9]+)", lambda string: int(string)),
        "body_type": (r"Biltyp([^ ]+)", None),
        "horsepower": (r"Hästkrafter([0-9]+)", lambda string: int(string)),
        "color": (r"Färg([^ ]+)", None),
        }

    if "general" in json_item:
        for key, value in general_info_patterns.items():
            pattern, transformer = value
            match = re.findall(pattern, json_item["general"])

            if match:
                if transformer is not None:
                    value = transformer(match[0])

                else:
                    value = match[0]

                db_dict[key] = value

    return db_dict

def insert_to_database(db_handler, json_data):
    print(f"Inserting {len(json_data)} items into database...")
    for item in json_data:
        db_dict = json_to_db_dict(item)
        db_handler.insert_vehicle_ad(db_dict)

    print("Done!")

def main(path):
    json_data = read_json(path)
    db_handler = connect_to_db()

    insert_to_database(db_handler, json_data)

if __name__ == '__main__':
    path = "data/v70__hela_sverige__post2008.json"
    main(path)
    
    """
    if len(sys.argv) == 2:
        main(sys.argv[1])

    else:
        print("Incorrect number of arguments!")
    """