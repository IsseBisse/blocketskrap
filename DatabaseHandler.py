import mysql.connector
from mysql.connector import errorcode

class DatabaseHandler:

    default_config = {
        'host':'mysql-server-testing.mysql.database.azure.com',
        'user':'testingonazure@mysql-server-testing'
        'password':'Quickdraw1',
        'database':'<mydatabase>',
        'client_flags': [mysql.connector.ClientFlag.SSL],
        'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
        }

    def __init__(self, config=None):
        if config is not None:
            self.config = config

        else:
            self.config = self.default_config

    def connect(self):
        try:
            conn = mysql.connector.connect(**config)
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


if __name__ == '__main__':
    db_handler = DatabaseHandler()
    db_handler.connect()
    db_handler.disconnect()

