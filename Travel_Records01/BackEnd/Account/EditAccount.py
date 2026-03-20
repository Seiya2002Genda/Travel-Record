from werkzeug.security import generate_password_hash
from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class EditAccount:
    """
    Handle editing user account information
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # GET USER INFO
    # =========================
    def get_user(self, user_id):
        conn = self.db.connect()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT id, username, first_name, last_name, email FROM users WHERE id=%s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user

        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            self.db.disconnect()

    # =========================
    # UPDATE USER INFO
    # =========================
    def update_user(self, user_id, username, first_name, last_name, email):
        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            UPDATE users
            SET username=%s,
                first_name=%s,
                last_name=%s,
                email=%s
            WHERE id=%s
            """

            cursor.execute(query, (
                username.strip(),
                first_name.strip(),
                last_name.strip(),
                email.strip(),
                user_id
            ))

            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Account updated successfully"

    # =========================
    # CHANGE PASSWORD
    # =========================
    def change_password(self, user_id, new_password):
        if not new_password or len(new_password) < 6:
            return False, "Password must be at least 6 characters"

        hashed = generate_password_hash(new_password)

        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            UPDATE users
            SET password=%s
            WHERE id=%s
            """

            cursor.execute(query, (hashed, user_id))
            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Password updated successfully"