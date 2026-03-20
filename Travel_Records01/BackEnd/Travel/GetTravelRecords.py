from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class GetTravelRecords:
    """
    Handle fetching travel records and related data
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # GET ALL TRAVEL RECORDS
    # =========================
    def get_all_travel_records(self, user_id):
        """
        Get all travel records for a user
        """

        conn = self.db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM travel_records
            WHERE user_id=%s
            ORDER BY start_date DESC
            """
            cursor.execute(query, (user_id,))
            records = cursor.fetchall()

            return records

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            cursor.close()
            self.db.disconnect()

    # =========================
    # GET SINGLE TRAVEL RECORD
    # =========================
    def get_travel_record(self, travel_record_id):
        """
        Get a single travel record
        """

        conn = self.db.connect()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM travel_records
            WHERE id=%s
            """
            cursor.execute(query, (travel_record_id,))
            record = cursor.fetchone()

            return record

        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            self.db.disconnect()

    # =========================
    # GET TRAVEL DAYS
    # =========================
    def get_travel_days(self, travel_record_id):
        """
        Get all days for a travel record
        """

        conn = self.db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM travel_days
            WHERE travel_record_id=%s
            ORDER BY day_date ASC
            """
            cursor.execute(query, (travel_record_id,))
            days = cursor.fetchall()

            return days

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            cursor.close()
            self.db.disconnect()

    # =========================
    # GET FULL TRAVEL DETAIL
    # =========================
    def get_full_travel_detail(self, travel_record_id):
        """
        Get travel record + all daily logs
        """

        record = self.get_travel_record(travel_record_id)
        if not record:
            return None

        days = self.get_travel_days(travel_record_id)

        return {
            "travel": record,
            "days": days
        }