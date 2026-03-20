import mysql.connector
from mysql.connector import Error
from Travel_Records01.BackEnd.Database.Config import Config


class CreateDatabase:
    """
    Create the database and all required tables
    for the Travel Records application.
    """

    def __init__(self):
        self.config = Config.get_db_config()

    # =========================
    # DATABASE
    # =========================
    def create_database(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"]
            )
            cursor = connection.cursor()

            database_name = self.config["database"]
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"Database '{database_name}' ready.")

        except Error as e:
            print(f"Error creating database: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # =========================
    # USERS TABLE
    # =========================
    def create_users_table(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            cursor.execute(query)
            connection.commit()
            print("users table ready.")

        except Error as e:
            print(f"Error creating users table: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # =========================
    # TRAVEL RECORDS TABLE
    # =========================
    def create_travel_records_table(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS travel_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                destination VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                purpose VARCHAR(255) NOT NULL,
                impression TEXT,
                total_cost DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
            """

            cursor.execute(query)
            connection.commit()
            print("travel_records table ready.")

        except Error as e:
            print(f"Error creating travel_records: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # =========================
    # TRAVEL DAYS TABLE
    # =========================
    def create_travel_days_table(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS travel_days (
                id INT AUTO_INCREMENT PRIMARY KEY,
                travel_record_id INT NOT NULL,
                day_date DATE NOT NULL,
                day_destination VARCHAR(255) NOT NULL,
                activities TEXT,
                day_impression TEXT,
                day_cost DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (travel_record_id) REFERENCES travel_records(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
            """

            cursor.execute(query)
            connection.commit()
            print("travel_days table ready.")

        except Error as e:
            print(f"Error creating travel_days: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # =========================
    # OTP TABLE (重要)
    # =========================
    def create_otp_table(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS otp_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                otp_code VARCHAR(10) NOT NULL,
                expiry DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(email),
                INDEX(email),
                FOREIGN KEY (email) REFERENCES users(email)
                    ON DELETE CASCADE
            )
            """

            cursor.execute(query)
            connection.commit()
            print("otp_codes table ready.")

        except Error as e:
            print(f"Error creating otp_codes: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # =========================
    # INITIALIZE ALL
    # =========================
    def initialize(self):
        self.create_database()
        self.create_users_table()
        self.create_travel_records_table()
        self.create_travel_days_table()
        self.create_otp_table()

        print("All tables initialized successfully.")