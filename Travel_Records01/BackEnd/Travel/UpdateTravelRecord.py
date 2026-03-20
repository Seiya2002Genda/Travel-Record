from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class UpdateTravelRecord:
    """
    Handle updating travel records
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # CHECK OWNERSHIP
    # =========================
    def check_ownership(self, user_id, travel_record_id):
        """
        Ensure the user owns the record
        """

        conn = self.db.connect()
        if conn is None:
            return False

        cursor = conn.cursor()

        query = """
        SELECT id FROM travel_records
        WHERE id=%s AND user_id=%s
        """

        cursor.execute(query, (travel_record_id, user_id))
        result = cursor.fetchone()

        cursor.close()
        self.db.disconnect()

        return result is not None

    # =========================
    # VALIDATION
    # =========================
    def validate_input(self, destination, start_date, end_date, purpose, total_cost):
        """
        Validate input fields
        """

        if not destination or not destination.strip():
            return False, "Destination is required"

        if not start_date or not end_date:
            return False, "Start and end dates are required"

        if str(start_date) > str(end_date):
            return False, "Invalid date range"

        if not purpose or not purpose.strip():
            return False, "Purpose is required"

        try:
            if total_cost in [None, ""]:
                total_cost = 0.00
            else:
                total_cost = float(total_cost)

            if total_cost < 0:
                return False, "Cost cannot be negative"

        except ValueError:
            return False, "Invalid cost value"

        return True, "Valid input"

    # =========================
    # UPDATE TRAVEL RECORD
    # =========================
    def update_travel_record(
        self,
        user_id,
        travel_record_id,
        destination,
        start_date,
        end_date,
        purpose,
        impression="",
        total_cost=0.00
    ):
        """
        Update travel record
        """

        # ① ownership check
        if not self.check_ownership(user_id, travel_record_id):
            return False, "Unauthorized"

        # ② validation
        valid, message = self.validate_input(
            destination, start_date, end_date, purpose, total_cost
        )
        if not valid:
            return False, message

        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            UPDATE travel_records
            SET destination=%s,
                start_date=%s,
                end_date=%s,
                purpose=%s,
                impression=%s,
                total_cost=%s
            WHERE id=%s
            """

            cursor.execute(query, (
                destination.strip(),
                start_date,
                end_date,
                purpose.strip(),
                impression.strip() if impression else "",
                float(total_cost) if total_cost not in [None, ""] else 0.00,
                travel_record_id
            ))

            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Travel record updated successfully"