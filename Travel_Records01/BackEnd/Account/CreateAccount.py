import re
from werkzeug.security import generate_password_hash
from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class CreateAccount:
    """
    Handle user account creation (Signup)
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # VALIDATION
    # =========================
    def validate_input(self, username, first_name, last_name, email, password):
        """
        Validate user input
        """

        if not all([username, first_name, last_name, email, password]):
            return False, "All fields are required."

        if len(username) < 3:
            return False, "Username must be at least 3 characters."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format."

        if len(password) < 6:
            return False, "Password must be at least 6 characters."

        return True, "Valid input"

    # =========================
    # CHECK DUPLICATE
    # =========================
    def check_duplicate_user(self, username, email):
        """
        Check if username or email already exists
        """
        conn = self.db.connect()
        if conn is None:
            return True, "Database connection failed"

        cursor = conn.cursor()

        query = "SELECT id FROM users WHERE username=%s OR email=%s"
        cursor.execute(query, (username, email))

        result = cursor.fetchone()

        cursor.close()
        self.db.disconnect()

        if result:
            return True, "Username or Email already exists"

        return False, "OK"

    # =========================
    # HASH PASSWORD
    # =========================
    def hash_password(self, password):
        """
        Hash password securely
        """
        return generate_password_hash(password)

    # =========================
    # CREATE ACCOUNT
    # =========================
    def create_account(self, username, first_name, last_name, email, password):
        """
        Main function to create user account
        """

        # ① Validation
        valid, message = self.validate_input(
            username, first_name, last_name, email, password
        )
        if not valid:
            return False, message

        # ② Duplicate check
        is_duplicate, message = self.check_duplicate_user(username, email)
        if is_duplicate:
            return False, message

        # ③ Hash password
        hashed_password = self.hash_password(password)

        # ④ Insert into DB
        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            INSERT INTO users (username, first_name, last_name, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                username,
                first_name,
                last_name,
                email,
                hashed_password
            ))

            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Account created successfully"