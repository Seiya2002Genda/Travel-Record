import os

class Config:
    """
    Database configuration class
    Handles environment-based configuration
    """

    # =========================
    # BASIC CONFIG
    # =========================
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root1234")
    DB_NAME = os.getenv("DB_NAME", "travel_records")

    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

    # =========================
    # MAIL (for future OTP / reset)
    # =========================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

    @classmethod
    def get_db_config(cls):
        """
        Return DB config as dictionary
        """
        return {
            "host": cls.DB_HOST,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME
        }