# 🌍 Travel Records App

A full-stack web application for managing personal travel experiences, daily logs, and expenses.
Built with **Flask + MySQL + HTML/CSS/JavaScript**.

---

## 🚀 Features

### 🔐 Authentication

* User Signup / Login
* Session-based authentication
* Password reset via OTP (Email verification)

### 👤 Account Management

* Edit profile (username, name, email)
* Change password
* View account settings

### ✈️ Travel Records

* Create, update, delete travel records
* Store:

  * Destination
  * Date range
  * Purpose
  * Impression
  * Total cost

### 📅 Daily Travel Logs

* Add daily entries for each trip
* Track:

  * Date
  * Location
  * Activities
  * Daily impressions
  * Daily expenses

### ⚙️ System Features

* Settings API
* Session debug endpoint
* Secure database schema with foreign keys

---

## 🏗️ Project Structure

```
Travel_Records01/
│
├── app.py
│
├── BackEnd/
│   ├── Account/
│   ├── Database/
│   ├── Travel/
│   └── System/
│
├── FrontEnd/
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── TravelRecord.html
│   │   ├── setting.html
│   │   └── forget_password.html
│   │
│   └── static/
│       ├── css/
│       └── js/
```

---

## ⚙️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript
* **Authentication:** Session + OTP (Email)
* **Architecture:** Modular (Backend / Frontend separation)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/travel-records-app.git
cd travel-records-app
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure database

Edit:

```
BackEnd/Database/Config.py
```

Example:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "travel_records_db"
}
```

---

### 4. Configure email (for OTP)

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

---

### 5. Run the application

```bash
python app.py
```

---

### 6. Open in browser

```
http://127.0.0.1:5000
```

---

## 🔑 API Endpoints

### Authentication

* `POST /signup`
* `POST /login`
* `GET /logout`

### Account

* `GET /api/account`
* `PUT /api/account`
* `PUT /api/account/password`

### Travel

* `GET /api/travels`
* `POST /api/travel`
* `GET /api/travel/<id>`
* `PUT /api/travel/<id>`
* `DELETE /api/travel/<id>`

### Travel Days

* `POST /api/travel/day`

### Password Reset

* `POST /api/send-otp`
* `POST /api/verify-otp`
* `POST /api/reset-password`

---

## 🔒 Security Notes

* Passwords are hashed before storage
* OTP expires after a limited time
* Session-based authentication
* Foreign key constraints ensure data integrity

---

## 📌 Future Improvements

* JWT authentication
* Google OAuth login
* Travel analytics (charts, insights)
* AI-based travel recommendations
* Deployment (AWS / Render)

---

## 👨‍💻 Author

Seiya Genda
Computer Science × Marketing Student
University of Nebraska at Kearney

---

## ⭐️ Why this project?

This project demonstrates:

* Full-stack development
* Secure authentication systems
* Database design with relationships
* RESTful API design
* Real-world application structure

---
