import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase
from Travel_Records01.BackEnd.Database.Config import Config


class ForgetPassword:

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # OTP GENERATE
    # =========================
    def generate_otp(self):
        return str(random.randint(100000, 999999))

    # =========================
    # SEND EMAIL
    # =========================
    def send_email(self, to_email, otp):

        try:
            msg = MIMEText(f"Your OTP code is: {otp}")
            msg["Subject"] = "Password Reset OTP"
            msg["From"] = Config.EMAIL_ADDRESS
            msg["To"] = to_email

            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                server.send_message(msg)

            return True, "OTP sent successfully"

        except Exception as e:
            print("EMAIL ERROR:", e)
            return False, "Failed to send email"

    # =========================
    # SEND OTP
    # =========================
    def send_otp(self, email):

        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        # check user exists
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return False, "Email not registered"

        otp = self.generate_otp()
        expiry = datetime.now() + timedelta(minutes=5)

        # delete old OTP
        cursor.execute("DELETE FROM otp_codes WHERE email=%s", (email,))

        # insert new OTP
        cursor.execute("""
            INSERT INTO otp_codes (email, otp_code, expiry)
            VALUES (%s, %s, %s)
        """, (email, otp, expiry))

        conn.commit()
        cursor.close()
        conn.close()

        return self.send_email(email, otp)

    # =========================
    # VERIFY OTP
    # =========================
    def verify_otp(self, email, otp):

        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM otp_codes
            WHERE email=%s AND otp_code=%s
        """, (email, otp))

        record = cursor.fetchone()

        if not record:
            cursor.close()
            conn.close()
            return False, "Invalid OTP"

        if datetime.now() > record["expiry"]:
            cursor.close()
            conn.close()
            return False, "OTP expired"

        cursor.close()
        conn.close()

        return True, "OTP verified"

    # =========================
    # RESET PASSWORD
    # =========================
    def reset_password(self, email, new_password):

        conn = self.db.connect()
        cursor = conn.cursor()

        # hash password
        import hashlib
        hashed = hashlib.sha256(new_password.encode()).hexdigest()

        cursor.execute("""
            UPDATE users SET password=%s WHERE email=%s
        """, (hashed, email))

        # delete OTP after use
        cursor.execute("DELETE FROM otp_codes WHERE email=%s", (email,))

        conn.commit()
        cursor.close()
        conn.close()

        return True, "Password reset successful"