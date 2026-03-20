from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class CreateTravelRecord:
    """
    Handle creation of overall travel records.
    """

    def __init__(self):
        self.db = ConnectDatabase()

    def validate_input(self, user_id, destination, start_date, end_date, purpose, total_cost):
        """
        Validate travel record input.
        """
        if not user_id:
            return False, "User ID is required."

        if not destination or not destination.strip():
            return False, "Destination is required."

        if not start_date:
            return False, "Start date is required."

        if not end_date:
            return False, "End date is required."

        if not purpose or not purpose.strip():
            return False, "Purpose is required."

        try:
            if total_cost in [None, ""]:
                total_cost = 0.00
            else:
                total_cost = float(total_cost)

            if total_cost < 0:
                return False, "Total cost cannot be negative."

        except ValueError:
            return False, "Total cost must be a valid number."

        if str(start_date) > str(end_date):
            return False, "Start date cannot be later than end date."

        return True, "Valid input."

    def create_travel_record(self, user_id, destination, start_date, end_date, purpose, impression="", total_cost=0.00):
        """
        Create a new travel record.
        """
        is_valid, message = self.validate_input(
            user_id, destination, start_date, end_date, purpose, total_cost
        )
        if not is_valid:
            return False, message, None

        connection = self.db.connect()
        if connection is None:
            return False, "Database connection failed.", None

        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO travel_records
            (user_id, destination, start_date, end_date, purpose, impression, total_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    user_id,
                    destination.strip(),
                    start_date,
                    end_date,
                    purpose.strip(),
                    impression.strip() if impression else "",
                    float(total_cost) if total_cost not in [None, ""] else 0.00
                )
            )
            connection.commit()

            travel_record_id = cursor.lastrowid
            return True, "Travel record created successfully.", travel_record_id

        except Exception as e:
            return False, f"Error while creating travel record: {e}", None

        finally:
            cursor.close()
            self.db.disconnect()