from Travel_Records01.BackEnd.Database.ConnectDatabase import ConnectDatabase


class DeleteTravelRecord:
    """
    Handle deletion of travel records
    """

    def __init__(self):
        self.db = ConnectDatabase()

    # =========================
    # CHECK OWNERSHIP
    # =========================
    def check_ownership(self, user_id, travel_record_id):
        """
        Ensure the user owns the travel record
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
    # DELETE TRAVEL RECORD
    # =========================
    def delete_travel_record(self, user_id, travel_record_id):
        """
        Delete travel record safely
        """

        # ① 所有者チェック
        if not self.check_ownership(user_id, travel_record_id):
            return False, "Unauthorized or record not found"

        conn = self.db.connect()
        if conn is None:
            return False, "Database connection failed"

        cursor = conn.cursor()

        try:
            query = """
            DELETE FROM travel_records
            WHERE id=%s
            """

            cursor.execute(query, (travel_record_id,))
            conn.commit()

        except Exception as e:
            return False, f"Error: {e}"

        finally:
            cursor.close()
            self.db.disconnect()

        return True, "Travel record deleted successfully"