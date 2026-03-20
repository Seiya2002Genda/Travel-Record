from werkzeug.security import check_password_hash
from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class Login:
    """
    Handle user login authentication
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # LOGIN PROCESS
    # =========================
    def login_user(self, username, password):
        """
        Authenticate user
        """

        # ① 入力チェック
        if not username or not password:
            return False, "Username and password are required", None

        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed", None

        cursor = conn.cursor(dictionary=True)

        try:
            # ② ユーザー取得
            query = "SELECT * FROM users WHERE username=%s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            # ③ ユーザー存在チェック
            if not user:
                return False, "Invalid username", None

            # ④ パスワード照合（ここが最重要）
            if not check_password_hash(user["password"], password):
                return False, "Invalid password", None

            # ⑤ 成功（セッション用データ返す）
            user_data = {
                "id": user["id"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"]
            }

            return True, "Login successful", user_data

        except Exception as e:
            return False, f"Error: {e}", None

        finally:
            cursor.close()
            self.db.disconnect()