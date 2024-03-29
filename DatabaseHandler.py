import mysql.connector
from mysql.connector import errorcode

DEFAULT_CONFIG = {
    'host':'mysql-server-testing.mysql.database.azure.com',
    'user':'testingonazure@mysql-server-testing',
    'password':'Quickdraw1',
    'port': 3306,
    #'client_flags': [mysql.connector.ClientFlag.SSL],
    #'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem',
    #'ssl_verify_cert': False,
    'connection_timeout': 10,
    'use_pure': True
    }

class ServerHandler:

    def __init__(self, config=None):
        if config is not None:
            self.config = config

        else:
            self.config = DEFAULT_CONFIG

    def __str__(self):
        self.cursor.execute("SHOW DATABASES")
        string = "Available databases:\n"
        for db in self.cursor.fetchall():
            string += f"{db[0]}\n"

        return string


    """
    CONNECTION
    """
    def connect(self):
        try:
            print("Connecting to server...")
            conn = mysql.connector.connect(**self.config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = conn.cursor()
            self.conn = conn

    def disconnect(self):
        self.cursor.close()
        self.conn.close()
        print("Connection closed")

    """
    DATABASE
    """
    def create_database(self, name):
        self.cursor.execute(f"CREATE DATABASE {name}")

    def delete_database(self, name):
        self.cursor.execute(f"DROP DATABASE {name}")
    
    def get_databases(self):
        self.cursor.execute("SHOW DATABASES")
        return [item[0] for item in self.cursor.fetchall()]

class DatabaseHandler():

    def __init__(self, config=None):
        if config is not None:
            self.config = config

        else:
            self.config = DEFAULT_CONFIG

    def __str__(self):
        self.cursor.execute("SHOW TABLES")
        string = "Available tables:\n"
        for table in self.cursor.fetchall():
            table_name = table[0]
            string += f"{table_name}\n"
            
            string += "Columns:\n"
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            for col in self.cursor.fetchall():
                string += f"{col[0]}\n"

            string += "\n"

        return string 

    def connect(self):
        try:
            print("Connecting to database...")
            conn = mysql.connector.connect(**self.config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = conn.cursor()
            self.conn = conn

    def disconnect(self):
        self.cursor.close()
        self.conn.close()
        print("Connection closed")

    """
    TABLE
    """
    def create_table(self, name, columns):
        columns_string = ", ".join(columns)
        self.cursor.execute(f"CREATE TABLE {name} ({columns_string})")

    def drop_table(self, name):
        self.cursor.execute(f"DROP TABLE {name}")

    def get_tables(self):
        self.cursor.execute("SHOW TABLES")
        return [item[0] for item in self.cursor.fetchall()]
    
    """
    VEHICLE TYPES
    """
    def add_vehicle_type(self, engine_type, horsepower): 
        self.cursor.execute("INSERT INTO vehicle_types (engine_type, horsepower) VALUES (%s, %s)", (engine_type, horsepower))
        self.conn.commit()

def setup():
    # Setup server
    EXPECTED_DBS = ["vehicle_ad_db"]

    server_handler = ServerHandler()
    server_handler.connect()
    
    available_databases = server_handler.get_databases()
    print(available_databases)

    for expected_db in EXPECTED_DBS:
        if expected_db not in available_databases:
            server_handler.create_database(expected_db)
    
    server_handler.disconnect()
    
    # Setup tables
    EXPECTED_TABLES = [("vehicle_types", 
                            ["id INT AUTO_INCREMENT PRIMARY KEY",
                            "engine_type VARCHAR(8) NOT NULL",
                            "horsepower SMALLINT"]),
                        ("ads",
                            ["id INT AUTO_INCREMENT PRIMARY KEY",
                            "vehicle_id INT",
                            "FOREIGN KEY(vehicle_id) REFERENCES vehicle_types(id)",
                            "description MEDIUMTEXT"])]

    db_handler = DatabaseHandler({**DEFAULT_CONFIG, "database": "vehicle_ad_db"})
    db_handler.connect()
    
    available_tables = db_handler.get_tables()
    for expected_table_name, columns in EXPECTED_TABLES:
        if expected_table_name not in available_tables:
            db_handler.create_table(expected_table_name, columns)

    print(db_handler)

    db_handler.disconnect()

def add_dummy_data():
    db_handler = DatabaseHandler({**DEFAULT_CONFIG, "database": "vehicle_ad_db"})
    db_handler.connect()
    
    db_handler.add_vehicle_type("D4", 163)


if __name__ == '__main__':
    setup
    add_dummy_data()

    
