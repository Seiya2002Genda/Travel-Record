from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class AddTravelDay:
    """
    Handle adding daily travel records
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # VALIDATION
    # =========================
    def validate_input(self, travel_record_id, day_date, day_destination, day_cost):
        """
        Validate input data
        """

        if not travel_record_id:
            return False, "Travel record ID is required."

        if not day_date:
            return False, "Date is required."

        if not day_destination or not day_destination.strip():
            return False, "Destination is required."

        try:
            if day_cost in [None, ""]:
                day_cost = 0.00
            else:
                day_cost = float(day_cost)

            if day_cost < 0:
                return False, "Cost cannot be negative."

        except ValueError:
            return False, "Cost must be a valid number."

        return True, "Valid input"

    # =========================
    # CHECK DUPLICATE DATE
    # =========================
    def check_duplicate_day(self, travel_record_id, day_date):
        """
        Prevent duplicate entries for same day
        """

        conn = self.db.connect()
        if conn is None:
            return True, "Database connection failed"

        cursor = conn.cursor()

        query = """
        SELECT id FROM travel_days
        WHERE travel_record_id=%s AND day_date=%s
        """

        cursor.execute(query, (travel_record_id, day_date))
        result = cursor.fetchone()

        cursor.close()
        self.db.disconnect()

        if result:
            return True, "This date is already registered."

        return False, "OK"

    # =========================
    # ADD TRAVEL DAY
    # =========================
    def add_travel_day(
        self,
        travel_record_id,
        day_date,
        day_destination,
        activities="",
        day_impression="",
        day_cost=0.00
    ):
        """
        Add a daily travel record
        """

        # ① Validation
        valid, message = self.validate_input(
            travel_record_id,
            day_date,
            day_destination,
            day_cost
        )
        if not valid:
            return False, message

        # ② Duplicate check
        is_duplicate, message = self.check_duplicate_day(
            travel_record_id,
            day_date
        )
        if is_duplicate:
            return False, message

        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            INSERT INTO travel_days
            (travel_record_id, day_date, day_destination, activities, day_impression, day_cost)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                travel_record_id,
                day_date,
                day_destination.strip(),
                activities.strip() if activities else "",
                day_impression.strip() if day_impression else "",
                float(day_cost) if day_cost not in [None, ""] else 0.00
            ))

            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Travel day added successfully"