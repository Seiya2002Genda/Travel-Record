import mysql.connector
from mysql.connector import Error
from Travel_Records01.BackEnd.Database.Config import Config


class ConnectDatabase:
    """
    Database connection handler
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Create DB connection
        """
        try:
            db_config = Config.get_db_config()

            self.connection = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"]
            )

            if self.connection.is_connected():
                print("✅ Database connected successfully")
                return self.connection

        except Error as e:
            print(f"❌ Database connection failed: {e}")
            return None

    def disconnect(self):
        """
        Close DB connection safely
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Database connection closed")