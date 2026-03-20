from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from Travel_Records01.BackEnd.Database.Config import Config
from Travel_Records01.BackEnd.Database.CreateDatabase import CreateDatabase

from Travel_Records01.BackEnd.Account.CreateAccount import CreateAccount
from Travel_Records01.BackEnd.Account.Login import Login
from Travel_Records01.BackEnd.Account.EditAccount import EditAccount
from Travel_Records01.BackEnd.Account.ForgetPassword import ForgetPassword

from Travel_Records01.BackEnd.Travel.CreateTravelRecord import CreateTravelRecord
from Travel_Records01.BackEnd.Travel.AddTravelDay import AddTravelDay
from Travel_Records01.BackEnd.Travel.GetTravelRecords import GetTravelRecords
from Travel_Records01.BackEnd.Travel.UpdateTravelRecord import UpdateTravelRecord
from Travel_Records01.BackEnd.Travel.DeleteTravelRecord import DeleteTravelRecord

from Travel_Records01.BackEnd.System.Setting import Setting


app = Flask(
    __name__,
    template_folder="FrontEnd/templates",
    static_folder="FrontEnd/static"
)
app.secret_key = Config.SECRET_KEY


# =========================
# DATABASE INITIALIZATION
# =========================
def initialize_database():
    """
    Create database and required tables on app startup.
    """
    try:
        creator = CreateDatabase()
        creator.initialize()
        print("Database initialization completed.")
    except Exception as e:
        print(f"Database initialization error: {e}")


initialize_database()


# =========================
# HELPER
# =========================
def is_logged_in():
    return "user_id" in session


def require_login_json():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    return None


# =========================
# PAGE ROUTES
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    creator = CreateAccount()
    success, message = creator.create_account(
        data.get("username", ""),
        data.get("first_name", ""),
        data.get("last_name", ""),
        data.get("email", ""),
        data.get("password", "")
    )

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    auth = Login()
    success, message, user = auth.login_user(
        data.get("username", ""),
        data.get("password", "")
    )

    if success:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]
        session["email"] = user["email"]

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/TravelRecord")
def travel_record_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    return render_template("TravelRecord.html")


@app.route("/forget_password")
def forget_password():
    return render_template("forget_password.html")


@app.route("/setting")
def setting():
    if not is_logged_in():
        return redirect(url_for("login"))

    account_editor = EditAccount()
    user = account_editor.get_user(session["user_id"])

    app_setting = Setting()
    settings_data = app_setting.get_all_settings()

    return render_template(
        "setting.html",
        user=user,
        settings=settings_data
    )


# =========================
# ACCOUNT API
# =========================
@app.route("/api/account", methods=["GET"])
def get_account():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    editor = EditAccount()
    user = editor.get_user(session["user_id"])

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify({
        "success": True,
        "user": user
    })


@app.route("/api/account", methods=["PUT"])
def update_account():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    editor = EditAccount()
    success, message = editor.update_user(
        session["user_id"],
        data.get("username", ""),
        data.get("first_name", ""),
        data.get("last_name", ""),
        data.get("email", "")
    )

    if success:
        session["username"] = data.get("username", session.get("username"))
        session["first_name"] = data.get("first_name", session.get("first_name"))
        session["last_name"] = data.get("last_name", session.get("last_name"))
        session["email"] = data.get("email", session.get("email"))

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/api/account/password", methods=["PUT"])
def change_password():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    editor = EditAccount()
    success, message = editor.change_password(
        session["user_id"],
        data.get("new_password", "")
    )

    return jsonify({
        "success": success,
        "message": message
    })


# =========================
# SETTING API
# =========================
@app.route("/api/settings", methods=["GET"])
def get_settings():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    setting_manager = Setting()
    return jsonify({
        "success": True,
        "settings": setting_manager.get_all_settings()
    })


# =========================
# TRAVEL API
# =========================
@app.route("/api/travels", methods=["GET"])
def get_travels():
    auth_check = require_login_json()
    if auth_check:
        return []

    getter = GetTravelRecords()
    records = getter.get_all_travel_records(session["user_id"])
    return jsonify(records)


@app.route("/api/travel", methods=["POST"])
def create_travel():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    creator = CreateTravelRecord()
    success, message, travel_record_id = creator.create_travel_record(
        session["user_id"],
        data.get("destination", ""),
        data.get("start_date", ""),
        data.get("end_date", ""),
        data.get("purpose", ""),
        data.get("impression", ""),
        data.get("total_cost", 0.00)
    )

    return jsonify({
        "success": success,
        "message": message,
        "id": travel_record_id
    })


@app.route("/api/travel/<int:travel_id>", methods=["GET"])
def get_travel(travel_id):
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    getter = GetTravelRecords()
    data = getter.get_full_travel_detail(travel_id)

    if not data:
        return jsonify({"success": False, "message": "Travel record not found"}), 404

    record = data.get("travel")
    if not record or record.get("user_id") != session["user_id"]:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    return jsonify(data)


@app.route("/api/travel/<int:travel_id>", methods=["PUT"])
def update_travel(travel_id):
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    updater = UpdateTravelRecord()
    success, message = updater.update_travel_record(
        session["user_id"],
        travel_id,
        data.get("destination", ""),
        data.get("start_date", ""),
        data.get("end_date", ""),
        data.get("purpose", ""),
        data.get("impression", ""),
        data.get("total_cost", 0.00)
    )

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/api/travel/<int:travel_id>", methods=["DELETE"])
def delete_travel(travel_id):
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    deleter = DeleteTravelRecord()
    success, message = deleter.delete_travel_record(
        session["user_id"],
        travel_id
    )

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/api/travel/day", methods=["POST"])
def add_travel_day():
    auth_check = require_login_json()
    if auth_check:
        return auth_check

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    adder = AddTravelDay()
    success, message = adder.add_travel_day(
        data.get("travel_id", ""),
        data.get("day_date", ""),
        data.get("day_destination", ""),
        data.get("activities", ""),
        data.get("day_impression", ""),
        data.get("day_cost", 0.00)
    )

    return jsonify({
        "success": success,
        "message": message
    })


# =========================
# FORGET PASSWORD API
# =========================
@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    fp = ForgetPassword()
    success, message = fp.send_otp(data.get("email", ""))

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    fp = ForgetPassword()
    success, message = fp.verify_otp(
        data.get("email", ""),
        data.get("otp", "")
    )

    return jsonify({
        "success": success,
        "message": message
    })


@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request body"}), 400

    fp = ForgetPassword()
    success, message = fp.reset_password(
        data.get("email", ""),
        data.get("password", "")
    )

    return jsonify({
        "success": success,
        "message": message
    })


# =========================
# DEBUG SESSION API
# =========================
@app.route("/api/session", methods=["GET"])
def get_session_info():
    if not is_logged_in():
        return jsonify({
            "logged_in": False
        })

    return jsonify({
        "logged_in": True,
        "user_id": session.get("user_id"),
        "username": session.get("username"),
        "email": session.get("email")
    })


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)