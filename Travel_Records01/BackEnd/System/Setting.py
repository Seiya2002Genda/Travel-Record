class Setting:
    """
    Application settings manager
    (Can be expanded later for DB-based settings)
    """

    def __init__(self):
        # 今は簡易設定（後でDB化できる）
        self.settings = {
            "app_name": "Travel Records",
            "version": "1.0.0",
            "max_travel_days": 365,
            "currency": "USD",
            "date_format": "YYYY-MM-DD"
        }

    # =========================
    # GET ALL SETTINGS
    # =========================
    def get_all_settings(self):
        return self.settings

    # =========================
    # GET SINGLE SETTING
    # =========================
    def get_setting(self, key):
        return self.settings.get(key, None)

    # =========================
    # UPDATE SETTING（将来用）
    # =========================
    def update_setting(self, key, value):
        if key not in self.settings:
            return False, "Invalid setting key"

        self.settings[key] = value
        return True, "Setting updated"